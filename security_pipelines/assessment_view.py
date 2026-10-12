"""A printable high-level view with native SVG diagrams; no external assets."""

from html import escape


def render(result: dict, entries: list[dict]) -> str:
    run = result["runs"]["governed"]
    links = "".join(f"<li><a href='{escape(entry['file'], quote=True)}'>"
                    f"{escape(entry['title'])}</a></li>" for entry in entries)
    bars = "".join(f"<g transform='translate(0,{index*86})'><rect width='420' height='60' rx='8' "
                   f"fill='{color}'/><text x='20' y='36' fill='white'>{label}</text></g>"
                   for index, (label, color) in enumerate([
                       ("01 · Proposed tool call (untrusted)", "#334155"),
                       ("02 · Contract and authorization boundary", "#2563eb"),
                       ("03 · Allow / deny decision (no execution)", "#334155"),
                       ("04 · Replay evidence and review pack", "#2563eb")]))
    arrows = "".join(f"<path d='M210 {y} v20' stroke='#64748b' stroke-width='3' "
                     "marker-end='url(#arrow)'/>" for y in (60, 146, 232))
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>AI security evaluation assessment pack</title><style>"
            "*{box-sizing:border-box}body{margin:0;background:#f3f6fb;color:#172439;font:17px system-ui}"
            "main{max-width:1120px;margin:auto;padding:50px 24px}h1{font-size:clamp(30px,5vw,52px);max-width:850px}"
            "p{line-height:1.7}section{background:white;border:1px solid #d6e0ec;padding:28px;margin:24px 0}"
            ".split{display:grid;grid-template-columns:1fr 1fr;gap:36px}svg{width:100%;height:auto}"
            "a{color:#1558bd}li{margin:14px 0}code{overflow-wrap:anywhere;font-size:13px}"
            ".state{display:inline-block;background:#e6efff;padding:8px 16px;color:#1448a5}"
            "@media(max-width:700px){.split{grid-template-columns:1fr}main{padding:24px 16px}}"
            "@media print{body{background:white}main{padding:0}section{break-inside:avoid}a{color:black}}"
            "</style></head><body><main><p>Rahul Chamoli · KaizenxRyu · Security pipelines</p>"
            "<h1>AI security evaluation and assessment pack</h1>"
            f"<p class='state'>Offline evaluation: {escape(result['verdict'])}</p> "
            "<p class='state'>Production: NOT ASSESSED</p><section class='split'><div>"
            "<h2>What this run established</h2>"
            f"<p>{result['case_count']} identical paired fixtures. "
            f"{run['forbidden_allowed']}/{run['forbidden_total']} forbidden calls allowed; "
            f"{run['legitimate_blocked']}/{run['legitimate_total']} legitimate calls blocked.</p>"
            "<p>Synthetic policy decisions only. No language model, real tool calls, customer data or network. "
            "This pack supports review; it is not a company compliance certificate.</p>"
            "<p>Model behavior, privacy, performance and real-system security: NOT RUN. "
            "Reviewer sign-off: PENDING.</p></div>"
            "<svg role='img' aria-label='Four-stage offline evaluation flow' viewBox='0 0 420 324'>"
            "<defs><marker id='arrow' markerWidth='8' markerHeight='8' refX='4' refY='4' orient='auto'>"
            "<path d='M0 0 L8 4 L0 8' fill='#64748b'/></marker></defs>"
            + bars + arrows + "</svg></section><section class='split'><div>"
            "<h2>Assessment documents</h2><ol>" + links + "</ol></div><div>"
            "<h2>Before a company release</h2><p>Define the actual system, models, data, permissions and "
            "business risks. Approve measurable requirements. Run real-model tests, fix findings, "
            "and record a human release decision.</p><p>The generated documents identify these gaps instead "
            "of marking unperformed evaluations as passed.</p><p>Use browser Print → Save as PDF for this "
            "overview. Markdown documents remain editable; manifest.json records document hashes.</p>"
            "<p><a href='../report.html'>Detailed evaluation results</a> · "
            "<a href='manifest.json'>Evidence manifest</a></p></div></section>"
            f"<p>Run UTC: {escape(result['timestamp_utc'])}</p>"
            f"<p>Suite SHA-256: <code>{escape(result['suite_sha256'])}</code></p></main></body></html>")
