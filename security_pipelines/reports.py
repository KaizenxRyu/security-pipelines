"""Readable portable reports; raw credentials and tool arguments are omitted."""

import html
import json
from pathlib import Path


def write_reports(result: dict, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "report.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    rows = []
    for name, run in result["runs"].items():
        rows.append(f"| {name} | {run['forbidden_allowed']}/{run['forbidden_total']} | "
                    f"{run['legitimate_blocked']}/{run['legitimate_total']} |")
    failed = [row["id"] for row in result["runs"]["governed"]["cases"] if not row["passed"]]
    text = (f"# Agent boundary replay: {result['verdict']}\n\n"
            f"**{result['limits']}**\n\n"
            f"Cases: {result['case_count']} · Suite SHA-256: `{result['suite_sha256']}`\n\n"
            "| Variant | Forbidden calls allowed | Legitimate calls blocked |\n"
            "| --- | --- | --- |\n" + "\n".join(rows) + "\n\n"
            + "Failed governed cases: " + (", ".join(failed) if failed else "none") + "\n")
    (destination / "report.md").write_text(text, encoding="utf-8")
    table = "".join("<tr><td>" + name + "</td><td>" +
                    f"{run['forbidden_allowed']}/{run['forbidden_total']}" + "</td><td>" +
                    f"{run['legitimate_blocked']}/{run['legitimate_total']}" + "</td></tr>"
                    for name, run in result["runs"].items())
    page = ("<!doctype html><html lang='en'><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Security pipelines report</title><style>"
            "body{font:17px system-ui;background:#f5f8fc;color:#162438;margin:0;padding:6vw}"
            "main{max-width:850px;margin:auto}h1{font-size:clamp(28px,5vw,48px)}"
            "table{width:100%;border-collapse:collapse;background:white}"
            "th,td{padding:18px;border-bottom:1px solid #cbd9ed;text-align:left}"
            "code{overflow-wrap:anywhere}p{line-height:1.7}</style><main>"
            f"<p>KaizenxRyu · Security pipelines</p><h1>Boundary replay: {result['verdict']}</h1>"
            f"<p>{html.escape(result['limits'])}</p><table><thead><tr><th>Variant</th>"
            "<th>Forbidden allowed</th><th>Legitimate blocked</th></tr></thead>"
            f"<tbody>{table}</tbody></table><p>{result['case_count']} identical paired cases. "
            "Counts describe these fixtures, not a statistical AI safety estimate.</p>"
            f"<p>Failed cases: {html.escape(', '.join(failed) or 'none')}</p>"
            f"<p>Suite fingerprint: <code>{result['suite_sha256']}</code></p></main></html>")
    (destination / "report.html").write_text(page, encoding="utf-8")
