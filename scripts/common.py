"""Shared helpers: paths, settings, simple checks."""
import subprocess, sys
from pathlib import Path
import yaml

KIT = Path(__file__).resolve().parent.parent; ME = KIT / "my-book"
def stop(m): sys.exit("\nSTOP: " + m + "\n")
def cfg():
    p = ME / "book.yaml"
    if not p.exists(): stop("my-book/book.yaml is missing. Run: bash scripts/1_setup.sh")
    return yaml.safe_load(open(p))
def reader():
    for n in ("reader.mp4", "reader.mov", "reader.MOV", "reader.m4v"):
        if (ME / n).exists(): return ME / n
    stop("put the recording of the reader in my-book/ and name it reader.mp4 or reader.mov (docs/01).")
def run(*a): subprocess.run([str(x) for x in a], check=True)
def probe(p, e): return subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", e, "-of", "csv=p=0", str(p)]).decode().strip().strip(",")
def duration(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())
