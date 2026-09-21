#!/usr/bin/env python3
"""Build a self-contained offline HTML slide deck from JSON."""
import html
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: generate_html.py INPUT.json OUTPUT.html", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    data = json.loads(source.read_text(encoding="utf-8"))
    title = html.escape(str(data.get("title", "Presentación")))
    subtitle = html.escape(str(data.get("subtitle", "")))
    slides = data.get("slides", [])
    if not 1 <= len(slides) <= 8:
        raise ValueError("slides must contain between 1 and 8 items")
    rendered = []
    for index, slide in enumerate(slides):
        heading = html.escape(str(slide.get("title", f"Diapositiva {index + 1}")))
        bullets = "".join(f"<li>{html.escape(str(item))}</li>" for item in slide.get("bullets", []))
        rendered.append(f'<section class="slide" aria-label="Diapositiva {index + 1}"><p class="kicker">{index + 1:02d}</p><h2>{heading}</h2><ul>{bullets}</ul></section>')
    deck = "\n".join(rendered)
    document = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#101827;--ink:#f7fafc;--muted:#a9b8cc;--accent:#4fd1c5}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,Segoe UI,sans-serif}}
.deck{{min-height:100vh;display:grid;place-items:center;padding:5vw}} .slide{{display:none;max-width:1000px;width:100%;min-height:62vh;padding:7vw;border:1px solid #2d405b;border-radius:28px;background:linear-gradient(135deg,#17243a,#111a2c);box-shadow:0 20px 70px #0008}} .slide.active{{display:block}} .kicker{{color:var(--accent);font-weight:800;letter-spacing:.2em}} h1{{font-size:clamp(2.5rem,7vw,6rem);margin:.2em 0 .1em;line-height:1.02}} h2{{font-size:clamp(2rem,5vw,4.5rem);margin:.3em 0 .5em;line-height:1.05}} p{{color:var(--muted);font-size:clamp(1.05rem,2vw,1.5rem)}} ul{{padding-left:1.2em;color:#dce7f5;font-size:clamp(1.1rem,2.5vw,2rem);line-height:1.6}} .cover{{display:block}} .counter{{position:fixed;right:3vw;bottom:2vw;color:var(--muted);font-variant-numeric:tabular-nums}}
</style></head><body><main class="deck"><section class="slide active cover"><p class="kicker">PRESENTACIÓN</p><h1>{title}</h1><p>{subtitle}</p></section>{deck}</main><div class="counter" id="counter"></div><script>
const slides=[...document.querySelectorAll('.slide')], counter=document.getElementById('counter'); let current=0;
function show(n){{current=Math.max(0,Math.min(n,slides.length-1));slides.forEach((s,i)=>s.classList.toggle('active',i===current));counter.textContent=`${{current+1}} / ${{slides.length}}`;}}
addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key))show(current+1);if(['ArrowLeft','PageUp'].includes(e.key))show(current-1);if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);}}); show(0);
</script></body></html>'''
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document, encoding="utf-8")
    print(f"created {target} ({len(document.encode('utf-8'))} bytes, {len(slides)+1} slides)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
