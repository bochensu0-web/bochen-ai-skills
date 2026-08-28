#!/usr/bin/env python3
"""Audit figure/table captions, numbering, mentions, and Markdown placement."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


CAPTION_RE = re.compile(r"^\s*(图|表)\s*(\d+(?:[-–—.]\d+)*)\s*[：:、.\s]\s*(\S.+?)\s*$")
MENTION_RE = re.compile(r"([图表])\s*(\d+(?:[-–—.]\d+)*)")
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
MARKDOWN_TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: int | None = None


def canonical(kind: str, number: str) -> str:
    return kind + re.sub(r"[–—.]", "-", number)


def audit_text(text: str) -> tuple[list[Issue], dict[str, int]]:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            lines.append("")
        elif in_fence:
            lines.append("")
        else:
            lines.append(line)
    captions: dict[str, list[int]] = {}
    mentions: dict[str, list[int]] = {}
    caption_lines: set[int] = set()
    issues: list[Issue] = []

    for line_no, line in enumerate(lines, 1):
        caption_match = CAPTION_RE.match(line)
        if caption_match:
            key = canonical(caption_match.group(1), caption_match.group(2))
            captions.setdefault(key, []).append(line_no)
            caption_lines.add(line_no)
            title = caption_match.group(3).strip()
            if len(title) < 3:
                issues.append(Issue("WARNING", "SHORT_CAPTION", f"{key} 的标题过短，难以自解释。", line_no))

        for kind, number in MENTION_RE.findall(line):
            key = canonical(kind, number)
            if not caption_match:
                mentions.setdefault(key, []).append(line_no)

    for key, line_numbers in captions.items():
        if len(line_numbers) > 1:
            issues.append(
                Issue("ERROR", "DUPLICATE_CAPTION", f"{key} 有多个题注，位于 {line_numbers}。")
            )
        if key not in mentions:
            issues.append(Issue("WARNING", "CAPTION_NOT_MENTIONED", f"{key} 未在正文中被引用。", line_numbers[0]))

    for key, line_numbers in mentions.items():
        if key not in captions:
            issues.append(Issue("ERROR", "MENTION_WITHOUT_CAPTION", f"正文引用 {key}，但未找到对应题注。", line_numbers[0]))

    for index, line in enumerate(lines):
        line_no = index + 1
        if MARKDOWN_IMAGE_RE.search(line):
            nearby = range(max(1, line_no - 2), min(len(lines), line_no + 2) + 1)
            if not any(candidate in caption_lines for candidate in nearby):
                issues.append(Issue("WARNING", "IMAGE_WITHOUT_NEARBY_CAPTION", "Markdown 图片附近未找到图题。", line_no))

        if MARKDOWN_TABLE_RE.match(line):
            previous_is_table = index > 0 and MARKDOWN_TABLE_RE.match(lines[index - 1])
            if previous_is_table:
                continue
            nearby = range(max(1, line_no - 3), min(len(lines), line_no + 1) + 1)
            if not any(candidate in caption_lines for candidate in nearby):
                issues.append(Issue("WARNING", "TABLE_WITHOUT_NEARBY_CAPTION", "Markdown 表格附近未找到表题。", line_no))

    for kind in ("图", "表"):
        by_chapter: dict[str, list[int]] = {}
        for key in captions:
            if not key.startswith(kind):
                continue
            parts = key[1:].split("-")
            if len(parts) >= 2 and parts[-1].isdigit():
                by_chapter.setdefault("-".join(parts[:-1]), []).append(int(parts[-1]))
        for chapter, values in by_chapter.items():
            unique = sorted(set(values))
            expected = list(range(1, max(unique) + 1))
            missing = sorted(set(expected) - set(unique))
            if missing:
                issues.append(
                    Issue("WARNING", "NUMBER_GAP", f"{kind}{chapter}-* 的编号缺失：{missing}。")
                )

    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)
    summary = {
        "figures": sum(key.startswith("图") for key in captions),
        "tables": sum(key.startswith("表") for key in captions),
        "errors": errors,
        "warnings": warnings,
    }
    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="检查图表题注、编号、正文引用和 Markdown 放置。")
    parser.add_argument("paper", type=Path, help="UTF-8 Markdown 或纯文本论文")
    parser.add_argument("--json", action="store_true", dest="as_json", help="输出 JSON")
    args = parser.parse_args()
    try:
        text = args.paper.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"无法读取文件：{exc}", file=sys.stderr)
        return 2

    issues, summary = audit_text(text)
    if args.as_json:
        print(json.dumps({"summary": summary, "issues": [asdict(i) for i in issues]}, ensure_ascii=False, indent=2))
    else:
        print(
            f"图题：{summary['figures']}；表题：{summary['tables']}；"
            f"错误：{summary['errors']}；警告：{summary['warnings']}"
        )
        for issue in issues:
            location = f"第 {issue.line} 行：" if issue.line else ""
            print(f"[{issue.severity}] {issue.code} {location}{issue.message}")
        print("说明：本工具不能判断图表数据真实性、可比性或版权状态。")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
