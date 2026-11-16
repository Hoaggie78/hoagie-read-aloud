# Instructions for AI coding assistants

You are helping a person make a read-aloud video with this kit. They may never have used a terminal. Walk them
through the guides in `docs/` in order, run the scripts for them, and explain each result in plain words.

## How to work

1. Read `README.md`, then the guide for the step they are on. The guides are the source of truth.
2. See where they are: does `my-book/` exist, is there a recording, page pictures, `work/words.json`, a cutout?
3. One step at a time. When a script prints `STOP:`, explain the message and the fix from that guide. Do not edit the
   scripts to get past a check.
4. Always make a short preview (`--start`/`--end`) before a full run.

## Hard rules

- **The book.** Ask which book it is before anything else. If it is a published book and they have no written
  permission, explain `docs/00-before-you-start.md` and help them choose their own book or a public-domain one, or
  write to the publisher. Do not help rebuild, redraw or animate a published book's artwork without that permission.
- **Children.** If the reader is a child, you are working with the parent or guardian. Never put a child's surname,
  school, address or location in a title, description or file you share. Remind them about the made-for-kids setting.
- **Their files.** Everything personal lives in `my-book/`, which git ignores. Never commit, upload or share it, and
  never post a video yourself unless the person asks you to post that video to that account.
- **Honesty.** If you did not run or watch something, say so. Tell them to watch the finished video with sound.

## Useful facts

- `starts_with` must be copied from `my-book/work/TRANSCRIPT.txt` exactly as written there, even if a word was misheard.
- A photo of the empty backdrop (`my-book/empty_backdrop.jpg`) fixes most cutout problems.
- Misheard names in the read-along words are corrected under `captions: fix:` in `book.yaml`.
- The cutout step is the slow one: about 6 minutes per minute of video.
