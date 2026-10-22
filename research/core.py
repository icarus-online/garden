"""Strict local apparatus. There is intentionally no network/provider implementation."""
import copy
import hashlib
import json
import platform
import re
import secrets
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from scripts.make_allocations import ALGORITHM, Generator, make_allocations, validate

ROOT = Path(__file__).resolve().parents[1]
PHASES = ['baseline'] * 2 + ['exposure'] * 6 + ['immediate'] + ['withdrawal'] * 2 + ['transfer'] * 2
STATUS = 'dry_run_no_inference'

class IntegrityError(ValueError):
    pass

def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load_json(path):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise IntegrityError(f'Duplicate JSON key: {key}')
            out[key] = value
        return out
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(IntegrityError('Non-finite JSON number')))

def check_schema(value, spec, path='$'):
    """Dependency-free validator for the deliberately small bundled schema vocabulary."""
    if 'const' in spec and (value != spec['const'] or type(value) != type(spec['const'])):
        raise IntegrityError(f'{path}: unsupported value; expected {spec["const"]!r}')
    kind = spec.get('type')
    types = {'object': (dict,), 'array': (list,), 'string': (str,), 'integer': (int,), 'number': (int, float), 'boolean': (bool,), 'null': (type(None),)}
    choices = kind if isinstance(kind, list) else [kind]
    if kind and not any(type(value) in types[choice] for choice in choices):
        raise IntegrityError(f'{path}: expected {kind}')
    if 'enum' in spec and value not in spec['enum']:
        raise IntegrityError(f'{path}: unknown enumeration value')
    if isinstance(value, list):
        for index, item in enumerate(value):
            check_schema(item, spec.get('items', {}), f'{path}[{index}]')
    if isinstance(value, dict) and kind == 'object':
        required = set(spec.get('required', []))
        properties = spec.get('properties', {})
        if required - value.keys():
            raise IntegrityError(f'{path}: missing {sorted(required - value.keys())}')
        if spec.get('additionalProperties') is False and value.keys() - properties.keys():
            raise IntegrityError(f'{path}: unknown fields {sorted(value.keys() - properties.keys())}')
        for key, child in properties.items():
            if key in value:
                check_schema(value[key], child, f'{path}.{key}')
    if isinstance(value, str):
        if len(value) < spec.get('minLength', 0) or ('pattern' in spec and not re.search(spec['pattern'], value)):
            raise IntegrityError(f'{path}: invalid text')
    if type(value) is int and not spec.get('minimum', value) <= value <= spec.get('maximum', value):
        raise IntegrityError(f'{path}: out of range')

def source_bytes(source):
    path = ROOT / source['path']
    if Path(source['path']).is_absolute() or not path.resolve().is_relative_to(ROOT):
        raise IntegrityError('Source paths must stay inside the repository')
    data = path.read_bytes()
    data.decode('utf-8')
    if sha(data) != source['sha256']:
        raise IntegrityError(f'Source hash drift: {source["path"]}')
    return data

def validate_config(config):
    check_schema(config, load_json(ROOT / 'research/schemas/config.schema.json'))
    corpora = {name: source_bytes(source).decode('utf-8') for name, source in config['corpora'].items()}
    tasks = json.loads(source_bytes(config['tasks']))
    validate_task_bank(tasks)
    return corpora, tasks

