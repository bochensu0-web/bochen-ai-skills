"""Install Bochen AI Skills into supported Agent clients or a custom directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_REL_PATHS: dict[str, str] = {
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

CLIENT_DEFAULTS: dict[str, Path] = {
    "codex": Path.home() / ".codex" / "skills",
    "antigravity": Path.home() / ".gemini" / "config" / "skills",
    "claude": Path.home() / ".claude" / "skills",
    "agents": Path.cwd() / ".agents" / "skills",
}

IGNORE_NAMES = {"__pycache__", ".pytest_cache", ".DS_Store", "Thumbs.db"}


def discover_skills(root: Path = REPO_ROOT) -> dict[str, Path]:
    return {name: root / rel for name, rel in SKILL_REL_PATHS.items()}


def install_skills(
    target_dir: Path,
    skill_names: list[str] | None = None,
    *,
    dry_run: bool = False,
    root: Path = REPO_ROOT,
) -> list[Path]:
    available = discover_skills(root)
    selected = skill_names or list(available.keys())
    unknown = [name for name in selected if name not in available]
    if unknown:
        raise ValueError(f"Unknown skill(s): {', '.join(unknown)}")

    installed: list[Path] = []
    for name in selected:
        src = available[name]
        dest = target_dir / name
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(
                src,
                dest,
                ignore=shutil.ignore_patterns(*IGNORE_NAMES, "*.pyc"),
            )
        installed.append(dest)
    return installed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Install Bochen AI Skills.")
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available skills and exit.",
    )
    parser.add_argument(
        "--client",
        choices=sorted(CLIENT_DEFAULTS.keys()),
        default="antigravity",
        help="Target client preset when --target is not specified (default: antigravity).",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Explicit destination directory for installed skill folders.",
    )
    parser.add_argument(
        "--skills",
        nargs="+",
        default=None,
        help="Subset of skill names to install (defaults to all 10 skills).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned destination paths without copying files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    available = discover_skills()
    if args.list:
        for name, path in available.items():
            print(f"{name:30s} -> {path.relative_to(REPO_ROOT).as_posix()}")
        return 0

    target = args.target if args.target is not None else CLIENT_DEFAULTS[args.client]
    installed = install_skills(target, args.skills, dry_run=args.dry_run)
    prefix = "[dry-run] Would install" if args.dry_run else "Installed"
    for dest in installed:
        print(f"{prefix}: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
