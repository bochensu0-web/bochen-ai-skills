"""Package individual skills and the full suite into clean, deterministic ZIP archives."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

from install_skills import REPO_ROOT, discover_skills


EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache", "dist"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip"}
EXCLUDED_FILES = {".DS_Store", "Thumbs.db"}


def should_include(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.name in EXCLUDED_FILES or path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def write_deterministic_zip(source_dir: Path, zip_path: Path, prefix: str = "") -> int:
    files = sorted(p for p in source_dir.rglob("*") if should_include(p, source_dir))
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in files:
            rel_posix = file.relative_to(source_dir).as_posix()
            arcname = f"{prefix}/{rel_posix}" if prefix else rel_posix
            info = zipfile.ZipInfo(arcname, date_time=(2026, 8, 28, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, file.read_bytes())
    return len(files)


def package_all(output_dir: Path, root: Path = REPO_ROOT) -> list[Path]:
    created: list[Path] = []
    for name, skill_dir in discover_skills(root).items():
        zip_path = output_dir / f"{name}.zip"
        prefix = name if name == "bochen-cn-engineering-paper" else ""
        write_deterministic_zip(skill_dir, zip_path, prefix=prefix)
        created.append(zip_path)

    suite_zip = output_dir / "bochen-ai-skills.zip"
    write_deterministic_zip(root, suite_zip, prefix="bochen-ai-skills")
    created.append(suite_zip)
    return created


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build clean skill ZIP packages.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT,
        help="Directory where ZIP archives will be written (default: repo root).",
    )
    args = parser.parse_args(argv)
    created = package_all(args.output_dir)
    for path in created:
        print(f"Packaged: {path.name} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
