from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVAL_FILE = ROOT.parents[1] / "evals" / "bochen-cn-engineering-paper.json"


class EvalSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
        cls.evals = cls.payload["evals"]

    def test_suite_contains_eight_unique_realistic_scenarios(self):
        self.assertEqual(len(self.evals), 8)
        self.assertEqual(len({case["id"] for case in self.evals}), 8)
        for case in self.evals:
            self.assertGreaterEqual(len(case["prompt"]), 15)
            self.assertGreaterEqual(len(case["expected_output"]), 20)

    def test_suite_covers_integrity_school_rules_and_full_lifecycle(self):
        prompts = "\n".join(case["prompt"] for case in self.evals)
        lifecycle_concepts = (
            ("选题", "题目是否太大"),
            ("文献",),
            ("实验",),
            ("初稿",),
            ("北交大",),
            ("图表",),
            ("终稿",),
            ("答辩",),
        )
        for alternatives in lifecycle_concepts:
            self.assertTrue(any(concept in prompts for concept in alternatives), alternatives)


if __name__ == "__main__":
    unittest.main()
