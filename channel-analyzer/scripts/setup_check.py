#!/usr/bin/env python3
"""Verify that required Python packages are installed."""
import sys
import importlib.util

REQUIRED = ["yt_dlp", "youtube_transcript_api"]

missing = []
for pkg in REQUIRED:
    if importlib.util.find_spec(pkg) is None:
        missing.append(pkg.replace("_", "-"))

if missing:
    print(f"MISSING: {', '.join(missing)}")
    print("Install with: pip install --break-system-packages " + " ".join(missing))
    sys.exit(1)

print("OK: all dependencies installed")
sys.exit(0)
