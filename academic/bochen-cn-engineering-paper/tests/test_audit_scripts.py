from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


reference_audit = load_module("reference_audit")
citation_check = load_module("citation_consistency_check")
style_lint = load_module("academic_style_lint")
figure_table_audit = load_module("figure_table_audit")


class AuditScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.good = (FIXTURES / "sample_good.md").read_text(encoding="utf-8")
        cls.bad = (FIXTURES / "sample_bad.md").read_text(encoding="utf-8")

    def test_good_reference_list_has_no_errors(self):
        _, summary = reference_audit.audit_text(self.good)
        self.assertEqual(summary["errors"], 0)

    def test_bad_reference_list_finds_placeholder_and_gap(self):
        issues, summary = reference_audit.audit_text(self.bad)
        self.assertGreater(summary["errors"], 0)
        self.assertIn("PLACEHOLDER", {issue.code for issue in issues})
        self.assertIn("NUMBER_GAP", {issue.code for issue in issues})

    def test_good_citations_are_bidirectionally_consistent(self):
        _, summary = citation_check.audit_text(self.good)
        self.assertEqual(summary["errors"], 0)
        self.assertEqual(summary["warnings"], 0)

    def test_bad_citations_find_missing_reference(self):
        issues, summary = citation_check.audit_text(self.bad)
        self.assertGreater(summary["errors"], 0)
        self.assertIn("CITATION_WITHOUT_REFERENCE", {issue.code for issue in issues})

    def test_style_lint_is_not_silent_on_bad_text(self):
        issues, _ = style_lint.audit_text(self.bad)
        codes = {issue.code for issue in issues}
        self.assertIn("EMPTY_OPENING", codes)
        self.assertIn("UNSUPPORTED_SIGNIFICANCE", codes)
        self.assertIn("PLACEHOLDER", codes)

    def test_good_figure_table_links_have_no_errors(self):
        _, summary = figure_table_audit.audit_text(self.good)
        self.assertEqual(summary["errors"], 0)

    def test_bad_figure_table_links_find_missing_and_duplicate(self):
        issues, summary = figure_table_audit.audit_text(self.bad)
        self.assertGreater(summary["errors"], 0)
        codes = {issue.code for issue in issues}
        self.assertIn("MENTION_WITHOUT_CAPTION", codes)
        self.assertIn("DUPLICATE_CAPTION", codes)

    def test_auditors_ignore_fenced_code_blocks(self):
        text = """正文没有数字引文。\n\n```python\nvalues = [99]\n# 如图 9-9 所示\n# 随着人工智能的飞速发展\n[99] fake reference\n```\n\n## 参考文献\n\n[1] Real Author. Real title[J]. 2025.\n"""

        _, reference_summary = reference_audit.audit_text(text)
        self.assertEqual(reference_summary["entries"], 1)

        _, citation_summary = citation_check.audit_text(text)
        self.assertEqual(citation_summary["unique_citations"], 0)

        figure_issues, _ = figure_table_audit.audit_text(text)
        self.assertNotIn("MENTION_WITHOUT_CAPTION", {issue.code for issue in figure_issues})

        style_issues, _ = style_lint.audit_text(text)
        self.assertNotIn("EMPTY_OPENING", {issue.code for issue in style_issues})


if __name__ == "__main__":
    unittest.main()
