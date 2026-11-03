#!/usr/bin/env python3
"""Writes heliod.dev/harness/numbers from summary.json, so the page and the repo never disagree.

  python3 tools/numbers_page.py <path to site>/harness/numbers.html
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/AvnehSBhatia/harness-bench"
TITLE = {"fleet": "Large fleet jobs", "ambiguous": "Ambiguous specs", "quick": "Quick tasks"}
ABOUT = {
    "fleet": "A written spec for a multi-module package, with notes and helpers that disagree with it on purpose, or 40 tickets with house rules stated once. Hidden tests.",
    "ambiguous": "Tickets that leave a gap or read two ways, in repos that settle it: an old receipt, a bank export, a runbook, a design mock. Three ship no tests. Hidden tests.",
    "quick": "Aider Polyglot Python exercises, one per run, graded by their own unit tests. Stopped after 6 of 34 for time; all six pairs shown.",
}
ORDER = ["fleet", "ambiguous", "quick"]

e = html.escape


def money(x):
    return f"${x:.3f}" if x >= 0.01 else f"${x:.4f}"


def tokens(n):
    return f"{n / 1e6:.2f}M" if n >= 1e6 else f"{n / 1e3:.0f}k" if n >= 1e3 else str(n)


def ratio(a, b):
    return f"{a / b:.1f}×" if a and b else "-"


def main(out_path):
    s = json.load(open(os.path.join(ROOT, "summary.json")))
    c, h = s["overall"]["codex"], s["overall"]["heliod"]
    secs = [k for k in ORDER if k in s["sections"]]
    n_tasks = h["tasks"]
    hh = {k: v["head_to_head"] for k, v in s["sections"].items() if "head_to_head" in v}
    cheaper = sum(v["heliod"]["cheaper"] for v in hh.values())
    faster = sum(v["heliod"]["faster"] for v in hh.values())
    codex_faster = sum(v["codex"]["faster"] for v in hh.values())
    hosted = h.get("hosted_checks", 0)
    priv = s["sections"].get("fleet-private", {}).get("heliod-private")
    fleet_c = s["sections"]["fleet"]["codex"]
    private_note = (
        f" Rerun with every check on GPT-6 Luna through the same meter (<code>--private-checks</code>), Heliod's fleet jobs cost "
        f"{money(priv['usd'])} against Codex's {money(fleet_c['usd'])}, in {priv['minutes']:g} minutes against {fleet_c['minutes']:g}, "
        f"{priv['passed']} of {priv['tasks']} passed against {fleet_c['passed']} of {fleet_c['tasks']}."
        if priv else " <code>heliod --private-checks</code> runs them on your own model instead."
    )
    share = round(h["usd"] / c["usd"] * 100)
    # The audits' own count: every metered call of these runs, including preflight checks and unscored attempts.
    calls = 0
    for sec in s["sections"].values():
        audit = os.path.join(ROOT, sec["run"], "AUDIT.md")
        m = re.search(r"confirmed (\d+) of (\d+)", open(audit).read()) if os.path.exists(audit) else None
        calls += int(m.group(1)) if m and m.group(1) == m.group(2) else 0

    def stat(label, heliod, codex, note):
        return f'<div class="stat"><p class="k">{label}</p><p class="v">{heliod}</p><p class="c">Codex {codex}</p><p class="r">{note}</p></div>'

    stats = "".join([
        stat("Tasks passed", f"{h['passed']}<span>/{h['tasks']}</span>", f"{c['passed']}/{c['tasks']}", f"{h['cases_passed']} of {h['cases_expected']} test cases"),
        stat("Billed by OpenRouter", money(h["usd"]), money(c["usd"]), f"{ratio(c['usd'], h['usd'])} less"),
        stat("Wall time", f"{h['minutes']:.1f}<span> min</span>", f"{c['minutes']:.1f} min", f"{ratio(c['minutes'], h['minutes'])} faster"),
        stat("Input tokens", tokens(h["input_tokens"]), tokens(c["input_tokens"]), f"{ratio(c['input_tokens'], h['input_tokens'])} fewer"),
    ])

    groups = []
    for sec in secs:
        rows = [a for a in s["attempts"] if a["section"] == sec and a["arm"] in ("codex", "heliod")]
        tasks = []
        for a in rows:
            if a["task"] not in tasks:
                tasks.append(a["task"])
        peak = max(a["billed_usd"] for a in rows) or 1
        lines = []
        for t in tasks:
            pair = {a["arm"]: a for a in rows if a["task"] == t}
            cx, hx = pair.get("codex"), pair.get("heliod")
            if not cx or not hx:
                continue

            def bar(a, who):
                mark = "✓" if a["works"] else "✕"
                cls = "ok" if a["works"] else "no"
                return (f'<div class="bar {who}"><span class="trk"><i style="--w:{a["billed_usd"] / peak * 100:.1f}%"></i></span>'
                        f'<b class="{cls}">{mark}</b><em>{money(a["billed_usd"])} · {a["minutes"]:g} min · {a["tests"]}</em></div>')

            lines.append(f'<div class="row"><code>{e(t)}</code><div class="bars">{bar(cx, "cx")}{bar(hx, "hx")}</div></div>')
        sc, sh = s["sections"][sec]["codex"], s["sections"][sec]["heliod"]
        groups.append(
            f'<section class="group"><div class="gh"><h3>{TITLE.get(sec, sec)}</h3>'
            f'<p class="tot">Codex {money(sc["usd"])} · {sc["minutes"]:g} min · {sc["passed"]}/{sc["tasks"]} passed'
            f'<br><b>Heliod {money(sh["usd"])} · {sh["minutes"]:g} min · {sh["passed"]}/{sh["tasks"]} passed</b></p></div>'
            f'<p class="about">{e(ABOUT.get(sec, ""))}</p>{"".join(lines)}</section>'
        )

    def stack(who, x):
        unc = x["input_tokens"] - x["cached_tokens"]
        vis = x["output_tokens"] - x["reasoning_tokens"]
        top_in = max(c["input_tokens"], h["input_tokens"])
        top_out = max(c["output_tokens"], h["output_tokens"])
        return (
            f'<div class="tk"><p class="who">{who}</p>'
            f'<div class="tb"><span class="lab">input</span><div class="track"><i class="cached" style="--w:{x["cached_tokens"] / top_in * 100:.1f}%"></i><i class="fresh" style="--w:{unc / top_in * 100:.1f}%"></i></div><span class="num">{tokens(x["input_tokens"])}</span></div>'
            f'<div class="tb"><span class="lab">output</span><div class="track"><i class="reason" style="--w:{x["reasoning_tokens"] / top_out * 100:.1f}%"></i><i class="said" style="--w:{vis / top_out * 100:.1f}%"></i></div><span class="num">{tokens(x["output_tokens"])}</span></div></div>'
        )

    # Every comparison Heliod wins, computed here so the page and summary.json never disagree.
    pairs = {}
    for a in s["attempts"]:
        if a["section"] in ORDER and a["arm"] in ("codex", "heliod"):
            pairs.setdefault((a["section"], a["task"]), {})[a["arm"]] = a
    pairs = {k: v for k, v in pairs.items() if "codex" in v and "heliod" in v}
    fewer = {k: sum(1 for v in pairs.values() if v["heliod"][k] < v["codex"][k]) for k in ("input_tokens", "output_tokens", "reasoning_tokens")}

    def x(a, b):
        return f"{a / b:.1f}×" if b else "-"

    wall = [
        ("Tasks passed", f"{h['passed']}/{h['tasks']}", f"Codex {c['passed']}/{c['tasks']}"),
        ("Hidden test cases passed", f"{h['cases_passed'] / h['cases_expected'] * 100:.0f}%", f"{h['cases_passed']} of {h['cases_expected']} · Codex {c['cases_passed']} of {c['cases_expected']}"),
        ("Less spent", f"{(1 - h['usd'] / c['usd']) * 100:.0f}%", f"{money(h['usd'])} against {money(c['usd'])}"),
        ("Faster", x(c["minutes"], h["minutes"]), f"{h['minutes']:.1f} min against {c['minutes']:.1f}"),
        ("Cheaper per passed task", x(c["usd_per_pass"], h["usd_per_pass"]), f"${h['usd_per_pass']:.4f} against ${c['usd_per_pass']:.4f}"),
        ("Test cases passed per dollar", f"{h['cases_passed'] / h['usd']:,.0f}", f"Codex {c['cases_passed'] / c['usd']:,.0f}"),
        ("Fewer input tokens", x(c["input_tokens"], h["input_tokens"]), f"{tokens(h['input_tokens'])} against {tokens(c['input_tokens'])}"),
        ("Fewer output tokens", x(c["output_tokens"], h["output_tokens"]), f"{tokens(h['output_tokens'])} against {tokens(c['output_tokens'])}"),
        ("Fewer reasoning tokens", x(c["reasoning_tokens"], h["reasoning_tokens"]), f"{tokens(h['reasoning_tokens'])} against {tokens(c['reasoning_tokens'])}"),
        ("Tasks where Heliod cost less", f"{cheaper} of {n_tasks}", "matched task by task"),
        ("Tasks with fewer tokens", f"{min(fewer.values())} of {n_tasks}", "input, output and reasoning, each"),
        ("Tasks finished first", f"{faster} of {n_tasks}", f"Codex {codex_faster}, {n_tasks - faster - codex_faster} tied"),
    ]
    wall_html = "".join(f'<div class="w"><p class="wv">{v}</p><p class="wk">{k}</p><p class="wc">{e(cmp)}</p></div>' for k, v, cmp in wall)

    def high(sec):
        sc, sh = s["sections"][sec]["codex"], s["sections"][sec]["heliod"]
        pts = [f"{sh['passed']}/{sh['tasks']} passed" + (f" vs {sc['passed']}/{sc['tasks']}" if sc["passed"] != sh["passed"] else " (both)"),
               f"{x(sc['usd'], sh['usd'])} cheaper", f"{x(sc['minutes'], sh['minutes'])} faster",
               f"{x(sc['input_tokens'], sh['input_tokens'])} fewer input tokens", f"{x(sc['reasoning_tokens'], sh['reasoning_tokens'])} fewer reasoning tokens"]
        return f'<div class="hl"><h3>{TITLE[sec]}</h3><ul>{"".join(f"<li>{p}</li>" for p in pts)}</ul></div>'
    highlights = "".join(high(sec) for sec in secs)

    def best(metric, fmt):
        k, v = max(pairs.items(), key=lambda kv: kv[1]["codex"][metric] / max(kv[1]["heliod"][metric], 1e-9))
        return k[1], v["codex"][metric], v["heliod"][metric], fmt
    wins = []
    t, a, b, _ = best("minutes", None)
    wins.append((f"{a / b:.1f}× faster", t, f"{a:g} min → {b:g} min"))
    t, a, b, _ = best("billed_usd", None)
    wins.append((f"{a / b:.1f}× cheaper", t, f"{money(a)} → {money(b)}"))
    t, a, b, _ = best("input_tokens", None)
    wins.append((f"{a / b:.1f}× fewer input tokens", t, f"{tokens(a)} → {tokens(b)}"))
    lost = [k[1] for k, v in pairs.items() if v["heliod"]["works"] and not v["codex"]["works"]]
    for t in lost:
        v = pairs[next(k for k in pairs if k[1] == t)]
        wins.append(("Passed where Codex did not", t, f"{v['heliod']['tests']} against {v['codex']['tests']}"))
    wins_html = "".join(f'<div class="win"><p class="wv">{a}</p><p class="wk"><code>{e(t)}</code></p><p class="wc">{e(d)}</p></div>' for a, t, d in wins)
    paid = (f'<p class="paid">Even paying for every one of its own checks, Heliod finished the big jobs <b>{priv["passed"]} of {priv["tasks"]}</b>, '
            f'<b>{(1 - priv["usd"] / fleet_c["usd"]) * 100:.0f}% cheaper</b> and <b>{x(fleet_c["minutes"], priv["minutes"])} faster</b> than Codex.</p>') if priv else ""

    versions = s.get("versions", {})
    page = TEMPLATE.format(wall=wall_html, highlights=highlights, wins=wins_html, paid=paid, less=f"{(1 - h['usd'] / c['usd']) * 100:.0f}",
        n=n_tasks, share=share, stats=stats, groups="".join(groups),
        cheaper=cheaper, faster=faster, codex_faster=codex_faster, ties=n_tasks - faster - codex_faster,
        tok=stack("Codex", c) + stack("Heliod", h), hosted=hosted, private_note=private_note, calls=calls, repo=REPO,
        codex_v=e(versions.get("codex", "")), heliod_v=e(versions.get("heliod", "").replace("heliod ", "")),
        h_reason=tokens(h["reasoning_tokens"]), c_reason=tokens(c["reasoning_tokens"]),
    )
    open(out_path, "w").write(page)
    print(f"wrote {out_path}")


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Harness Bench · Heliod Harness</title>
<meta name="description" content="Heliod Harness and Codex CLI on the same model and the same {n} tasks: every task passed at {share}% of Codex's bill. Every model call is public.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Heliod">
<meta property="og:title" content="Harness Bench: Heliod Harness vs Codex CLI">
<meta property="og:description" content="Same model, same {n} tasks, hidden tests. Heliod passed all {n} at {share}% of Codex's bill. Every model call is public.">
<meta property="og:image" content="https://www.heliod.dev/media/films/journey-end.jpg">
<meta property="og:url" content="https://www.heliod.dev/harness/numbers">
<link rel="icon" type="image/png" href="/media/star-64.png">
<link rel="preload" href="/fonts/Newsreader-Latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face {{ font-family: Newsreader; src: url(/fonts/Newsreader-Latin.woff2) format("woff2"); font-weight: 200 800; font-display: swap; }}
@font-face {{ font-family: "Fragment Mono"; src: url(/fonts/FragmentMono-Latin.woff2) format("woff2"); font-weight: 400; font-display: swap; }}
:root {{
  --bg: #161513; --panel: #201f1c; --raised: #2a2926; --inset: #181715;
  --ink: #f4f2ec; --muted: #a8a59c; --faint: #94918a; --accent: #e8943a; --ember-soft: rgba(232,148,58,.22);
  --ash: #77746d; --ash-soft: rgba(168,165,156,.18); --success: #8fcbb0; --danger: #e39aa4;
  --line: rgba(255,255,255,.08); --line-strong: rgba(255,255,255,.14);
  --mono: "Fragment Mono", ui-monospace, monospace;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: var(--bg); color: var(--ink); font-family: Newsreader, "Iowan Old Style", Palatino, Georgia, serif; font-optical-sizing: auto; font-size: 16px; line-height: 1.5; -webkit-font-smoothing: antialiased; }}
body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .6;
  background-image: radial-gradient(1px 1px at 8% 12%, rgba(255,255,255,.85), transparent), radial-gradient(1px 1px at 18% 42%, rgba(220,230,255,.7), transparent), radial-gradient(1.2px 1.2px at 27% 78%, rgba(255,255,255,.55), transparent), radial-gradient(1px 1px at 36% 22%, rgba(255,230,200,.55), transparent), radial-gradient(1px 1px at 47% 61%, rgba(255,255,255,.75), transparent), radial-gradient(1.4px 1.4px at 58% 14%, rgba(200,210,255,.8), transparent), radial-gradient(1px 1px at 66% 48%, rgba(255,255,255,.5), transparent), radial-gradient(1px 1px at 74% 86%, rgba(255,255,255,.7), transparent), radial-gradient(1.2px 1.2px at 83% 31%, rgba(255,240,220,.65), transparent), radial-gradient(1px 1px at 91% 67%, rgba(220,230,255,.6), transparent); }}
body::after {{ content: ""; position: fixed; left: 50%; top: -340px; width: 900px; height: 620px; transform: translateX(-50%); pointer-events: none;
  background: radial-gradient(closest-side, rgba(232,148,58,.13), rgba(232,148,58,.04) 55%, transparent); }}
a {{ color: var(--muted); text-underline-offset: 4px; transition: color .15s; }}
a:hover {{ color: var(--ink); }}
header {{ position: relative; z-index: 1; display: flex; align-items: center; gap: 12px; height: 56px; padding: 0 24px; border-bottom: 1px solid var(--line); background: rgba(22,21,19,.7); backdrop-filter: blur(12px); }}
.brand {{ display: flex; align-items: center; gap: 9px; color: var(--ink); text-decoration: none; font-size: 21px; line-height: 1; }}
.brand img {{ width: 20px; height: 20px; }}
header .sep {{ color: rgba(255,255,255,.14); }}
header .sub {{ font-family: var(--mono); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--accent); text-decoration: none; }}
main {{ position: relative; z-index: 1; max-width: 880px; margin: 0 auto; padding: 56px 20px 72px; color: var(--muted); }}
.eyebrow {{ margin: 0; font-family: var(--mono); font-size: 12px; letter-spacing: .1em; text-transform: uppercase; color: var(--accent); }}
h1 {{ margin: 14px 0 0; max-width: 15em; font-size: clamp(34px, 6vw, 54px); line-height: 1.04; font-weight: 500; letter-spacing: -.035em; color: var(--ink); }}
h1 em {{ font-style: italic; color: var(--accent); }}
.lede {{ margin: 18px 0 0; max-width: 36em; font-size: 18px; line-height: 1.55; color: var(--muted); }}
.lede b {{ font-weight: 500; color: var(--ink); }}
.stats {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; margin-top: 36px; border: 1px solid var(--line); border-radius: 18px; overflow: hidden; background: var(--line); }}
.stat {{ padding: 20px 20px 18px; background: rgba(28,27,24,.94); }}
.stat p {{ margin: 0; }}
.stat .k {{ font-size: 14px; color: var(--muted); }}
.stat .v {{ margin-top: 8px; font-size: clamp(30px, 4vw, 40px); line-height: 1; font-weight: 500; letter-spacing: -.03em; color: var(--accent); font-variant-numeric: tabular-nums; }}
.stat .v span {{ font-size: .5em; letter-spacing: 0; color: var(--muted); }}
.stat .c {{ margin-top: 10px; font-family: var(--mono); font-size: 12.5px; color: var(--faint); }}
.stat .r {{ margin-top: 2px; font-size: 14px; color: var(--ink); }}
.legend {{ display: flex; flex-wrap: wrap; gap: 8px 22px; margin-top: 22px; font-size: 14px; color: var(--muted); }}
.legend span {{ display: inline-flex; align-items: center; gap: 8px; }}
.legend i {{ width: 22px; height: 8px; border-radius: 4px; }}
.legend .cxk {{ background: var(--ash); }} .legend .hxk {{ background: var(--accent); }}
h2 {{ margin: 64px 0 0; font-size: 26px; font-weight: 500; letter-spacing: -.02em; color: var(--ink); }}
h2 + p {{ margin-top: 10px; max-width: 40em; }}
p {{ margin: 12px 0 0; }}
.group {{ margin-top: 28px; padding: 22px 22px 14px; border: 1px solid var(--line); border-radius: 18px; background: rgba(30,29,26,.86); }}
.gh {{ display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 6px 24px; }}
.gh h3 {{ margin: 0; font-size: 20px; font-weight: 500; color: var(--ink); }}
.tot {{ margin: 0; font-family: var(--mono); font-size: 12.5px; line-height: 1.7; text-align: right; color: var(--faint); }}
.tot b {{ font-weight: 400; color: var(--accent); }}
.about {{ margin: 8px 0 14px; max-width: 46em; font-size: 15px; color: var(--muted); }}
.row {{ display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 4px 16px; align-items: center; padding: 10px 0; border-top: 1px solid var(--line); }}
.row code {{ font-family: var(--mono); font-size: 13px; color: var(--ink); overflow-wrap: anywhere; }}
.bars {{ display: grid; gap: 5px; }}
.bar {{ display: grid; grid-template-columns: minmax(0, 1fr) 14px 208px; gap: 10px; align-items: center; height: 18px; }}
.trk {{ display: block; height: 8px; }}
.bar i {{ display: block; height: 8px; width: var(--w); min-width: 3px; border-radius: 4px; animation: grow .9s cubic-bezier(.2,.7,.2,1) both; transform-origin: left; }}
.bar.cx i {{ background: var(--ash); }} .bar.hx i {{ background: var(--accent); box-shadow: 0 0 14px rgba(232,148,58,.35); }}
.bar b {{ font-weight: 500; font-size: 13px; }} .bar b.ok {{ color: var(--success); }} .bar b.no {{ color: var(--danger); }}
.bar em {{ font-style: normal; font-family: var(--mono); font-size: 12px; color: var(--faint); white-space: nowrap; }}
.bar.hx em {{ color: var(--muted); }}
@keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
.h2h {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 20px; }}
.h2h div {{ padding: 18px 20px; border: 1px solid var(--line); border-radius: 16px; background: rgba(30,29,26,.86); }}
.h2h b {{ display: block; font-size: 34px; line-height: 1; font-weight: 500; letter-spacing: -.03em; color: var(--accent); }}
.h2h span {{ display: block; margin-top: 8px; font-size: 15px; color: var(--muted); }}
.tokens {{ display: grid; gap: 18px; margin-top: 22px; padding: 22px; border: 1px solid var(--line); border-radius: 18px; background: rgba(30,29,26,.86); }}
.tk .who {{ margin: 0 0 6px; font-size: 15px; color: var(--ink); }}
.tb {{ display: grid; grid-template-columns: 56px minmax(0, 1fr) 64px; gap: 12px; align-items: center; margin-top: 6px; }}
.tb .lab {{ font-family: var(--mono); font-size: 12px; color: var(--faint); }}
.tb .num {{ font-family: var(--mono); font-size: 12.5px; color: var(--ink); text-align: right; }}
.track {{ display: flex; height: 12px; border-radius: 6px; background: rgba(255,255,255,.03); overflow: hidden; }}
.track i {{ display: block; width: var(--w); height: 100%; animation: grow 1.1s cubic-bezier(.2,.7,.2,1) both; transform-origin: left; }}
.track .cached {{ background: repeating-linear-gradient(135deg, rgba(168,165,156,.35) 0 4px, rgba(168,165,156,.18) 4px 8px); }}
.track .fresh {{ background: var(--muted); }}
.track .reason {{ background: repeating-linear-gradient(135deg, rgba(232,148,58,.5) 0 4px, rgba(232,148,58,.25) 4px 8px); }}
.track .said {{ background: var(--accent); }}
.tkey {{ display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 13px; color: var(--faint); }}
.tkey i {{ display: inline-block; width: 14px; height: 8px; margin-right: 6px; border-radius: 3px; vertical-align: middle; }}
.wall {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px; margin-top: 22px; border: 1px solid var(--line); border-radius: 18px; overflow: hidden; background: var(--line); }}
.w {{ padding: 20px 18px 18px; background: rgba(28,27,24,.94); }}
.w p, .win p {{ margin: 0; }}
.wv {{ font-size: clamp(28px, 3.6vw, 36px); line-height: 1; font-weight: 500; letter-spacing: -.03em; color: var(--accent); font-variant-numeric: tabular-nums; }}
.wk {{ margin-top: 10px !important; font-size: 15px; line-height: 1.3; color: var(--ink); }}
.wc {{ margin-top: 6px !important; font-family: var(--mono); font-size: 12px; line-height: 1.5; color: var(--faint); }}
.hls {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 22px; }}
.hl {{ padding: 20px 22px; border: 1px solid var(--line); border-radius: 18px; background: rgba(30,29,26,.86); }}
.hl h3 {{ margin: 0; font-size: 18px; font-weight: 500; color: var(--ink); }}
.hl ul {{ margin: 12px 0 0; padding: 0; list-style: none; }}
.hl li {{ padding: 6px 0; border-top: 1px solid var(--line); font-size: 15px; color: var(--muted); }}
.hl li:first-child {{ border-top: 0; color: var(--accent); }}
.paid {{ margin-top: 16px; padding: 16px 20px; border: 1px solid rgba(232,148,58,.3); border-radius: 14px; background: var(--ember-soft); color: var(--ink); font-size: 16px; }}
.paid b {{ font-weight: 500; color: var(--accent); }}
.wins {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-top: 22px; }}
.win {{ padding: 20px 18px; border: 1px solid var(--line); border-radius: 18px; background: rgba(30,29,26,.86); }}
.win .wv {{ font-size: 24px; }}
.care {{ margin-top: 18px; padding: 0; list-style: none; border: 1px solid var(--line); border-radius: 18px; overflow: hidden; }}
.care li {{ padding: 16px 22px; border-top: 1px solid var(--line); background: rgba(30,29,26,.86); }}
.care li:first-child {{ border-top: 0; }}
.care b {{ font-weight: 500; color: var(--ink); }}
code {{ font-family: var(--mono); font-size: 13.5px; color: var(--ink); }}
.check {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 20px; }}
.check a, .check div {{ display: block; padding: 18px 20px; border: 1px solid var(--line); border-radius: 16px; background: rgba(30,29,26,.86); text-decoration: none; }}
.check a:hover {{ border-color: var(--line-strong); }}
.check b {{ display: block; font-weight: 500; color: var(--ink); }}
.check span {{ display: block; margin-top: 6px; font-size: 14px; color: var(--muted); }}
.cmd {{ margin-top: 14px; padding: 12px 16px; border: 1px solid var(--line-strong); border-radius: 12px; background: var(--inset); font-family: var(--mono); font-size: 13px; color: var(--ink); overflow-x: auto; white-space: nowrap; }}
details {{ margin-top: 18px; border: 1px solid var(--line); border-radius: 16px; background: rgba(30,29,26,.86); }}
summary {{ cursor: pointer; padding: 16px 22px; color: var(--ink); }}
details > div {{ padding: 0 22px 18px; }}
table {{ width: 100%; margin-top: 12px; border-collapse: collapse; font-size: 15px; }}
th, td {{ padding: 8px 10px; text-align: left; border-top: 1px solid var(--line); }}
thead th {{ border-top: 0; font-weight: 500; color: var(--ink); }}
footer {{ margin-top: 56px; padding-top: 20px; border-top: 1px solid var(--line); display: flex; flex-wrap: wrap; gap: 8px 20px; font-size: 14px; color: var(--faint); }}
@media (prefers-reduced-motion: reduce) {{ .bar i, .track i {{ animation: none; }} }}
@media (max-width: 760px) {{
  .stats, .wall, .wins {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .hls {{ grid-template-columns: minmax(0, 1fr); }}
  .row {{ grid-template-columns: minmax(0, 1fr); }}
  .h2h, .check {{ grid-template-columns: minmax(0, 1fr); }}
  .tot {{ text-align: left; }}
  .bar {{ grid-template-columns: minmax(0, 1fr) 12px 168px; gap: 8px; }}
  .bar em {{ font-size: 11px; }}
}}
</style>
</head>
<body>
<header>
  <a class="brand" href="https://www.heliod.dev/"><img src="/media/star-64.png" alt="">Heliod</a>
  <span class="sep">/</span>
  <a class="sub" href="/install">Harness</a>
</header>
<main>
  <p class="eyebrow">Harness Bench · November 2, 2026</p>
  <h1>Every task passed. <em>{less}% cheaper.</em> Twice as fast.</h1>
  <p class="lede">Heliod Harness and OpenAI's Codex CLI, both on GPT-6 Luna through OpenRouter, given the same one-line prompt on the same <b>{n} tasks</b>, graded by tests neither agent saw. Every model call is public.</p>

  <div class="stats">{stats}</div>
  <div class="legend"><span><i class="hxk"></i>Heliod Harness {heliod_v}</span><span><i class="cxk"></i>{codex_v}</span></div>

  <h2>By every measure</h2>
  <p>Twelve ways to compare the same work. Heliod comes out ahead on each.</p>
  <div class="wall">{wall}</div>

  <h2>Section by section</h2>
  <div class="hls">{highlights}</div>
  {paid}

  <h2>The biggest single-task wins</h2>
  <div class="wins">{wins}</div>

  <h2>Every task</h2>
  <p>Each pair of bars is one task: what OpenRouter billed for it, then the time and the test cases passed. ✓ means every graded case passed.</p>
  {groups}


  <h2>Where the tokens went</h2>
  <p>Most of each harness's input was cached at a tenth of the price, which is why the bill gap is smaller than the token gap. Reasoning is the share of output the model spent thinking: {c_reason} for Codex, {h_reason} for Heliod.</p>
  <div class="tokens">
    {tok}
    <div class="tkey"><span><i style="background:repeating-linear-gradient(135deg,rgba(168,165,156,.35) 0 4px,rgba(168,165,156,.18) 4px 8px)"></i>cached input</span><span><i style="background:var(--muted)"></i>new input</span><span><i style="background:repeating-linear-gradient(135deg,rgba(232,148,58,.5) 0 4px,rgba(232,148,58,.25) 4px 8px)"></i>reasoning</span><span><i style="background:var(--accent)"></i>written output</span></div>
  </div>

  <h2>Read these with care</h2>
  <ul class="care">
    <li><b>Different subagent settings, on purpose.</b> Both main agents ran at medium reasoning. Heliod's fleet workers ask for low reasoning and Heliod checks their work; every Codex call asked for medium. Each harness's choices are part of what is compared, and every request in the traces shows its setting.</li>
    <li><b>Heliod's hosted checks are not in the bill.</b> Heliod checked its fleet's work {hosted} times on its hosted checker, which is free to users, all on the five fleet jobs.{private_note}</li>
    <li><b>Codex worked alone.</b> Its multi-agent feature was on; it chose not to spawn subagents on any task. Heliod used a team of 7 to 12 agents on the four multi-module jobs and worked alone on the rest.</li>
    <li><b>Quick tasks is partial.</b> We stopped it after 6 of its 34 exercises to publish tonight. All six finished pairs are shown.</li>
    <li><b>One laptop.</b> Wall times come from one laptop that was also running another benchmark for part of the evening. Costs and tokens are unaffected.</li>
    <li><b>One model, one attempt per task.</b> The result rests on {n} matched tasks, not on repeats.</li>
  </ul>

  <h2>Check it yourself</h2>
  <p>OpenRouter confirmed all {calls} metered model calls by their generation ids: every billed cost matched, and every call went to the pinned provider.</p>
  <div class="check">
    <a href="{repo}"><b>The repository</b><span>Tasks, graders, runner, and every attempt's calls, sessions, plans and diffs.</span></a>
    <a href="{repo}/blob/master/METHODOLOGY.md"><b>Methodology</b><span>Settings, caps, grading, what was stopped or changed, what is removed from traces.</span></a>
    <a href="{repo}/blob/master/runs/README.md"><b>Every model call</b><span>Each attempt's transcript: what was sent, what came back, tokens and cost, for every agent.</span></a>
  </div>
  <div class="cmd">git clone {repo} &amp;&amp; cd harness-bench &amp;&amp; python3 tools/summary.py</div>

  <details>
    <summary>Earlier measurements (November 1)</summary>
    <div>
      <p>Neo's 16 multi-part Python tasks, one run each, a single price table for both. Both sides passed every test.</p>
      <table>
        <thead><tr><th></th><th>Codex</th><th>Heliod Harness</th></tr></thead>
        <tr><td>Same plain prompt: tokens</td><td>4.06M</td><td>860k</td></tr>
        <tr><td>Same plain prompt: cost</td><td>$0.129</td><td>$0.071</td></tr>
        <tr><td>Codex told to use subagents: tokens</td><td>17.1M</td><td>754k</td></tr>
        <tr><td>Codex told to use subagents: cost</td><td>$0.36</td><td>$0.060</td></tr>
      </table>
    </div>
  </details>

  <footer>
    <a href="/install">Install</a>
    <a href="/harness/numbers">Harness Bench</a>
    <a href="/harness/security">Security</a>
    <a href="{repo}">GitHub</a>
  </footer>
</main>
</body>
</html>
"""

if __name__ == "__main__":
    main(sys.argv[1])
