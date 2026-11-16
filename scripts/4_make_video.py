"""Step 4. Builds the read-aloud video: page art behind, the reader in the corner, read-along words that light up as they are spoken.
usage: .venv/bin/python scripts/4_make_video.py                       the whole 16:9 video -> my-book/final.mp4
       .venv/bin/python scripts/4_make_video.py --start 60 --end 80   a 20-second preview -> my-book/preview.mp4
       .venv/bin/python scripts/4_make_video.py --short 138 154 dog   a 9:16 Short of that range -> my-book/short_dog.mp4"""
import json, re, subprocess, sys
import av, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
from common import *

C = cfg(); R = reader(); Wk = ME / "work"; a = sys.argv
for f in ("words.json", "pages.json", "reader_fg.mp4", "reader_alpha.mp4", "cutout.json"):
    if not (Wk / f).exists(): stop(f"my-book/work/{f} is missing. Do the earlier steps first (docs/02 and docs/03).")
words, pages = json.load(open(Wk / "words.json")), json.load(open(Wk / "pages.json")); CUT = json.load(open(Wk / "cutout.json")); c0, c1 = CUT["start"], CUT["end"]
short = "--short" in a
if short: t0, t1, name = float(a[a.index("--short") + 1]), float(a[a.index("--short") + 2]), a[a.index("--short") + 3]; out = ME / f"short_{name}.mp4"; W, H = 1080, 1920
else: t0 = float(a[a.index("--start") + 1]) if "--start" in a else c0; t1 = float(a[a.index("--end") + 1]) if "--end" in a else c1; out = ME / ("preview.mp4" if "--start" in a or "--end" in a else "final.mp4"); W, H = 1920, 1080
if t0 < c0 - 0.05 or t1 > c1 + 0.05: stop(f"the cutout only covers {c0:.0f} to {c1:.0f} seconds. Run step 3 for the range you want.")
rd, cp = C.get("reader", {}), C.get("captions", {}); side = rd.get("side", "right"); FPS = 30
fix = {k.lower(): v for k, v in (cp.get("fix") or {}).items()}; show = lambda w: fix.get(re.sub(r"[^a-z0-9']", "", w.lower()), w)
font = next((p for p in ("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") if Path(p).exists()), None)
if cp.get("enabled", True) and not font: stop("no bold font found for the read-along words. Set captions -> enabled: false in book.yaml.")
# --- page area and reader area
if short: PX, PY, PW, PH = 0, 0, W, int(H * 0.40); RH = int(H * 0.49); CAPBOX = (60, PH + 16, W - 60, PH + 196)   # page on top, words in the middle, reader below
else: PX, PY, PW, PH = 0, 0, W, H; RH = int(H * float(rd.get("height", 0.62))); CAPBOX = ((60, H - 250, int(W * 0.62), H - 50) if side == "right" else (int(W * 0.38), H - 250, W - 60, H - 50))
art = {}
def page_at(t):
    p = next((p for p in pages if p["start"] <= t < p["end"]), pages[-1])
    if p["image"] not in art:
        im = ImageOps.exif_transpose(Image.open(ME / "pages" / p["image"])).convert("RGB"); m = 1 + float(C.get("page_motion", 0.06)); s = max(PW * m / im.width, PH * m / im.height)
        art[p["image"]] = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    im = art[p["image"]]; u = min(1.0, max(0.0, (t - p["start"]) / max(1e-3, p["end"] - p["start"]))); u = u * u * (3 - 2 * u)
    x = round((im.width - PW) * u); y = round((im.height - PH) * (1 - u) * 0.5)
    return im.crop((x, y, x + PW, y + PH))
# --- caption cards: a few words each, breaking at sentence ends
cards, cur = [], []
for w in words:
    cur.append(w)
    if len(cur) >= int(cp.get("words_per_card", 6)) or w["w"][-1:] in ".?!": cards.append(cur); cur = []