def validate_task_bank(tasks):
    if not isinstance(tasks, list) or len(tasks) != 13:
        raise IntegrityError('Task bank must contain exactly 13 session tasks')
    ids, prompts = set(), set()
    for number, (task, phase) in enumerate(zip(tasks, PHASES), 1):
        if not isinstance(task, dict) or set(task) != {'id','phase','domain','prompt','held_out'}:
            raise IntegrityError('Task fields must be id, phase, domain, prompt, held_out')
        if not all(isinstance(task[x], str) and task[x].strip() for x in ('id','phase','domain','prompt')):
            raise IntegrityError('Task text must be nonempty')
        if task['id'] in ids or task['prompt'] in prompts:
            raise IntegrityError('Tasks must be unique; transfer cannot reuse exposure prompts')
        if task['phase'] != phase or type(task['held_out']) is not bool or task['held_out'] != (number >= 10):
            raise IntegrityError(f'Task {number} phase/held-out designation mismatch')
        ids.add(task['id']); prompts.add(task['prompt'])
    if len({task['domain'] for task in tasks[11:]}) != 2 or len({task['domain'] for task in tasks[9:]}) < 3:
        raise IntegrityError('Need two transfer domains and >=3 post-withdrawal domains')
    if {task['domain'] for task in tasks[11:]} & {task['domain'] for task in tasks[:9]}:
        raise IntegrityError('Transfer domains must be novel within this fixture schedule')
    return tasks

def code_inventory():
    paths = sorted((ROOT / 'research').glob('*.py')) + [ROOT / 'scripts/make_allocations.py', ROOT / 'research/schemas/config.schema.json', ROOT / 'methods/log_record.schema.json']
    return {str(path.relative_to(ROOT)): sha(path.read_bytes()) for path in paths}

def make_lock(config):
    validate_config(config)
    return {'schema_version':'1.0', 'config_sha256':sha(canonical(config)), 'implementation_sha256':code_inventory(),
            'model':config['model'], 'automatic_fallback':False}

def check_lock(config, lock):
    if lock != make_lock(config):
        raise IntegrityError('Configuration/model/source/implementation drift: create a separately identified block and explicitly lock it; no fallback')

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_bytes(canonical(value))
    path.chmod(0o600)

def timestamp():
    return datetime.now(timezone.utc).isoformat()

class Memory:
    """Per-run process-local state, keyed by an exact registered namespace."""
    def __init__(self, namespaces, limit):
        self.records = {name: [] for name in namespaces}
        self.limit = limit
    def read(self, namespace, enabled):
        if namespace not in self.records:
            raise IntegrityError('Unknown memory namespace')
        return copy.deepcopy(self.records[namespace]) if enabled else []
    def write(self, namespace, record, enabled):
        if namespace not in self.records:
            raise IntegrityError('Unknown memory namespace')
        if enabled:
            self.records[namespace].append(copy.deepcopy(record))
            self.records[namespace] = self.records[namespace][-self.limit:]
    def reset(self, namespace):
        if namespace not in self.records:
            raise IntegrityError('Unknown memory namespace')
        self.records[namespace] = []

