"""
normalize_assets.py — build public/ with browser-safe, canonical asset names.

WHY THIS EXISTS
    audio/ contains a mix of formats and naming styles:
        Track 1.wma ... Track 25.wma   (actually WMA v2 — browsers cannot play WMA)
        Track 26.mp3 ... Track 50.mp3  (real MP3)
        plus "Track 1.wma" without zero padding
    part1_photos/ uses "lesson_01.jpg" (already canonical).
    The web app always requests:
        /audio/track_XX.mp3   and   /part1_photos/lesson_XX.jpg
    This script produces exactly those names under public/, converting the 25
    WMA files to MP3 with ffmpeg so Chrome/Edge/Firefox can play all 50 tracks.

USAGE
    python scripts/normalize_assets.py            # skip already-converted files
    python scripts/normalize_assets.py --force    # redo everything
"""

import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_SRC = os.path.join(ROOT, "audio")
PHOTO_SRC = os.path.join(ROOT, "part1_photos")
PUBLIC = os.path.join(ROOT, "public")
AUDIO_OUT = os.path.join(PUBLIC, "audio")
PHOTO_OUT = os.path.join(PUBLIC, "part1_photos")


def find_source_audio(track_num):
    """Return the on-disk source path for a track, whatever its extension/case."""
    for ext in (".wma", ".mp3", ".WMA", ".MP3"):
        for name in (f"Track {track_num}{ext}", f"Track {track_num:02d}{ext}"):
            p = os.path.join(AUDIO_SRC, name)
            if os.path.exists(p):
                return p
    return None


def ffmpeg_convert(src, dst):
    """Transcode to MP3 (libmp3lame, VBR q2 ≈ 190 kbps)."""
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", src,
        "-vn", "-acodec", "libmp3lame", "-q:a", "2",
        dst,
    ]
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="re-convert existing outputs")
    args = ap.parse_args()

    os.makedirs(AUDIO_OUT, exist_ok=True)
    os.makedirs(PHOTO_OUT, exist_ok=True)

    converted, copied, skipped, failed = 0, 0, 0, 0

    for n in range(1, 51):
        src = find_source_audio(n)
        dst = os.path.join(AUDIO_OUT, f"track_{n:02d}.mp3")

        if src is None:
            print(f"  [MISSING] track {n:02d}: no source file in audio/")
            failed += 1
            continue

        if os.path.exists(dst) and not args.force:
            skipped += 1
            continue

        try:
            if src.lower().endswith(".mp3"):
                shutil.copyfile(src, dst)
                copied += 1
                print(f"  [COPY] {os.path.basename(src)} -> track_{n:02d}.mp3")
            else:
                ffmpeg_convert(src, dst)
                converted += 1
                print(f"  [CONV] {os.path.basename(src)} -> track_{n:02d}.mp3")
        except subprocess.CalledProcessError as e:
            print(f"  [FAIL] track {n:02d}: ffmpeg error {e}")
            failed += 1
        except FileNotFoundError:
            print("  [FATAL] ffmpeg not found on PATH. Install ffmpeg and retry.")
            sys.exit(2)

    for n in range(1, 51):
        src = os.path.join(PHOTO_SRC, f"lesson_{n:02d}.jpg")
        dst = os.path.join(PHOTO_OUT, f"lesson_{n:02d}.jpg")
        if not os.path.exists(src):
            print(f"  [MISSING] photo lesson_{n:02d}.jpg")
            failed += 1
            continue
        if os.path.exists(dst) and not args.force:
            skipped += 1
            continue
        shutil.copyfile(src, dst)
        copied += 1

    print(f"\nDone. converted={converted} copied={copied} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()
