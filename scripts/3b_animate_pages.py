"""Optional step. Brings chosen pages to life with the LTX video model on your Mac (image-to-video).
For each page in book.yaml that has an `animate:` line, renders a 4-second moving version to my-book/anims/<page>.mp4.
Step 4 then plays it forwards and backwards behind the reader for as long as that page is on screen.
Pages without `animate:` keep the slow drift. Needs the ltx-2-mlx renderer (docs/05-animate-the-pages.md).
usage: .venv/bin/python scripts/3b_animate_pages.py [--dry-run] [--only 03.jpg]"""
import os, subprocess, sys, time
from common import *

C = cfg(); OUT = ME / "anims"; OUT.mkdir(exist_ok=True); DRY = "--dry-run" in sys.argv; only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
env = {}
if (KIT / ".env").exists():
    for l in (KIT / ".env").read_text().splitlines():
        if "=" in l and not l.startswith("#"): k, v = l.split("=", 1); env[k.strip()] = v.strip()
X = env.get("LTX_MLX_DIR") or os.environ.get("LTX_MLX_DIR", "")
todo = [p for p in C["pages"] if p.get("animate") and (not only or p["image"] == only)]
if not todo: stop("no page in my-book/book.yaml has an `animate:` line yet (docs/05-animate-the-pages.md, step 2).")
if not DRY:
    if not X or not Path(X, ".venv/bin/ltx-2-mlx").exists(): stop("set LTX_MLX_DIR in the kit's .env file to your ltx-2-mlx folder (docs/05, step 1).")
    W = next(iter(sorted(Path(X, "weights").glob("ltx-2.5-mlx-q8*"))), None)
    if not W: stop(f"the LTX-2.5 MLX model files are not in {X}/weights (docs/05, step 1).")
STYLE = "gentle storybook animation, soft natural motion, the drawing style, characters and colours stay exactly as in the picture, static camera, no new objects, no text"
for n, p in enumerate(todo, 1):
    img = ME / "pages" / p["image"]; out = OUT / (Path(p["image"]).stem + ".mp4"); prompt = f"{p['animate']}, {STYLE}"
    if not img.exists(): stop(f"picture my-book/pages/{p['image']} not found")
    if DRY: print(f"{p['image']}: {prompt}"); continue
    if out.exists(): print(f"{p['image']}: already animated, skipping (delete my-book/anims/{out.name} to redo it)"); continue
    t0 = time.time(); print(f"{p['image']}: rendering 4 seconds ({n} of {len(todo)})...", flush=True)
    r = subprocess.run([f"{X}/.venv/bin/ltx-2-mlx", "generate", "--distilled", "--low-ram", "--model", str(W), "--image", str(img), "0", "1.0", "--prompt", prompt,
                        "--width", "1216", "--height", "704", "--frames", "97", "--frame-rate", "24", "--seed", str(42 + n), "-o", str(out)], cwd=X, capture_output=True, text=True)
    if r.returncode or not out.exists(): print(f"{p['image']}: the renderer failed:\n{(r.stderr or r.stdout)[-500:]}"); continue
    print(f"{p['image']}: done in {(time.time() - t0) / 60:.0f} min -> my-book/anims/{out.name}", flush=True)
if not DRY: print("\nNow WATCH every file in my-book/anims/. If a character changes shape, melts or disappears, delete that file: the page will use the slow drift instead.")
