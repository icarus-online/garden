import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from make_allocations import make_allocations, validate, seed_hash

class AllocationTests(unittest.TestCase):
    def test_fixed_seed_reproduces(self):
        self.assertEqual(make_allocations("test-123"), make_allocations("test-123"))
    def test_different_seeds_differ(self):
        self.assertNotEqual(make_allocations("test-123"), make_allocations("test-124"))
    def test_balanced_and_isolated(self):
        allocations = make_allocations("garden-study", 12)
        self.assertTrue(validate(allocations,12))
        self.assertEqual(Counter(x["arm"] for x in allocations), {"N0":12,"G0":12,"N1":12,"G1":12})
    def test_one_each_in_block(self):
        items=make_allocations("other-seed",16)
        self.assertEqual({x["arm"] for x in items[:4]}, {"N0","G0","N1","G1"})
    def test_algorithm_golden_vector_and_namespace_scope(self):
        self.assertEqual([x['arm'] for x in make_allocations('golden-雪-001',4)],
            ['G1','N1','N0','G0','N0','G0','G1','N1','N0','G0','N1','G1','G0','G1','N1','N0'])
        one = make_allocations('same',1,'experiment-one')
        two = make_allocations('same',1,'experiment-two')
        self.assertEqual([x['arm'] for x in one], [x['arm'] for x in two])
        self.assertTrue({x['memory_namespace'] for x in one}.isdisjoint({x['memory_namespace'] for x in two}))
    def test_validation_not_disabled_by_python_optimization(self):
        items = make_allocations('seed',1)
        items[0]['memory_namespace'] = items[1]['memory_namespace']
        with self.assertRaises(ValueError): validate(items,1)
    def test_empty_seed_and_boolean_count_rejected(self):
        with self.assertRaises(ValueError): make_allocations('',1)
        with self.assertRaises(ValueError): make_allocations('seed',True)
    def test_seed_not_zero(self):
        self.assertNotEqual(seed_hash(""),0)
    def test_invalid_count(self):
        with self.assertRaises(ValueError): make_allocations("a",0)
        with self.assertRaises(ValueError): make_allocations("a",2001)

if __name__ == "__main__":
    unittest.main()
