# YouTube Channel Analyzer

A Claude Code skill that reverse-engineers any YouTube creator's writing voice into a reusable script-writing tool.

## What it does

Point it at a YouTube channel and it:

1. Fetches the top 20 videos by view count using `yt-dlp` — a free tool that pulls YouTube metadata without needing a Google API key
2. Downloads every transcript and reads them in full
3. Extracts hook structure, sentence rhythm, evidence habits, closing patterns, and the specific phrases that voice naturally avoids
4. Selects the 3 highest-performing videos and embeds their full transcripts verbatim — so when you generate new scripts, you're matching against real examples, not just a description of them
5. Outputs a reusable `SKILL.md` you can invoke any time

The result isn't a one-off analysis. It's a standing writing assistant locked to a specific creator's voice.

## Requirements

- [Claude Code](https://claude.ai/code) (the CLI)
- Python 3
- Two Python packages (the skill installs these for you):
  ```
  pip install yt-dlp youtube-transcript-api
  ```

## Installation

```bash
# Clone the repo
git clone https://github.com/ryancarr678-maker/yt-channel-analyzer.git

# Copy the skill into your Claude Code skills directory
cp -r yt-channel-analyzer/channel-analyzer ~/.claude/skills/
```

That's it. The next time you open Claude Code, the skill will be available.

## Usage

In Claude Code, just say what you want:

```
Analyze @mkbhd and build a writing skill from it.
```

or

```
Reverse-engineer youtube.com/@sszuchan — I want to write like him.
```

Claude Code will fetch the top videos, read the transcripts, and write a new `SKILL.md` to `~/output/<handle>-writer/`. Copy that folder into `~/.claude/skills/` and the new writing skill is ready to use.

## What you get

The output skill captures:

- **Voice and philosophy** — what the writer is actually doing and why it works
- **Beat structure** — the repeatable arc the creator follows (if they have one)
- **Sentence-level rules** — length defaults, rhythm, tense, fragment usage
- **AI-avoidance rules** — the specific phrases that voice naturally dodges
- **Title patterns** — extracted from real video titles
- **Quality checklist** — criteria a generated script should pass
- **3 reference transcripts** — pasted verbatim as voice benchmarks

## Options

Default is top 20 videos. For channels with more material:

```
Analyze @sszuchan with the top 40 videos.
```

## Limitations

- **Transcripts only.** Delivery, B-roll, and edit pacing aren't captured.
- **Needs ~10 usable transcripts minimum.** Below that, the output overfits.
- **Auto-captions vary in quality.** Manually uploaded subtitles produce cleaner extraction.
- **English-tuned.** Other languages will work but may need manual review.

## Built by

Ryan Carruthers — [LinkedIn](https://www.linkedin.com/in/ryancarruthers)
