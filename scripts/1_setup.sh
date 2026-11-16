#!/bin/bash
# Step 1. Checks your computer and creates your private my-book/ folder. Safe to run again.
KIT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$KIT"; ok=1
say() { printf "%-22s %s\n" "$1" "$2"; }
[ "$(uname -s)" = Darwin ] && [ "$(uname -m)" = arm64 ] && say "Apple Silicon Mac" "yes" || say "Apple Silicon Mac" "NO - the speech step (2) uses a Mac-only tool; tested only on Apple Silicon"
command -v ffmpeg >/dev/null && say "ffmpeg" "found" || { say "ffmpeg" "MISSING - install with: brew install ffmpeg"; ok=0; }
command -v python3 >/dev/null && say "python3" "$(python3 -V 2>&1)" || { say "python3" "MISSING - install Python 3.11 or newer"; ok=0; }
[ $ok = 1 ] || { echo; echo "Fix the MISSING items above, then run this again."; exit 1; }
[ -d .venv ] || { echo "creating .venv (a private Python for this kit)..."; python3 -m venv .venv; }
.venv/bin/pip install -q --upgrade pip && .venv/bin/pip install -q pyyaml numpy pillow av onnxruntime opencv-python "mlx-whisper; platform_machine=='arm64'" || { echo "STOP: installing Python packages failed"; exit 1; }
mkdir -p my-book/pages my-book/work; [ -f my-book/book.yaml ] || cp book.example.yaml my-book/book.yaml
[ -f models/bgmv2.onnx ] && say "matting model" "found" || say "matting model" "not yet - docs/03-cut-out-the-reader.md, step 1"
echo; echo "Setup is fine. Next: docs/00-before-you-start.md, then record (docs/01) and put"
echo "  the recording at  my-book/reader.mp4   and the page pictures in  my-book/pages/01.jpg, 02.jpg, ..."