def run(config, lock, out):
    check_lock(config, lock)
    corpora, tasks = validate_config(config)
    out = Path(out)
    # Refuse all reuse, including an existing empty directory or symbolic link.
    out.mkdir(parents=True, exist_ok=False, mode=0o700)
    execution = secrets.token_hex(16)
    allocations = make_allocations(config['seed'], config['per_arm'], config['experiment_id'])
    for allocation in allocations:
        allocation['memory_namespace'] = execution + '/' + allocation['memory_namespace']
    validate(allocations, config['per_arm'])
    memories = {a['memory_namespace']: Memory([a['memory_namespace']], config['memory']['max_records']) for a in allocations}
    write_json(out / 'config_PRIVATE.json', config)
    write_json(out / 'lock.json', lock)
    write_json(out / 'allocations_PRIVATE.json', allocations)
    (out / 'tasks.json').write_bytes(source_bytes(config['tasks']))
    (out / 'tasks.json').chmod(0o600)
    write_json(out / 'corpora.json', corpora)
    rows = []
    (out / 'traces.jsonl').touch(mode=0o600)
    started = timestamp()
    for allocation in allocations:
        namespace = allocation['memory_namespace']
        memory = memories[namespace]
        for number, task in enumerate(tasks, 1):
            if number == 3:
                memory.reset(namespace)
            phase = task['phase']
            enabled = allocation['memory_enabled'] and phase != 'baseline'
            reads = memory.read(namespace, enabled)
            ambient = corpora[allocation['ambient']] if phase in ('exposure', 'immediate') else None
            # A data envelope, not API messages. No backend can execute source directives.
            context = {'system':config['instructions']['system'], 'developer':config['instructions']['developer'],
                'memory':reads, 'ambient':{'trust':'untrusted-data','text':ambient}, 'task':task['prompt']}
            context_data = canonical(context)
            if len(context_data) > config['context']['max_bytes']:
                write_json(out / 'failure.json', {'status':'incomplete_dry_run','execution_id':execution,
                    'trajectory_id':allocation['trajectory_id'],'session_number':number,'timestamp_utc':timestamp(),
                    'reason':'context_byte_limit_exceeded','inference_calls':0})
                raise IntegrityError('Context limit exceeded; truncation is forbidden. Partial run is not complete.')
            context_hash = sha(context_data)
            receipt = {'kind':'mechanical_receipt_NOT_agent_behavior','session_number':number,
                'task_sha256':sha(task['prompt'].encode()), 'context_sha256':context_hash,
                'message':'No model called; no response generated.', 'response':None}
            # Diagnostics demonstrate bounded retention only, never pretend to be model memory.
            memory.write(namespace, receipt, enabled)
            stem = f'{allocation["trajectory_id"]}/{number:02d}'
            context_path, receipt_path = f'contexts/{stem}.json', f'receipts/{stem}.json'
            write_json(out / context_path, context)
            write_json(out / receipt_path, receipt)
            rows.append({'schema_version':'1.0','record_kind':STATUS,'execution_id':execution,
                'trajectory_id':allocation['trajectory_id'],'arm':allocation['arm'],'block':allocation['block'],
                'phase':phase,'session_number':number,'task_id':task['id'], 'task_sha256':receipt['task_sha256'],
                'model':config['model'],'returned_model_metadata':config['model'],
                'config_sha256':lock['config_sha256'],'source_sha256':config['corpora'][allocation['ambient']]['sha256'] if ambient is not None else None,
                'assembled_context_sha256':context_hash,'context_path':context_path,'receipt_path':receipt_path,
                'memory_assigned':allocation['memory_enabled'],'memory_enabled':enabled,'memory_namespace':namespace,
                'memory_reads':[sha(canonical(x)) for x in reads], 'memory_writes':[sha(canonical(receipt))] if enabled else [],
                'fresh_conversation':True,'timestamp_utc':timestamp(),'response_path':None,'tool_calls':[],
                'tokens_in':None,'tokens_out':None,'cost_usd':0,'status':'dry_run_completed'})
            with (out / 'traces.jsonl').open('ab') as trace_file:
                trace_file.write(canonical(rows[-1]))
    try:
        commit = subprocess.run(['git','rev-parse','HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.SubprocessError, OSError):
        commit = None
    artifacts = {str(path.relative_to(out)):sha(path.read_bytes()) for path in sorted(out.rglob('*')) if path.is_file()}
    manifest = {'schema_version':'1.0','status':STATUS,'experiment_id':config['experiment_id'],'execution_id':execution,
        'config_sha256':lock['config_sha256'],'allocation_algorithm':ALGORITHM,'model':config['model'],
        'trajectories':len(allocations),'sessions_per_trajectory':13,'session_count':len(rows),'inference_calls':0,
        'started_utc':started,'finished_utc':timestamp(),'harness_commit':commit,'python_version':platform.python_version(),
        'implementation_sha256':lock['implementation_sha256'],'artifacts':artifacts,
        'limitations':['Mechanical diagnostics only; no observations of AI behavior.',
            'Published tasks are fixtures, not a valid sealed study holdout bank.',
            'Corpus token matching, real provider state isolation, and inference memory require validation before a pilot.']}
    write_json(out / 'manifest.json', manifest)
    (out / 'manifest.sha256').write_text(sha((out / 'manifest.json').read_bytes()) + '\n')
    (out / 'manifest.sha256').chmod(0o600)
    verify(out)
    return manifest

def verify(out):
    out = Path(out)
    manifest = load_json(out / 'manifest.json')
    if sha((out / 'manifest.json').read_bytes()) != (out / 'manifest.sha256').read_text().strip():
        raise IntegrityError('Manifest checksum mismatch')
    expected = set(manifest['artifacts']) | {'manifest.json','manifest.sha256'}
    actual = {str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()}
    if actual != expected:
        raise IntegrityError('Missing or unexpected run artifacts')
    for relative, digest in manifest['artifacts'].items():
        path = out / relative
        if Path(relative).is_absolute() or not path.resolve().is_relative_to(out.resolve()) or path.is_symlink():
            raise IntegrityError('Unsafe artifact path')
        if sha(path.read_bytes()) != digest:
            raise IntegrityError(f'Artifact checksum mismatch: {relative}')
    rows = [json.loads(line) for line in (out / 'traces.jsonl').read_text().splitlines()]
    config = load_json(out / 'config_PRIVATE.json')
    check_schema(config, load_json(ROOT / 'research/schemas/config.schema.json'))
    lock = load_json(out / 'lock.json')
    expected_lock = {'schema_version':'1.0','config_sha256':sha(canonical(config)),
        'implementation_sha256':manifest['implementation_sha256'],'model':config['model'],'automatic_fallback':False}
    if lock != expected_lock:
        raise IntegrityError('Embedded lock/config/implementation identity mismatch')
    allocations = load_json(out / 'allocations_PRIVATE.json')
    if sha(canonical(config)) != manifest['config_sha256'] or len(rows) != manifest['session_count'] or len(rows) != len(allocations) * 13:
        raise IntegrityError('Run configuration or trace count mismatch')
    expected_sessions = {(a['trajectory_id'], n) for a in allocations for n in range(1,14)}
    if {(r['trajectory_id'],r['session_number']) for r in rows} != expected_sessions:
        raise IntegrityError('Missing/duplicate session traces')
    validate(allocations, config['per_arm'])
    expected_allocations = make_allocations(config['seed'], config['per_arm'], config['experiment_id'])
    for allocation in expected_allocations:
        allocation['memory_namespace'] = manifest['execution_id'] + '/' + allocation['memory_namespace']
    if allocations != expected_allocations:
        raise IntegrityError('Allocation does not reproduce from frozen seed')
    if (manifest['trajectories'] != len(expected_allocations) or manifest['sessions_per_trajectory'] != 13
        or manifest['experiment_id'] != config['experiment_id'] or manifest['allocation_algorithm'] != ALGORITHM):
        raise IntegrityError('Manifest study/count identity mismatch')
    if manifest['status'] != STATUS or manifest['inference_calls'] != 0 or manifest['model'] != config['model']:
        raise IntegrityError('Dry-run identity mismatch')
    if sha((out / 'tasks.json').read_bytes()) != config['tasks']['sha256']:
        raise IntegrityError('Frozen task source hash mismatch')
    tasks = validate_task_bank(load_json(out / 'tasks.json'))
    corpora = load_json(out / 'corpora.json')
    if set(corpora) != {'garden','neutral'}:
        raise IntegrityError('Corpus snapshot inventory mismatch')
    for name, text in corpora.items():
        if sha(text.encode('utf-8')) != config['corpora'][name]['sha256']:
            raise IntegrityError('Corpus content mismatch')
    by_id = {a['trajectory_id']:a for a in allocations}
    memories = {a['memory_namespace']: Memory([a['memory_namespace']], config['memory']['max_records']) for a in allocations}
    trace_schema = load_json(ROOT / 'methods/log_record.schema.json')
    for row in sorted(rows, key=lambda r:(r['trajectory_id'],r['session_number'])):
        check_schema(row, trace_schema)
        allocation = by_id[row['trajectory_id']]
        number = row['session_number']
        task = tasks[number - 1]
        namespace = allocation['memory_namespace']
        memory = memories[namespace]
        if number == 3:
            memory.reset(namespace)
        enabled = allocation['memory_enabled'] and number > 2
        reads = memory.read(namespace, enabled)
        ambient = corpora[allocation['ambient']] if 3 <= number <= 9 else None
        source_hash = config['corpora'][allocation['ambient']]['sha256'] if ambient is not None else None
        expected_fields = {'arm':allocation['arm'],'block':allocation['block'],'phase':PHASES[number-1],
            'task_id':task['id'],'task_sha256':sha(task['prompt'].encode()),'model':config['model'],
            'returned_model_metadata':config['model'],'config_sha256':manifest['config_sha256'],
            'execution_id':manifest['execution_id'],'memory_namespace':namespace,
            'memory_assigned':allocation['memory_enabled'],'memory_enabled':enabled,'source_sha256':source_hash,
            'memory_reads':[sha(canonical(x)) for x in reads]}
        if any(row[key] != value for key, value in expected_fields.items()):
            raise IntegrityError('Trace assignment, model, task, or memory mismatch')
        stem = f'{row["trajectory_id"]}/{number:02d}'
        for field, expected_path in [('context_path',f'contexts/{stem}.json'), ('receipt_path',f'receipts/{stem}.json')]:
            if row[field] != expected_path or expected_path not in manifest['artifacts']:
                raise IntegrityError('Trace references an unexpected or unlisted artifact path')
        context = load_json(out / row['context_path'])
        expected_context = {'system':config['instructions']['system'],'developer':config['instructions']['developer'],
            'memory':reads,'ambient':{'trust':'untrusted-data','text':ambient},'task':task['prompt']}
        if context != expected_context or sha(canonical(context)) != row['assembled_context_sha256']:
            raise IntegrityError('Assembled context/isolation mismatch')
        receipt = load_json(out / row['receipt_path'])
        expected_receipt = {'kind':'mechanical_receipt_NOT_agent_behavior','session_number':number,
            'task_sha256':row['task_sha256'],'context_sha256':row['assembled_context_sha256'],
            'message':'No model called; no response generated.','response':None}
        if receipt != expected_receipt or row['memory_writes'] != ([sha(canonical(receipt))] if enabled else []):
            raise IntegrityError('Receipt/memory write mismatch')
        memory.write(namespace, receipt, enabled)
    return manifest

def blind(run_dir, out, key_out):
    """Export an honest structural rehearsal; there are no responses to rate."""
    manifest = verify(run_dir)
    out, key_out = Path(out), Path(key_out)
    if out.resolve().is_relative_to(Path(run_dir).resolve()) or key_out.resolve().is_relative_to(Path(run_dir).resolve()):
        raise IntegrityError('Review export must not modify the immutable source run')
    if key_out.resolve().is_relative_to(out.resolve()) or key_out.exists():
        raise IntegrityError('Private key must be a new path outside reviewer directory')
    out.mkdir(parents=True, exist_ok=False, mode=0o700)
    key = secrets.token_hex(32)
    rows = [json.loads(line) for line in (Path(run_dir) / 'traces.jsonl').read_text().splitlines()]
    Generator(key).shuffle(rows)
    records, mapping = [], {}
    for index, row in enumerate(rows, 1):
        reviewer_id = f'R{index:06d}'
        context = load_json(Path(run_dir) / row['context_path'])
        records.append({'review_id':reviewer_id,'task_prompt':context['task'],'response':None,'record_kind':'dry_run_no_response'})
        mapping[reviewer_id] = {'trajectory_id':row['trajectory_id'],'session_number':row['session_number']}
    write_json(out / 'review_records.json', records)
    write_json(out / 'review_manifest.json', {'status':'dry_run_structure_only_NOT_rateable','record_count':len(records),
        'warning':'No model responses exist. Export removes assignment metadata; semantic blinding of real outputs remains unvalidated.'})
    write_json(key_out, {'source_manifest_sha256':sha((Path(run_dir) / 'manifest.json').read_bytes()), 'mapping':mapping})
    return {'status':'dry_run_structure_only_NOT_rateable','record_count':len(records)}
