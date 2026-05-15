#!/usr/bin/env python3
"""
Fetch the top-N videos by view count from a YouTube channel and pull their
transcripts. Writes videos.json + transcripts/*.txt to the output directory.

Usage:
    python3 fetch_channel.py "@sszuchan" --top 20 --out corpus/
    python3 fetch_channel.py "https://youtube.com/@mkbhd" --top 30 --out corpus/
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import yt_dlp
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
    )
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install --break-system-packages yt-dlp youtube-transcript-api")
    sys.exit(1)


def normalize_channel_url(raw: str) -> str:
    """Accept @handle, youtube.com/@handle, or full URL. Return a URL yt-dlp can use."""
    raw = raw.strip()
    if raw.startswith("@"):
        return f"https://www.youtube.com/{raw}/videos"
    if "youtube.com" not in raw and "youtu.be" not in raw:
        # Assume it's a handle without @
        return f"https://www.youtube.com/@{raw}/videos"
    # Ensure we're hitting the videos tab, not the channel home
    if "/videos" not in raw and "/watch" not in raw:
        raw = raw.rstrip("/") + "/videos"
    return raw


def fetch_video_list(channel_url: str, limit: int = 200) -> list[dict]:
    """Use yt-dlp to enumerate videos on a channel. Returns list of dicts with metadata."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",
        "playlistend": limit,
        "skip_download": True,
    }
    print(f"Enumerating videos from: {channel_url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    entries = info.get("entries", [])
    videos = []
    for e in entries:
        if not e or not e.get("id"):
            continue
        videos.append({
            "id": e.get("id"),
            "title": e.get("title", "").strip(),
            "url": e.get("url") or f"https://www.youtube.com/watch?v={e.get('id')}",
            "views": e.get("view_count") or 0,
            "duration": e.get("duration") or 0,
        })
    return videos


def hydrate_view_counts(videos: list[dict]) -> list[dict]:
    """
    Flat extraction sometimes returns view_count=None. Re-fetch individually for
    any video missing view counts. Slower but accurate.
    """
    missing = [v for v in videos if not v["views"]]
    if not missing:
        return videos

    print(f"Hydrating view counts for {len(missing)} videos (flat extract was incomplete)...")
    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for v in missing:
            try:
                info = ydl.extract_info(v["url"], download=False)
                v["views"] = info.get("view_count") or 0
                v["duration"] = info.get("duration") or v["duration"]
                v["upload_date"] = info.get("upload_date", "")
            except Exception as err:
                print(f"  [warn] could not hydrate {v['id']}: {err}")
                v["views"] = 0
    return videos


def sanitize_filename(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", s)[:120]


def fetch_transcript(video_id: str) -> str | None:
    """Returns transcript text or None if unavailable."""
    try:
        api = YouTubeTranscriptApi()
        # Prefer manually-created over auto-generated for cadence quality
        transcript_list = api.list(video_id)
        try:
            t = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
        except NoTranscriptFound:
            t = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
        entries = t.fetch()
        # Join with spaces, preserving rough sentence structure
        return " ".join(e.text.replace("\n", " ").strip() for e in entries if e.text)
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
        return None
    except Exception as err:
        print(f"  [warn] transcript fetch failed for {video_id}: {err}")
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel", help="Channel URL or @handle")
    ap.add_argument("--top", type=int, default=20, help="Number of top videos by views to pull")
    ap.add_argument("--out", default="corpus/", help="Output directory")
    ap.add_argument("--scan", type=int, default=150,
                    help="How many recent videos to scan before picking top N (default 150)")
    args = ap.parse_args()

    if args.top > 50:
        print("Warning: --top > 50 will produce a corpus too large for meaningful analysis. Capping at 50.")
        args.top = 50

    out_dir = Path(args.out)
    (out_dir / "transcripts").mkdir(parents=True, exist_ok=True)

    url = normalize_channel_url(args.channel)
    videos = fetch_video_list(url, limit=args.scan)

    if not videos:
        print(f"ERROR: no videos found at {url}")
        sys.exit(1)

    print(f"Found {len(videos)} videos. Hydrating view counts...")
    videos = hydrate_view_counts(videos)
    videos.sort(key=lambda v: v["views"], reverse=True)
    top_videos = videos[: args.top]

    print(f"\nTop {len(top_videos)} by views:")
    for i, v in enumerate(top_videos[:10], 1):
        print(f"  {i:2d}. [{v['views']:>10,}] {v['title'][:70]}")
    if len(top_videos) > 10:
        print(f"  ... and {len(top_videos) - 10} more")

    print("\nFetching transcripts...")
    results = []
    fails = 0
    for v in top_videos:
        transcript = fetch_transcript(v["id"])
        if transcript is None:
            fails += 1
            v["transcript_status"] = "unavailable"
            results.append(v)
            continue

        fname = f"{sanitize_filename(v['id'])}.txt"
        fpath = out_dir / "transcripts" / fname
        header = (
            f"# {v['title']}\n"
            f"# URL: {v['url']}\n"
            f"# Views: {v['views']:,}\n"
            f"# Duration: {v['duration']}s\n"
            f"# ID: {v['id']}\n\n"
        )
        fpath.write_text(header + transcript, encoding="utf-8")
        v["transcript_file"] = str(fpath)
        v["transcript_status"] = "ok"
        v["word_count"] = len(transcript.split())
        results.append(v)

    fail_rate = fails / len(top_videos) if top_videos else 1.0
    summary = {
        "channel_input": args.channel,
        "channel_url": url,
        "total_scanned": len(videos),
        "top_requested": args.top,
        "transcripts_fetched": len(top_videos) - fails,
        "transcripts_failed": fails,
        "fail_rate": round(fail_rate, 2),
        "videos": results,
    }
    (out_dir / "videos.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nDone. Wrote {len(top_videos) - fails} transcripts to {out_dir}/transcripts/")
    print(f"Summary: {out_dir}/videos.json")
    if fail_rate > 0.3:
        print(f"\nWARNING: {fail_rate:.0%} of videos had no transcript available.")
        print("Consider re-running with a larger --top value to compensate.")


if __name__ == "__main__":
    main()
