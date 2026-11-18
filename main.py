#!/usr/bin/env python3
"""make.fun entry: news-image-20261118 — "Sum up 18 November's world news in one image".

The front page itself is composed by build_page.py (in this repository),
which draws the whole newspaper page from the day's stories with Pillow and
writes assets/entry.png. This entrypoint is what the grader runs: it copies
that image to /output/entry.png, using only the Python standard library so
it runs in the bare grading sandbox (no network, no third-party packages).
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")
DEST_DIR = "/output"
DEST = os.path.join(DEST_DIR, "entry.png")


def main():
    if not os.path.exists(SOURCE):
        print(f"missing image asset: {SOURCE}", file=sys.stderr)
        return 1
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    size = os.path.getsize(DEST)
    print(f"wrote {DEST} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
