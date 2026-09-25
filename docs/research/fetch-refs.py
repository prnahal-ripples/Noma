#!/usr/bin/env python3
"""
Pipeline for turning Mobbin MCP results into the reference captures used by build-refs.py.

  1. python3 fetch-refs.py add   <key> <pos:shorturl> ...   # record + download a flow's screens
  2. python3 fetch-refs.py sheet <key>                      # build a numbered montage to identify positions
  3. python3 fetch-refs.py bind  <slug>=<key>:<pos> ...      # copy chosen screens to refs/<slug>.png
  4. python3 fetch-refs.py status

Raw downloads live in refs/_raw/<key>/<pos>.webp and are kept, so re-binding never re-downloads.
"""
import json, pathlib, subprocess, sys
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
REFS = HERE / "refs"
RAW  = REFS / "_raw"
IDX  = RAW / "_index.json"
RAW.mkdir(parents=True, exist_ok=True)

def load(): return json.loads(IDX.read_text()) if IDX.exists() else {}
def save(d): IDX.write_text(json.dumps(d, indent=1, sort_keys=True))

def cmd_add(args):
    key, pairs = args[0], args[1:]
    idx = load(); idx.setdefault(key, {})
    d = RAW / key; d.mkdir(parents=True, exist_ok=True)
    got = 0
    for p in pairs:
        pos, short = p.split(":", 1)
        out = d / f"{int(pos):02d}.webp"
        idx[key][str(int(pos))] = short
        if out.exists() and out.stat().st_size > 2000:
            continue
        url = short if short.startswith("http") else f"https://mobbin.com/api/mcp/short/{short}"
        r = subprocess.run(["curl", "-sL", "-m", "40", "-o", str(out), url], capture_output=True)
        if out.exists() and out.stat().st_size > 2000:
            got += 1
        else:
            out.unlink(missing_ok=True)
            print(f"  ! failed pos {pos}")
    save(idx)
    have = len(list(d.glob("*.webp")))
    print(f"{key}: downloaded {got} new, {have} on disk")

def cmd_sheet(args):
    keys = args
    tiles, labels = [], []
    for key in keys:
        for f in sorted((RAW / key).glob("*.webp")):
            tiles.append(f); labels.append(f"{key}:{int(f.stem)}")
    if not tiles:
        print("no tiles"); return
    TW, TH, PAD, LBL = 150, 325, 6, 16
    cols = 11
    rows = (len(tiles) + cols - 1) // cols
    W = cols * (TW + PAD) + PAD
    H = rows * (TH + LBL + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (28, 28, 28))
    dr = ImageDraw.Draw(sheet)
    for i, (f, lab) in enumerate(zip(tiles, labels)):
        c, r = i % cols, i // cols
        x = PAD + c * (TW + PAD); y = PAD + r * (TH + LBL + PAD)
        im = Image.open(f).convert("RGB")
        im.thumbnail((TW, TH))
        sheet.paste(im, (x + (TW - im.width) // 2, y + LBL))
        dr.text((x + 2, y + 2), lab, fill=(180, 230, 160))
    out = RAW / ("_sheet_" + "_".join(keys)[:60] + ".png")
    sheet.save(out)
    print(f"{out}  ({len(tiles)} screens, {cols}x{rows})")

def cmd_bind(args):
    n = 0
    for a in args:
        slug, src = a.split("=", 1)
        key, pos = src.split(":", 1)
        srcf = RAW / key / f"{int(pos):02d}.webp"
        if not srcf.exists():
            print(f"  ! missing {srcf}"); continue
        Image.open(srcf).convert("RGB").save(REFS / f"{slug}.png")
        n += 1
    print(f"bound {n} captures")

def cmd_status(args):
    m = json.loads((HERE / "refs-map.json").read_text())
    have = [r for r in m["refs"] if (REFS / f"{r['slug']}.png").exists()]
    miss = [r for r in m["refs"] if not (REFS / f"{r['slug']}.png").exists()]
    print(f"bound {len(have)}/{len(m['refs'])}")
    if miss:
        print("missing:")
        for r in miss:
            print(f"  {r['stage']} {r['slug']:22s} {r['app']} / {r['flow']} > {r['screen']}")

{"add": cmd_add, "sheet": cmd_sheet, "bind": cmd_bind, "status": cmd_status}[sys.argv[1]](sys.argv[2:])
