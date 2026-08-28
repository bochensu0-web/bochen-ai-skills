#!/usr/bin/env python3
"""Lint common clarity problems in Chinese academic prose.

This is a transparent style checker, not an AI-writing detector.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Issue:
    severity: str
    code: str
    message: str
    line: int | None = None


PHRASES = {
    "EMPTY_OPENING": re.compile(r"随着.{0,18}(快速|迅速|飞速|蓬勃)发展"),
    "VAGUE_CONSENSUS": re.compile(r"众所周知|不难发现|显而易见"),
    "VAGUE_IMPORTANCE": re.compile(r"具有(十分|非常|重要)?的?(理论|现实|实践)?意义"),
    "VAGUE_RESEARCH": re.compile(r"国内外(专家|学者)?(已经)?(进行了|开展了)?大量(的)?研究"),
    "GENERIC_RESULT": re.compile(r"实验结果表明.{0,20}(有效|优越|良好|可行)(?:[。；;]|$)"),
    "ABSOLUTE_CLAIM": re.compile(r"(完全|彻底|必然|绝对|全面)解决|达到最优|世界领先|填补.{0,8}空白"),
    "PLACEHOLDER": re.compile(r"(?i)\[(待补|待核验|填入|TODO|TBD)[^\]]*\]|XXX"),
}

SIGNIFICANT_RE = re.compile(r"显著(提高|提升|降低|优于|改善|增强|减少)")
SIGNIFICANCE_EVIDENCE_RE = re.compile(r"(%|％|百分点|p\s*[<=>]|P\s*[<=>]|置信区间|显著性|效应量|阈值)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？；!?;])")


def visible_length(sentence: str) -> int:
    return len(re.sub(r"\s+", "", sentence))


def audit_text(text: str) -> tuple[list[Issue], dict[str, int]]:
    issues: list[Issue] = []
    connector_count = 0
    nonempty_lines = 0
    in_fence = False

    for line_no, raw_line in enumerate(text.splitlines(), 1):
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line or line.startswith("#") or line.startswith("|"):
            continue
        nonempty_lines += 1

        for code, pattern in PHRASES.items():
            if pattern.search(line):
                severity = "ERROR" if code == "PLACEHOLDER" else "WARNING"
                advice = {
                    "EMPTY_OPENING": "直接写与研究问题有关的技术变化、数据或场景。",
                    "VAGUE_CONSENSUS": "给出证据或删除无需证明的强调。",
                    "VAGUE_IMPORTANCE": "分别说明解决什么问题、影响什么对象。",
                    "VAGUE_RESEARCH": "概括主要方法、代表证据和真实分歧。",
                    "GENERIC_RESULT": "补充指标、基线、数值、条件与边界。",
                    "ABSOLUTE_CLAIM": "降低结论强度，或提供足够证据与适用范围。",
                    "PLACEHOLDER": "终稿前补齐真实证据或明确删除。",
                }[code]
                issues.append(Issue(severity, code, advice, line_no))

        if SIGNIFICANT_RE.search(line) and not SIGNIFICANCE_EVIDENCE_RE.search(line):
            issues.append(
                Issue(
                    "WARNING",
                    "UNSUPPORTED_SIGNIFICANCE",
                    "出现“显著”但本句没有数值、统计或工程判据；请核对证据强度。",
                    line_no,
                )
            )

        connector_count += len(re.findall(r"首先|其次|再次|最后|综上所述", line))

        for sentence in SENTENCE_SPLIT_RE.split(line):
            if visible_length(sentence) > 100:
                issues.append(
                    Issue(
                        "WARNING",
                        "LONG_SENTENCE",
                        f"句子约 {visible_length(sentence)} 字，建议按主张、证据或条件拆分。",
                        line_no,
                    )
                )

        if re.search(r"(^|[。；])\s*(进行了|开展了|实现了|完成了)", line) and not re.search(
            r"本文|本研究|本系统|本方法|实验|团队|作者|模型", line
        ):
            issues.append(
                Issue("WARNING", "UNCLEAR_SUBJECT", "动作句主语可能不清楚，请说明谁完成了什么。", line_no)
            )

    if connector_count >= 8 and nonempty_lines:
        issues.append(
            Issue(
                "WARNING",
                "MECHANICAL_CONNECTORS",
                f"检测到 {connector_count} 个顺序/总结连接词，检查是否存在机械罗列。",
            )
        )

    errors = sum(issue.severity == "ERROR" for issue in issues)
    warnings = sum(issue.severity == "WARNING" for issue in issues)
    return issues, {"checked_lines": nonempty_lines, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="检查中文学术文本中的空泛、夸张、占位和可读性问题。")
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
        print(f"检查正文行：{summary['checked_lines']}；错误：{summary['errors']}；警告：{summary['warnings']}")
        for issue in issues:
            location = f"第 {issue.line} 行：" if issue.line else ""
            print(f"[{issue.severity}] {issue.code} {location}{issue.message}")
        print("说明：本工具不是 AI 写作检测器；提示需结合学科内容人工判断。")
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
