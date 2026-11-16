# Hoagie Read Aloud

Turn a recording of someone reading a picture book into a finished read-aloud video: the book's pages fill the screen,
the reader sits in the corner, and the words light up as they are spoken. It also cuts vertical Shorts from the same
recording.

This is the method behind a small family read-aloud channel, with everything specific to that channel removed. It
contains scripts and step-by-step guides. It contains no book, no footage and no one's child.

> **Use a book you own, wrote, or have written permission to read on video, or a public-domain book. If the reader is a
> child, a parent runs everything.** Read `docs/00-before-you-start.md` first.

## The steps

| | Step | Guide | Time |
|---|---|---|---|
| 0 | Which book, and filming a child | `docs/00-before-you-start.md` | 10 min |
| 1 | Record the reader and photograph the pages | `docs/01-record.md` | 30 min |
| 2 | Find the page turns | `docs/02-find-the-page-turns.md` | 15 min |
| 3 | Cut out the reader | `docs/03-cut-out-the-reader.md` | about 6 min per minute of video |
| 4 | Make the video and Shorts | `docs/04-make-the-video.md` | a few minutes |
| 5 | Optional: animate the pages with LTX-2.5 | `docs/05-animate-the-pages.md` | several minutes per page |

## Quick start

    git clone https://github.com/Hoaggie78/hoagie-read-aloud.git
    cd hoagie-read-aloud
    bash scripts/1_setup.sh

Then open `docs/00-before-you-start.md` and go in order. Each script tells you what to do next and stops with a plain
message when something is wrong.

**Using an AI coding assistant?** Open this folder in your editor and say: *"Read AGENTS.md and help me make my
read-aloud video."*

## What you need

An Apple Silicon Mac, a phone, a plain backdrop, `ffmpeg` and Python 3.11 or newer (`brew install ffmpeg python`).
Everything runs on your computer and costs nothing. The optional page animation needs 64 GB of memory.

## What is in here

    docs/                    the guides, in order
    scripts/1_setup.sh       check your computer, make my-book/
    scripts/2_listen.py      write down every word with its time; find the page turns
    scripts/3_cutout.py      cut the reader out of the backdrop
    scripts/3b_animate_pages.py  optional: make chosen pages move (LTX-2.5 on your Mac)
    scripts/4_make_video.py  build the 16:9 video, previews and 9:16 Shorts
    book.example.yaml        the settings for your video
    my-book/                 YOUR recording, pages and videos (created by setup; never committed to git)

## What was tested

As of November 2026: setup, the listening step on a 9-minute recording, and the cutout, preview and Short on a
22-second stretch of real footage on an M1 Max, with the output checked by eye. Playing an animated page behind the reader was tested with an existing clip; **rendering** a page
animation with `3b_animate_pages.py` has not been run from this repository (the clips we used were made with an
earlier LTX version). A complete full-length build has not been run, and nothing was tested on Windows, Linux or Intel Macs.

## Models and licences

Whisper by OpenAI, through mlx-whisper (downloaded automatically), and Background Matting v2 by Peter Lin and others
(you download it; docs/03). The optional animation step uses LTX-2.5 by Lightricks through ltx-2-mlx by dgrauet (docs/05). The scripts and guides here are under the MIT licence (`LICENSE`).
