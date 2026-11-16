"""Step 3. Cuts the reader out of the plain backdrop (Background Matting v2, on the CPU).
Output: my-book/work/reader_fg.mp4 (the reader on black) and reader_alpha.mp4 (the cutout shape).
Best result: also photograph the EMPTY backdrop from the same camera position and save it as my-book/empty_backdrop.jpg.
Without it, the script builds an empty backdrop from the video, which works when the backdrop is plain and evenly lit.
usage: .venv/bin/python scripts/3_cutout.py [--start S --end S]   (a short range is useful for a first test)"""
import subprocess, sys
import av, cv2, numpy as np, onnxruntime as ort
from PIL import Image, ImageOps
from common import *

arg = lambda k, d: float(sys.argv[sys.argv.index(k) + 1]) if k in sys.argv else d
R = reader(); W = ME / "work"; W.mkdir(exist_ok=True); model = KIT / "models/bgmv2.onnx"
if not model.exists(): stop("matting model not found at models/bgmv2.onnx (docs/03-cut-out-the-reader.md, step 1).")
t0, t1 = arg("--start", 0.0), arg("--end", duration(R)); small = W / "reader_small.mp4"
print("preparing the recording (upright, 960 px tall)...", flush=True)
run("ffmpeg", "-v", "error", "-y", "-ss", t0, "-i", R, "-t", t1 - t0, "-vf", "scale=-2:960:flags=lanczos,fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", small)
c = av.open(str(small)); n_total = c.streams.video[0].frames; it = c.decode(video=0); first = next(it).to_ndarray(format="rgb24"); h, w, _ = first.shape
ep = ME / "empty_backdrop.jpg"
if ep.exists():
    plate = np.asarray(ImageOps.exif_transpose(Image.open(ep)).convert("RGB").resize((w, h), Image.LANCZOS), np.float32); print("using my-book/empty_backdrop.jpg")
else:
    f0 = first.astype(np.float32)
    L = np.stack([np.convolve(np.median(f0[:, 4:40], 1)[:, k], np.ones(61) / 61, "same") for k in range(3)], 1); Rr = np.stack([np.convolve(np.median(f0[:, -40:-4], 1)[:, k], np.ones(61) / 61, "same") for k in range(3)], 1)
    for E in (L, Rr):
        E[:30], E[-30:] = E[30], E[-31]; ref = np.median(E[: int(h * 0.4)], 0); bad = np.abs(E - ref).sum(1) > 40
        for y in range(1, h):
            if bad[y]: E[y] = E[y - 1]
    t = np.linspace(0, 1, w)[None, :, None]; model_bg = L[:, None, :] * (1 - t) + Rr[:, None, :] * t
    person = (np.abs(f0 - model_bg).sum(-1) > 45).astype(np.uint8)
    person = cv2.dilate(cv2.morphologyEx(cv2.morphologyEx(person, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)), cv2.MORPH_CLOSE, np.ones((35, 35), np.uint8)), np.ones((41, 41), np.uint8))
    if person.mean() > 0.85: stop("could not tell the reader from the backdrop. Photograph the empty backdrop and save it as my-book/empty_backdrop.jpg, or re-record on a plain, evenly lit backdrop (docs/01).")
    soft = cv2.GaussianBlur(person.astype(np.float32), (0, 0), 6)[..., None]; plate = model_bg * soft + f0 * (1 - soft); print("no empty_backdrop.jpg: built one from the video")
Image.fromarray(plate.astype(np.uint8)).save(W / "cleanplate.png"); b = (plate / 255).transpose(2, 0, 1)[None].astype(np.float32)
sess = ort.InferenceSession(str(model), providers=["CPUExecutionProvider"])
enc = lambda name, pix: subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", pix, "-s", f"{w}x{h}", "-r", "30", "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p", str(W / name)], stdin=subprocess.PIPE)
fg, al = enc("reader_fg.mp4", "rgb24"), enc("reader_alpha.mp4", "gray"); prev = None; bb = [w, h, 0, 0]
def frames():
    yield first
    for f in it: yield f.to_ndarray(format="rgb24")
for i, f in enumerate(frames()):
    s = (f.astype(np.float32) / 255).transpose(2, 0, 1)[None]; pha, fgr = sess.run(["pha", "fgr"], {"src": s, "bgr": b})[:2]; a = pha[0, 0]
    if prev is not None: a = np.where(np.abs(a - prev) < 0.08, 0.5 * a + 0.5 * prev, a)
    prev = a; fg.stdin.write((np.clip(fgr[0].transpose(1, 2, 0) * a[..., None], 0, 1) * 255).astype(np.uint8).tobytes()); al.stdin.write((a * 255).astype(np.uint8).tobytes())
    if i % 10 == 0:                                   # remember where the reader is, so the video step can crop the empty space away
        ys, xs = np.nonzero(a > 0.5)
        if len(xs): bb = [min(bb[0], xs.min()), min(bb[1], ys.min()), max(bb[2], xs.max()), max(bb[3], ys.max())]
    if i % 150 == 0: print(f"frame {i} of about {n_total}", flush=True)
for p in (fg, al): p.stdin.close(); p.wait()
import json; json.dump({"start": t0, "end": t1, "box": [int(v) for v in bb], "size": [w, h]}, open(W / "cutout.json", "w"))
print("done. Look at my-book/work/reader_fg.mp4: the reader on black, with clean edges and a solid book. Next: docs/04-make-the-video.md")
