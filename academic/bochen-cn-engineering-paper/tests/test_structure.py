from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StructureTests(unittest.TestCase):
    def test_openai_yaml_is_utf8_and_keeps_chinese_interface(self):
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("\ufffd", text)
        self.assertIn("苏博晨中国工科论文助手", text)
        self.assertIn("$bochen-cn-engineering-paper", text)

    def test_all_local_markdown_links_from_skill_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        local_links = re.findall(r"\]\((references/[^)]+\.md)\)", skill)
        self.assertGreaterEqual(len(local_links), 10)
        for relative in local_links:
            self.assertTrue((ROOT / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
