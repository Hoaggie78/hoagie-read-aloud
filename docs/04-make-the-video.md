# 4. Make the video

## Preview first

    .venv/bin/python scripts/4_make_video.py --start 60 --end 80

Open `my-book/preview.mp4`. You should see the page filling the screen and drifting slowly, the reader in the corner,
and a card of words where the word being spoken is highlighted.

Adjust in `my-book/book.yaml` and preview again:

| Setting | What it changes |
|---|---|
| `reader.side` | `right` or `left`. Put the reader over the less important side of the pictures. |
| `reader.height` | How big the reader is (0.62 = 62 % of the picture height). |
| `captions.words_per_card` | How many words show at once. |
| `captions.fix` | Corrects a misheard word everywhere, for example a name. |
| `captions.enabled` | `false` removes the words. |
| `page_motion` | How much the page drifts. `0` holds it still. |

## The full video

    .venv/bin/python scripts/4_make_video.py

Writes `my-book/final.mp4` (1920 × 1080). Watch it from start to finish with sound.

## Shorts

Pick a funny or sweet moment, note its start and end time in seconds from `TRANSCRIPT.txt`, and run:

    .venv/bin/python scripts/4_make_video.py --short 126 142 funny-dog

Writes `my-book/short_funny-dog.mp4` (1080 × 1920): the page on top, the words in the middle, the reader below.
Keep Shorts under 60 seconds.

## Before you post

- You have the right to show this book (docs/00).
- Nothing personal is visible or said.
- For a children's channel, the video is marked as made for kids.

## What this kit does not do

The channel this came from also animated some pages with a video model and rebuilt page art with an image model. Those
steps are not included: they need more hardware, and changing a published book's artwork needs the publisher's
permission. A slow drift across your own page photos does most of the work.
