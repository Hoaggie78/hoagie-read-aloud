# 5. Animate the pages (optional)

Instead of a slow drift, a page can move: leaves blow, clouds pass, a cloak flutters. A video model (LTX-2.5) turns
your page picture into a 4-second moving clip, and step 4 plays it forwards and backwards behind the reader for as
long as that page is on screen.

Only do this for a book you made or have permission to adapt. Animating changes the artwork, which goes further than
showing it (docs/00).

## What you need

- An Apple Silicon Mac with 64 GB of memory (what this was tested on) and about 80 GB of free disk
- A free Hugging Face account, with the licence accepted on the model page `dgrauet/ltx-2.5-mlx-q8`

## Step 1. Install the renderer (once)

Somewhere outside the kit folder:

    git clone https://github.com/dgrauet/ltx-2-mlx.git

Follow **that project's README** to install it (it creates a `.venv` folder with the `ltx-2-mlx` command) and to
download the **LTX-2.5 q8** model into `weights/ltx-2.5-mlx-q8` (about 70 GB). Then create a file named `.env` in the
kit folder containing one line with your own path:

    LTX_MLX_DIR=/Users/you/ltx-2-mlx

## Step 2. Say what should move

In `my-book/book.yaml`, add an `animate:` line to the pages you want to move. Describe only small, natural motion
of things already in the picture:

    pages:
      - image: 03.jpg
        starts_with: "over the fields"
        animate: "wind blows through the trees, clouds drift slowly, the cloak flutters"

Check the wording without rendering anything:

    .venv/bin/python scripts/3b_animate_pages.py --dry-run

## Step 3. Render

    .venv/bin/python scripts/3b_animate_pages.py

One 4-second clip per page, saved in `my-book/anims/`. Expect several minutes per page. Try one page first with
`--only 03.jpg`.

## Step 4. Watch every clip, and throw away the bad ones

This matters more than anything else on this page. The model often changes drawn characters: faces melt, a tail
vanishes, an extra arm appears. In the read-aloud this kit came from, **5 of 16 pages** were good enough to keep.

- **Works best:** one main subject, weather, sky, water, fire, hair and cloth.
- **Usually fails:** pages with several small characters or separate little scenes, and anything with printed text.
- **A bad clip:** delete its file from `my-book/anims/`. That page goes back to the slow drift, which always looks clean.

Then build the video as in `docs/04-make-the-video.md`. Preview each animated page before the full run.
