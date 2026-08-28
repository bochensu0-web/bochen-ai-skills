#!/usr/bin/env python3
"""Check bidirectional consistency between numeric citations and references."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REFERENCE_HEADING_RE = re.compile(r"(?im)^#{0,6}\s*(参考文献|references)\s*$")
REFERENCE_ENTRY_RE = re.compile(r"(?m)^\s*\[(\d+)\]\s+.+$")
CITATION_GROUP_RE = re.compile(r"\[\s*(\d+(?:\s*[-–—,，]\s*\d+)*)\s*\]")


@dataclass
class Issue:
    severity: str
    code: str
    message: str


def expand_group(group: str) -> list[int]:
    values: list[int] = []
    for part in re.split(r"\s*[,，]\s*", group):
        range_match = re.fullmatch(r"(\d+)\s*[-–—]\s*(\d+)", part)
        if range_match:
            start, end = map(int, range_match.groups())
            if 0 < end - start <= 1000:
                values.extend(range(start, end + 1))
            else:
                values.extend([start, end])
        elif part.isdigit():
            values.append(int(part))
    return values


def strip_fenced_code(text: str) -> str:
    output: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            output.append("\n" if line.endswith("\n") else "")
        elif in_fence:
            output.append("\n" if line.endswith("\n") else "")
        else:
            output.append(line)
    return "".join(output)


def audit_text(text: str) -> tuple[list[Issue], dict[str, int]]:
    text = strip_fenced_code(text)
    heading = REFERENCE_HEADING_RE.search(text)
    if heading:
        body = text[: heading.start()]
        references_text = text[heading.end() :]
    else:
        first_entry = REFERENCE_ENTRY_RE.search(text)
        body = text[: first_entry.start()] if first_entry else text
        references_text = text[first_entry.start() :] if first_entry else ""

    reference_numbers = [int(n) for n in REFERENCE_ENTRY_RE.findall(references_text)]
    citation_numbers: list[int] = []
    for group in CITATION_GROUP_RE.findall(body):
        citation_numbers.extend(expand_group(group))

    issues: list[Issue] = []
    ref_set = set(reference_numbers)
    cited_set = set(citation_numbers)

    if not reference_numbers:
        issues.append(Issue("ERROR", "NO_REFERENCES", "未找到文后参考文献条目。"))
    if not citation_numbers:
        issues.append(Issue("WARNING", "NO_CITATIONS", "正文未找到数字顺序编码引文。"))

    duplicate_refs = sorted({n for n in reference_numbers if reference_numbers.count(n) > 1})
    if duplicate_refs:
        issues.append(Issue("ERROR", "DUPLICATE_REFERENCE", f"文后编号重复：{duplicate_refs}。"))

    missing_refs = sorted(cited_set - ref_set)
    if missing_refs:
        issues.append(Issue("ERROR", "CITATION_WITHOUT_REFERENCE", f"正文引用但文后缺少：{missing_refs}。"))

    uncited_refs = sorted(ref_set - cited_set)
    if uncited_refs:
        issues.append(Issue("WARNING", "UNCITED_REFERENCE", f"文后存在但正文未引用：{uncited_refs}。"))

    first_seen: list[int] = []
    for number in citation_numbers:
        if number not in first_seen:
            first_seen.append(number)
    if first_seen and first_seen != sorted(first_seen):
        issues.append(
            Issue("WARNING", "FIRST_CITATION_ORDER", f"首次引用顺序不是升序：{first_seen}。请按学校格式确认。")
        )

    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)
    summary = {
        "unique_citations": len(cited_set),
        "references": len(reference_numbers),
        "errors": errors,
        "warnings": warnings,
    }
    return issues, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="检查数字引文与参考文献的双向一致性。")
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
            f"正文唯一引文：{summary['unique_citations']}；文后条目：{summary['references']}；"
            f"错误：{summary['errors']}；警告：{summary['warnings']}"
        )
        for issue in issues:
            print(f"[{issue.severity}] {issue.code} {issue.message}")
        print("说明：本工具只检查编号一致性，不验证来源真实性或主张支持关系。")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
