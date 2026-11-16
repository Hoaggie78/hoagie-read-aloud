"""Step 2. Listens to the recording, writes down every word with its time, and finds where each page starts.
Output: my-book/work/words.json, my-book/work/TRANSCRIPT.txt (read this), my-book/work/pages.json.
usage: .venv/bin/python scripts/2_listen.py"""
import json, re
from common import *

C = cfg(); R = reader(); W = ME / "work"; W.mkdir(exist_ok=True)
if not (W / "words.json").exists():
    import mlx_whisper
    print("listening to the recording (about 1 minute per 10 minutes of video)...", flush=True)
    wav = W / "audio16k.wav"; run("ffmpeg", "-v", "error", "-y", "-i", R, "-vn", "-ac", "1", "-ar", "16000", wav)
    r = mlx_whisper.transcribe(str(wav), path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en", word_timestamps=True)
    words = [{"w": x["word"].strip(), "s": round(float(x["start"]), 2), "e": round(float(x["end"]), 2)} for s in r["segments"] for x in s["words"] if x["word"].strip()]
    json.dump(words, open(W / "words.json", "w")); wav.unlink()
words = json.load(open(W / "words.json")); total = duration(R)
lines, cur = [], []
for w in words:
    cur.append(w)
    if w["w"][-1:] in ".?!" or len(cur) >= 14: lines.append(cur); cur = []
if cur: lines.append(cur)
(W / "TRANSCRIPT.txt").write_text("\n".join(f"{int(l[0]['s']) // 60}:{l[0]['s'] % 60:04.1f}  " + " ".join(x["w"] for x in l) for l in lines) + "\n")
n = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower().replace("’", "'").replace("'", "")).split()
flat = [n(w["w"])[0] if n(w["w"]) else "" for w in words]; pages = []; pos = 0; problems = []
for k, p in enumerate(C["pages"]):
    if not (ME / "pages" / p["image"]).exists(): problems.append(f"page {k + 1}: picture my-book/pages/{p['image']} not found")
    want = n(str(p.get("starts_with") or ""))
    if k == 0 and not want: pages.append({"image": p["image"], "start": 0.0}); continue
    if not want: problems.append(f"page {k + 1} ({p['image']}): starts_with is empty"); continue
    hit = next((i for i in range(pos, len(flat) - len(want) + 1) if flat[i:i + len(want)] == want), None)
    if hit is None: problems.append(f"page {k + 1} ({p['image']}): could not find \"{p['starts_with']}\" after {int(words[pos]['s']) // 60}:{words[pos]['s'] % 60:04.1f}. Copy the words from work/TRANSCRIPT.txt exactly as written there."); continue
    pages.append({"image": p["image"], "start": max(0.0, words[hit]["s"] - 0.25)}); pos = hit + len(want)
if problems: print("\nwords.json and TRANSCRIPT.txt are written. Fix these in my-book/book.yaml and run this step again:\n - " + "\n - ".join(problems)); raise SystemExit(1)
for a, b in zip(pages, pages[1:] + [{"start": total}]): a["end"] = round(b["start"], 2)
json.dump(pages, open(W / "pages.json", "w"), indent=1)
print(f"{len(words)} words, {total / 60:.1f} minutes. Page turns found:")
for p in pages: print(f"  {p['image']:<12} {int(p['start']) // 60}:{p['start'] % 60:04.1f} to {int(p['end']) // 60}:{p['end'] % 60:04.1f}  ({p['end'] - p['start']:.0f} s)")
print("\nRead my-book/work/TRANSCRIPT.txt once: misheard names can be corrected under captions -> fix in book.yaml.\nNext: docs/03-cut-out-the-reader.md")
