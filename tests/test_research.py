import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research.core import (IntegrityError, Memory, PHASES, blind, canonical, check_lock,
    load_json, make_lock, run, sha, validate_config, verify, write_json)
from scripts.make_allocations import make_allocations

class ResearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.base = Path(cls.temp.name)
        cls.config = load_json(ROOT / 'research/configs/dry-run.example.json')
        cls.config['per_arm'] = 1
        cls.lock = make_lock(cls.config)
        cls.first = cls.base / 'first'
        cls.second = cls.base / 'second'
        run(cls.config, cls.lock, cls.first)
        run(cls.config, cls.lock, cls.second)
        cls.rows = [json.loads(line) for line in (cls.first / 'traces.jsonl').read_text().splitlines()]

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_shipped_configuration_lock_validates(self):
        config = load_json(ROOT / 'research/configs/dry-run.example.json')
        check_lock(config, load_json(ROOT / 'research/configs/dry-run.example.lock.json'))

    def test_13_sessions_and_full_traces(self):
        manifest = verify(self.first)
        self.assertEqual(manifest['session_count'], 52)
        self.assertEqual(manifest['inference_calls'], 0)
        for trajectory in {row['trajectory_id'] for row in self.rows}:
            rows = [row for row in self.rows if row['trajectory_id'] == trajectory]
            self.assertEqual([row['phase'] for row in rows], PHASES)
            self.assertTrue(all(row['response_path'] is None and not row['tool_calls'] for row in rows))

    def test_repeated_runs_payloads_reproduce_and_namespaces_never_reuse(self):
        rows2 = [json.loads(line) for line in (self.second / 'traces.jsonl').read_text().splitlines()]
        self.assertEqual([r['assembled_context_sha256'] for r in self.rows], [r['assembled_context_sha256'] for r in rows2])
        self.assertTrue({r['memory_namespace'] for r in self.rows}.isdisjoint({r['memory_namespace'] for r in rows2}))
        self.assertEqual(len({r['memory_namespace'] for r in self.rows}), 4)

    def test_baseline_and_memory_off_cannot_carry_state(self):
        for row in self.rows:
            context = load_json(self.first / row['context_path'])
            if row['session_number'] <= 2 or row['arm'].endswith('0'):
                self.assertFalse(row['memory_enabled'])
                self.assertEqual(context['memory'], [])
                self.assertEqual(row['memory_reads'], [])
                self.assertEqual(row['memory_writes'], [])
            if row['session_number'] == 3:
                self.assertEqual(context['memory'], [])

    def test_stateless_postwithdrawal_contexts_identical_across_ambient_arms(self):
        for number in (1,2,10,11,12,13):
            rows = [row for row in self.rows if row['session_number'] == number and row['arm'].endswith('0')]
            self.assertEqual(rows[0]['assembled_context_sha256'], rows[1]['assembled_context_sha256'])

    def test_withdrawal_removes_ambient_and_keeps_only_allocated_memory(self):
        for row in self.rows:
            context = load_json(self.first / row['context_path'])
            if row['phase'] in ('baseline', 'withdrawal', 'transfer'):
                self.assertIsNone(context['ambient']['text'])
                self.assertIsNone(row['source_sha256'])
            else:
                self.assertTrue(context['ambient']['text'])
            if row['session_number'] >= 10 and row['arm'].endswith('1'):
                self.assertTrue(context['memory'])
                self.assertLessEqual(len(context['memory']), self.config['memory']['max_records'])

    def test_memory_namespace_denial_reset_and_disabled_write(self):
        foreign = Memory(['foreign'], 2)
        foreign.write('foreign', {'canary':'foreign-only'}, True)
        with self.assertRaises(IntegrityError):
            foreign.read('one', True)
        with self.assertRaises(IntegrityError):
            foreign.write('one', {'canary':'cross-trajectory'}, True)
        memory = Memory(['one','two'], 2)
        memory.write('one', {'canary':'one-only'}, True)
        self.assertEqual(memory.read('two', True), [])
        self.assertEqual(memory.read('one', False), [])
        memory.write('two', {'canary':'must-not-persist'}, False)
        self.assertEqual(memory.read('two', True), [])
        retrieved = memory.read('one', True)
        retrieved[0]['canary'] = 'modified'
        self.assertEqual(memory.read('one', True)[0]['canary'], 'one-only')
        with self.assertRaises(IntegrityError):
            memory.reset('unregistered')
        memory.reset('one')
        self.assertEqual(memory.read('one', True), [])
        with self.assertRaises(IntegrityError):
            memory.read('unregistered', True)

    def test_model_settings_extra_fields_and_live_calls_rejected(self):
        for field, value in [('provider','live-provider'),('model_id','other-model'),('reasoning_effort','high'),('temperature',0)]:
            config = copy.deepcopy(self.config)
            config['model'][field] = value
            with self.subTest(field=field), self.assertRaises(IntegrityError):
                validate_config(config)
        config = copy.deepcopy(self.config)
        config['automatic_fallback'] = True
        with self.assertRaises(IntegrityError):
            validate_config(config)
        config = copy.deepcopy(self.config)
        config['per_arm'] = True
        with self.assertRaises(IntegrityError):
            validate_config(config)

    def test_task_reuse_wrong_phase_and_non_novel_transfer_fail(self):
        from unittest.mock import patch
        from research.core import source_bytes
        original = json.loads(source_bytes(self.config['tasks']))
        for mutation in ('reused_prompt','wrong_phase','seen_transfer_domain'):
            tasks = copy.deepcopy(original)
            if mutation == 'reused_prompt':
                tasks[12]['prompt'] = tasks[2]['prompt']
            elif mutation == 'wrong_phase':
                tasks[12]['phase'] = 'exposure'
            else:
                tasks[12]['domain'] = tasks[2]['domain']
            def source_override(source):
                return canonical(tasks) if source == self.config['tasks'] else source_bytes(source)
            with self.subTest(mutation=mutation), patch('research.core.source_bytes', side_effect=source_override):
                with self.assertRaises(IntegrityError):
                    validate_config(self.config)

    def test_lock_detects_configuration_implementation_and_corpus_drift(self):
        config = copy.deepcopy(self.config)
        config['instructions']['system'] += ' changed'
        with self.assertRaises(IntegrityError):
            check_lock(config, self.lock)
        lock = copy.deepcopy(self.lock)
        lock['implementation_sha256']['research/core.py'] = '0' * 64
        with self.assertRaises(IntegrityError):
            check_lock(self.config, lock)
        config = copy.deepcopy(self.config)
        config['corpora']['garden']['sha256'] = '0' * 64
        with self.assertRaises(IntegrityError):
            validate_config(config)

    def test_reject_source_path_escape(self):
        config = copy.deepcopy(self.config)
        config['tasks']['path'] = '../outside.json'
        with self.assertRaises(IntegrityError):
            validate_config(config)

    def test_existing_output_refused(self):
        with self.assertRaises(FileExistsError):
            run(self.config, self.lock, self.first)

    def test_oversize_context_fails_without_silent_truncation(self):
        config = copy.deepcopy(self.config)
        config['context']['max_bytes'] = 1000
        with self.assertRaises(IntegrityError):
            run(config, make_lock(config), self.base / 'oversize')
        self.assertFalse((self.base / 'oversize/manifest.json').exists())
        self.assertEqual(load_json(self.base / 'oversize/failure.json')['reason'], 'context_byte_limit_exceeded')
        self.assertEqual(len((self.base / 'oversize/traces.jsonl').read_text().splitlines()), 2)

    def test_tampered_artifact_and_missing_trace_rejected(self):
        import shutil
        path = self.base / 'tampered'
        shutil.copytree(self.first, path)
        target = path / self.rows[0]['receipt_path']
        target.write_text('tampered')
        with self.assertRaises(IntegrityError):
            verify(path)
        path2 = self.base / 'missing'
        shutil.copytree(self.first, path2)
        (path2 / 'traces.jsonl').unlink()
        with self.assertRaises(IntegrityError):
            verify(path2)

    def test_rehashed_contamination_still_fails_semantic_validation(self):
        import shutil
        path = self.base / 'contaminated'
        shutil.copytree(self.first, path)
        rows = [json.loads(line) for line in (path / 'traces.jsonl').read_text().splitlines()]
        rows[0]['memory_enabled'] = True
        (path / 'traces.jsonl').write_bytes(b''.join(canonical(row) for row in rows))
        manifest = load_json(path / 'manifest.json')
        manifest['artifacts']['traces.jsonl'] = sha((path / 'traces.jsonl').read_bytes())
        write_json(path / 'manifest.json', manifest)
        (path / 'manifest.sha256').write_text(sha((path / 'manifest.json').read_bytes()))
        with self.assertRaises(IntegrityError):
            verify(path)

    def test_rehashed_path_task_lock_allocation_and_count_corruption_rejected(self):
        import shutil
        for mutation in ('outside_context','wrong_receipt','task_metadata','lock','allocation','count','unknown_config'):
            with self.subTest(mutation=mutation):
                path = self.base / ('corruption-' + mutation)
                shutil.copytree(self.first, path)
                manifest = load_json(path / 'manifest.json')
                if mutation in ('outside_context','wrong_receipt'):
                    rows = [json.loads(line) for line in (path / 'traces.jsonl').read_text().splitlines()]
                    rows[0]['context_path' if mutation == 'outside_context' else 'receipt_path'] = '../private-outside.json'
                    (path / 'traces.jsonl').write_bytes(b''.join(canonical(row) for row in rows))
                elif mutation == 'task_metadata':
                    tasks = load_json(path / 'tasks.json')
                    tasks[-1]['domain'] = 'changed-but-still-unique'
                    write_json(path / 'tasks.json', tasks)
                elif mutation == 'lock':
                    lock = load_json(path / 'lock.json')
                    lock['automatic_fallback'] = True
                    write_json(path / 'lock.json', lock)
                elif mutation == 'allocation':
                    allocations = load_json(path / 'allocations_PRIVATE.json')
                    allocations[0], allocations[1] = allocations[1], allocations[0]
                    write_json(path / 'allocations_PRIVATE.json', allocations)
                elif mutation == 'unknown_config':
                    config = load_json(path / 'config_PRIVATE.json')
                    config['fallback_model'] = 'untracked-model'
                    write_json(path / 'config_PRIVATE.json', config)
                else:
                    manifest['trajectories'] += 4
                for relative in manifest['artifacts']:
                    manifest['artifacts'][relative] = sha((path / relative).read_bytes())
                write_json(path / 'manifest.json', manifest)
                (path / 'manifest.sha256').write_text(sha((path / 'manifest.json').read_bytes()))
                with self.assertRaises(IntegrityError):
                    verify(path)

    def test_blind_export_contains_no_assignment_metadata_or_fake_responses(self):
        out = self.base / 'blind'
        key = self.base / 'blind-key_PRIVATE.json'
        result = blind(self.first, out, key)
        self.assertEqual(result['record_count'], 52)
        records = load_json(out / 'review_records.json')
        for row in records:
            self.assertEqual(set(row), {'review_id','task_prompt','response','record_kind'})
            self.assertIsNone(row['response'])
        self.assertEqual(len({r['review_id'] for r in records}), 52)
        mapping = load_json(key)['mapping']
        self.assertEqual(set(mapping), {r['review_id'] for r in records})
        for path in out.iterdir():
            text = path.read_text()
            for forbidden in ('memory_namespace','assembled_context_sha256','trajectory_id','Philosophy.md','"G1"','"N1"'):
                self.assertNotIn(forbidden, text)
        self.assertNotEqual([mapping[r['review_id']]['trajectory_id'] for r in records], [r['trajectory_id'] for r in self.rows])
        with self.assertRaises(IntegrityError):
            blind(self.first, self.base / 'badblind', self.base / 'badblind/key.json')

    def test_cli_round_trip(self):
        config_path = self.base / 'cli.json'
        write_json(config_path, self.config)
        for arguments in [
            ['lock', str(config_path)], ['validate',str(config_path)],
            ['run',str(config_path),'--out',str(self.base / 'cli-run')],
            ['verify',str(self.base / 'cli-run')]]:
            process = subprocess.run([sys.executable,'-m','research',*arguments],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
        config = copy.deepcopy(self.config)
        config['seed'] = 'drift'
        write_json(config_path, config)
        process = subprocess.run([sys.executable,'-m','research','validate',str(config_path)],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(process.returncode, 2)
        self.assertIn('drift', process.stderr)

if __name__ == '__main__':
    unittest.main()