if cur: cards.append(cur)
F = ImageFont.truetype(font, 58 if not short else 64) if font else None
def draw_card(img, t):
    card = next((c for c in cards if c[0]["s"] - 0.15 <= t < c[-1]["e"] + 0.35), None)
    if not card: return
    now = next((w for w in reversed(card) if w["s"] - 0.05 <= t), None)      # one highlighted word at a time: the latest one that has started
    d = ImageDraw.Draw(img, "RGBA"); x0, y0, x1, y1 = CAPBOX; sp = d.textlength(" ", font=F); lines, line, lw = [], [], 0
    for w in card:
        tw_ = d.textlength(show(w["w"]), font=F)
        if line and lw + sp + tw_ > x1 - x0 - 60: lines.append(line); line, lw = [], 0
        line.append((w, tw_)); lw += tw_ + (sp if len(line) > 1 else 0)
    lines.append(line); lh = F.size + 18; bh = lh * len(lines) + 44; by = y1 - bh
    d.rounded_rectangle([x0, by, x1, y1], radius=28, fill=(255, 250, 235, 235), outline=(40, 44, 90, 255), width=4)
    for k, ln in enumerate(lines):
        x = x0 + (x1 - x0 - sum(tw_ for _, tw_ in ln) - sp * (len(ln) - 1)) / 2; y = by + 22 + k * lh
        for w, tw_ in ln:
            if w is now: d.rounded_rectangle([x - 8, y - 2, x + tw_ + 8, y + F.size + 10], radius=12, fill=(255, 205, 60, 255))
            d.text((x, y), show(w["w"]), font=F, fill=(40, 44, 90, 255)); x += tw_ + sp
# --- render
fgc, alc = av.open(str(Wk / "reader_fg.mp4")), av.open(str(Wk / "reader_alpha.mp4")); skip = round((t0 - c0) * FPS); n = round((t1 - t0) * FPS)
tmp = out.with_suffix(".video.mp4")
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(tmp)], stdin=subprocess.PIPE)
bx0, by0, bx1, by1 = CUT["box"]; sw, sh_ = CUT["size"]; m = int(sh_ * 0.03)     # crop to where the reader actually is, plus a small margin
BOX = (max(0, bx0 - m), max(0, by0 - m), min(sw, bx1 + m), sh_ if by1 > sh_ * 0.93 else min(sh_, by1 + m))
for i, (ffr, afr) in enumerate(zip(fgc.decode(video=0), alc.decode(video=0))):
    if i < skip: continue
    k = i - skip
    if k >= n: break
    t = t0 + k / FPS; canvas = Image.new("RGB", (W, H), (18, 20, 34)); canvas.paste(page_at(t), (PX, PY))
    fg, al = ffr.to_image().convert("RGB"), afr.to_image().convert("L"); fg, al = fg.crop(BOX), al.crop(BOX)
    rw = round(fg.width * RH / fg.height); fg, al = fg.resize((rw, RH), Image.BILINEAR), al.resize((rw, RH), Image.BILINEAR)
    x = (W - rw) // 2 if short else (W - rw - 40 if side == "right" else 40); y = H - RH
    base = np.asarray(canvas, np.float32); A = np.asarray(al, np.float32)[..., None] / 255; reg = base[y:y + RH, max(0, x):x + rw]; sx = max(0, -x)
    reg[:] = np.asarray(fg, np.float32)[:, sx:sx + reg.shape[1]] + reg * (1 - A[:, sx:sx + reg.shape[1]]); canvas = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    if cp.get("enabled", True): draw_card(canvas, t)
    ff.stdin.write(canvas.tobytes())
    if k % 150 == 0: print(f"{k // FPS} of {n // FPS} seconds", flush=True)
ff.stdin.close(); ff.wait()
run("ffmpeg", "-v", "error", "-y", "-i", tmp, "-ss", t0, "-t", t1 - t0, "-i", R, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out); tmp.unlink()
print("wrote", out, f"({duration(out):.1f} s). Watch it all the way through, with sound, before you post it.")
