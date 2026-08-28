#!/usr/bin/env python3
"""Audit numbered reference entries in a Markdown or plain-text paper.

This script is intentionally conservative. It checks structure and suspicious
placeholders; it does not verify that a publication exists or supports a claim.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


ENTRY_RE = re.compile(r"^\s*\[(\d+)\]\s+(.+?)\s*$")
DOI_TOKEN_RE = re.compile(r"(?i)\bdoi\s*[:：]?\s*([^\s，。；;]+)")
VALID_DOI_RE = re.compile(r"(?i)^10\.\d{4,9}/[-._;()/:A-Z0-9]+$")
PLACEHOLDER_RE = re.compile(
    r"(?i)(待核验|待补|待填写|unknown|tbd|todo|xxx|example\.com|示例文献|某某)"
)
YEAR_RE = re.compile(r"(?<!\d)(19\d{2}|20\d{2})(?!\d)")


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: int | None = None


def normalize_entry(text: str) -> str:
    text = re.sub(r"https?://\S+", "", text.lower())
    text = re.sub(r"(?i)\bdoi\s*[:：]?\s*\S+", "", text)
    return re.sub(r"[\W_]+", "", text, flags=re.UNICODE)


def audit_text(text: str) -> tuple[list[Issue], dict[str, int]]:
    entries: list[tuple[int, str, int]] = []
    in_fence = False
    for line_no, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = ENTRY_RE.match(line)
        if match:
            entries.append((int(match.group(1)), match.group(2), line_no))

    issues: list[Issue] = []
    if not entries:
        issues.append(Issue("ERROR", "NO_REFERENCES", "未找到形如 [1] 文献条目的参考文献。"))
        return issues, {"entries": 0, "errors": 1, "warnings": 0}

    numbers = [number for number, _, _ in entries]
    seen_numbers: dict[int, int] = {}
    for number, _, line_no in entries:
        if number in seen_numbers:
            issues.append(
                Issue("ERROR", "DUPLICATE_NUMBER", f"编号 [{number}] 重复。", line_no)
            )
        else:
            seen_numbers[number] = line_no

    expected = list(range(1, max(numbers) + 1))
    missing = sorted(set(expected) - set(numbers))
    if missing:
        issues.append(
            Issue("ERROR", "NUMBER_GAP", f"参考文献编号缺失：{', '.join(map(str, missing))}。")
        )
    if numbers != sorted(numbers):
        issues.append(Issue("WARNING", "NUMBER_ORDER", "参考文献条目未按编号升序排列。"))

    normalized_seen: dict[str, int] = {}
    current_year = datetime.now().year
    for number, entry, line_no in entries:
        if PLACEHOLDER_RE.search(entry):
            issues.append(
                Issue("ERROR", "PLACEHOLDER", f"文献 [{number}] 含未完成或示例占位内容。", line_no)
            )

        normalized = normalize_entry(entry)
        if normalized and normalized in normalized_seen:
            issues.append(
                Issue(
                    "WARNING",
                    "POSSIBLE_DUPLICATE",
                    f"文献 [{number}] 可能与 [{normalized_seen[normalized]}] 重复。",
                    line_no,
                )
            )
        else:
            normalized_seen[normalized] = number

        years = [int(value) for value in YEAR_RE.findall(entry)]
        for year in years:
            if year > current_year + 1:
                issues.append(
                    Issue("ERROR", "FUTURE_YEAR", f"文献 [{number}] 的年份 {year} 可疑。", line_no)
                )

        for doi_token in DOI_TOKEN_RE.findall(entry):
            doi = doi_token.rstrip(".,;，。；)")
            if not VALID_DOI_RE.match(doi):
                issues.append(
                    Issue("WARNING", "DOI_FORMAT", f"文献 [{number}] 的 DOI 格式需核对：{doi}", line_no)
                )

        if len(entry.strip()) < 12:
            issues.append(
                Issue("WARNING", "TOO_SHORT", f"文献 [{number}] 条目信息可能不完整。", line_no)
            )

    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)
    return issues, {"entries": len(entries), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="检查参考文献编号、重复、占位符和 DOI 格式。")
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
        print(f"参考文献条目：{summary['entries']}；错误：{summary['errors']}；警告：{summary['warnings']}")
        for issue in issues:
            location = f"第 {issue.line} 行：" if issue.line else ""
            print(f"[{issue.severity}] {issue.code} {location}{issue.message}")
        print("说明：本工具不验证文献真实性，也不判断文献是否支持正文主张。")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
