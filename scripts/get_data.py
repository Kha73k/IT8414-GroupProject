"""Download and extract the UCI HAR dataset.

The dataset is not committed (270 MB extracted), so this script reproduces it.
Run once from the repo root:

    python scripts/get_data.py

The archive is verified against a SHA-256 hash before extraction so a truncated
or substituted download fails loudly rather than producing silently wrong data.
"""

import hashlib
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/240/human+activity+recognition+using+smartphones.zip"
SHA256 = "c00b803081a5c797cd5e4b83700a9810b38d53d9d84e01917e090e1fdbc81031"

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
ARCHIVE = DATA / "UCI_HAR_Dataset.zip"
EXTRACTED = DATA / "UCI HAR Dataset"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    DATA.mkdir(exist_ok=True)

    if not ARCHIVE.exists():
        print(f"Downloading {URL}")
        urllib.request.urlretrieve(URL, ARCHIVE)
    else:
        print(f"Archive already present: {ARCHIVE}")

    digest = sha256(ARCHIVE)
    if digest != SHA256:
        sys.exit(
            f"SHA-256 mismatch.\n  expected {SHA256}\n  got      {digest}\n"
            f"Delete {ARCHIVE} and re-run."
        )
    print(f"SHA-256 verified: {digest}")

    # The published archive nests a second zip inside the first.
    with zipfile.ZipFile(ARCHIVE) as outer:
        outer.extract("UCI HAR Dataset.names", DATA)
        with zipfile.ZipFile(io.BytesIO(outer.read("UCI HAR Dataset.zip"))) as inner:
            inner.extractall(DATA)

    macosx = DATA / "__MACOSX"
    if macosx.exists():
        for p in sorted(macosx.rglob("*"), reverse=True):
            p.unlink() if p.is_file() else p.rmdir()
        macosx.rmdir()

    n = len(list(EXTRACTED.rglob("*.txt")))
    print(f"Extracted to {EXTRACTED} ({n} .txt files)")


if __name__ == "__main__":
    main()
