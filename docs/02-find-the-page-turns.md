# 2. Find the page turns

The kit listens to the recording, writes down every word with its time, and works out when each page starts.

1. Run setup once: `bash scripts/1_setup.sh`
2. Open `my-book/book.yaml`. Under `pages:` make one entry per picture, in order. For now put anything in
   `starts_with` (leave the first page's empty).
3. Run:

       .venv/bin/python scripts/2_listen.py

   The first run takes about a minute per ten minutes of video. It will say it could not find your placeholder words.
   That is expected.
4. Open `my-book/work/TRANSCRIPT.txt`. Every line starts with a time. For each page, find the first few words the
   reader says on that page and copy **three to five words exactly as written there** into that page's `starts_with`.
   The transcript may mishear a word; copy what it wrote, not what the book says.
5. Run the command again. It prints each page with its start and end time. Check the times look right.

If a page shows only a second or two, its `starts_with` matched too early: pick words a little later, or a longer phrase.

Next: `docs/03-cut-out-the-reader.md`
