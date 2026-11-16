# 3. Cut out the reader

## Step 1. Get the matting model (once)

The kit uses **Background Matting v2** (BackgroundMattingV2 by Peter Lin and others, MIT licence).

1. Open `github.com/PeterL1n/BackgroundMattingV2` and follow its **Download** link.
2. Get an **ONNX** model with the **MobileNetV2** backbone, **HD** version (about 20 MB).
3. Save it in the kit as `models/bgmv2.onnx`.

File names on that page may differ; any ONNX file from that project with inputs named `src` and `bgr` works.

## Step 2. Try 20 seconds first

    .venv/bin/python scripts/3_cutout.py --start 60 --end 80

Open `my-book/work/reader_fg.mp4`. You should see the reader on black with clean edges and a solid book.

## Step 3. Do the whole recording

    .venv/bin/python scripts/3_cutout.py

About 6 minutes per minute of video. Let it run.

## If the cutout is poor

| Problem | Fix |
|---|---|
| Patches of backdrop left around the reader | Add `my-book/empty_backdrop.jpg` (docs/01). It must be from the same camera position. |
| The book or clothes go see-through | Their colour is too close to the backdrop. Use a different backdrop or top. |
| Flickering edges | Uneven light or a wrinkled backdrop. Light it evenly and pull it flat. |
| `could not tell the reader from the backdrop` | The backdrop is not plain, or does not reach the frame edges. |

Next: `docs/04-make-the-video.md`
