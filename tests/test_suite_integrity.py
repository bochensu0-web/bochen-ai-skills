from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import install_skills  # noqa: E402
import package_skills  # noqa: E402


EXPECTED_SKILLS = {
    "bochen-answer-style": "core/bochen-answer-style",
    "bochen-learning-tutor": "learning/bochen-learning-tutor",
    "bochen-code-algorithm-tutor": "learning/bochen-code-algorithm-tutor",
    "bochen-ai-math-tutor": "learning/bochen-ai-math-tutor",
    "bochen-exam-master": "learning/bochen-exam-master",
    "bochen-academic-writer": "academic/bochen-academic-writer",
    "bochen-cn-engineering-paper": "academic/bochen-cn-engineering-paper",
    "bochen-research-verifier": "research/bochen-research-verifier",
    "bochen-tech-guide": "utility/bochen-tech-guide",
    "bochen-skill-builder": "meta/bochen-skill-builder",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.DOTALL)
    if not match:
        raise AssertionError("Missing YAML frontmatter block")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.startswith(" "):
            continue
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


class SuiteIntegrityTests(unittest.TestCase):
    def test_all_ten_skills_exist_and_pass_frontmatter_rules(self) -> None:
        for name, rel in EXPECTED_SKILLS.items():
            skill_dir = REPO_ROOT / rel
            self.assertTrue(skill_dir.is_dir(), f"Missing skill directory: {rel}")
            skill_md = skill_dir / "SKILL.md"
            readme_md = skill_dir / "README.md"
            openai_yaml = skill_dir / "agents" / "openai.yaml"
            self.assertTrue(skill_md.is_file(), f"Missing SKILL.md for {name}")
            self.assertTrue(readme_md.is_file(), f"Missing README.md for {name}")
            self.assertTrue(openai_yaml.is_file(), f"Missing openai.yaml for {name}")

            text = skill_md.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", text)
            self.assertNotIn("博宸", text, f"Homophone typo found in {skill_md}")
            self.assertLessEqual(len(text.splitlines()), 500, f"{name} exceeds 500 lines")

            fm = parse_frontmatter(text)
            self.assertEqual(fm.get("name"), name)
            self.assertGreaterEqual(len(fm.get("description", "")), 30)

            yaml_text = openai_yaml.read_text(encoding="utf-8")
            self.assertNotIn("\ufffd", yaml_text)
            self.assertNotIn("博宸", yaml_text, f"Homophone typo found in {openai_yaml}")
            self.assertIn("interface:", yaml_text)
            self.assertIn("display_name:", yaml_text)
            self.assertIn("short_description:", yaml_text)
            self.assertIn(f"${name}", yaml_text)

    def test_all_eval_files_are_valid_and_have_at_least_three_cases(self) -> None:
        eval_dir = REPO_ROOT / "evals"
        for name in EXPECTED_SKILLS:
            eval_file = eval_dir / f"{name}.json"
            self.assertTrue(eval_file.is_file(), f"Missing eval file: {eval_file.name}")
            payload = json.loads(eval_file.read_text(encoding="utf-8"))
            self.assertEqual(payload.get("skill_name"), name)
            cases = payload.get("evals", [])
            self.assertGreaterEqual(len(cases), 3, f"{name} should have >= 3 eval cases")
            ids = [c["id"] for c in cases]
            self.assertEqual(len(ids), len(set(ids)), f"Duplicate eval IDs in {name}")
            for case in cases:
                self.assertTrue(case.get("prompt"))
                self.assertTrue(case.get("expected_output"))
                self.assertIsInstance(case.get("files"), list)

    def test_trigger_matrix_covers_all_ten_skills(self) -> None:
        matrix = (REPO_ROOT / "evals" / "TRIGGER-MATRIX.md").read_text(encoding="utf-8")
        for name in EXPECTED_SKILLS:
            short = name.removeprefix("bochen-")
            self.assertTrue(
                name in matrix or short in matrix,
                f"Skill {name} missing from TRIGGER-MATRIX.md",
            )

    def test_local_markdown_links_resolve(self) -> None:
        link_pattern = re.compile(r"\]\((?!https?://|mailto:|#)([^)]+)\)")
        for md_file in REPO_ROOT.rglob("*.md"):
            if ".git" in md_file.parts or "fixtures" in md_file.parts:
                continue
            text = md_file.read_text(encoding="utf-8")
            for target in link_pattern.findall(text):
                clean_target = target.split("#", 1)[0].strip()
                if not clean_target:
                    continue
                resolved = (md_file.parent / clean_target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"Broken link '{target}' in {md_file.relative_to(REPO_ROOT)}",
                )

    def test_installer_and_clean_packager(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            install_dir = tmp_path / "installed"
            installed = install_skills.install_skills(
                install_dir,
                ["bochen-answer-style", "bochen-code-algorithm-tutor"],
            )
            self.assertEqual(len(installed), 2)
            self.assertTrue((install_dir / "bochen-answer-style" / "SKILL.md").is_file())

            out_dir = tmp_path / "packages"
            created = package_skills.package_all(out_dir)
            self.assertEqual(len(created), 11)
            for zpath in created:
                with zipfile.ZipFile(zpath) as zf:
                    for entry in zf.namelist():
                        self.assertNotIn(".git/", entry, f".git leaked in {zpath.name}")
                        self.assertNotIn("__pycache__", entry)

    def test_root_zip_archives_do_not_leak_git_metadata(self) -> None:
        for zpath in REPO_ROOT.glob("*.zip"):
            with zipfile.ZipFile(zpath) as zf:
                for entry in zf.namelist():
                    self.assertFalse(
                        entry.startswith(".git/") or "/.git/" in entry or entry.endswith(".pyc"),
                        f"Forbidden entry '{entry}' in {zpath.name}",
                    )


if __name__ == "__main__":
    unittest.main()
