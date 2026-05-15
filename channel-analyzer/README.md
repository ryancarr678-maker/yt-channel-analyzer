# channel-analyzer

A Claude Code skill that reverse-engineers a YouTube channel's scriptwriting voice into a reusable writing skill.

## What it does

Point it at a YouTube channel → it pulls the top-N videos by view count, grabs their transcripts, reads through them, and writes a new `SKILL.md` file that captures the channel's voice, beat structure, and sentence-level habits. You drop that file into `~/.claude/skills/` and use it to generate scripts in that voice later.

## Installation

One-time setup:

```bash
# 1. Copy this folder into your Claude Code skills directory
cp -r channel-analyzer ~/.claude/skills/

# 2. Install the two Python dependencies
pip install --break-system-packages yt-dlp youtube-transcript-api
```

That's it. Next time you open Claude Code, the skill will be available.

## Usage

In Claude Code, just say what you want:

```
Analyze @sszuchan and build a writing skill from it.
```

or

```
Reverse-engineer youtube.com/@mkbhd — I want to write like him.
```

Claude Code will route to the skill, run the fetcher, read the corpus, and write a new `SKILL.md` to `/home/claude/output/<handle>-writer/`. Copy the resulting folder into `~/.claude/skills/` and the new writing skill is ready to use.

## What you get

The output skill has the same shape as `shorts-writer`:

- Voice and philosophy — what the writer is actually doing
- Beat structure (if the writer has one)
- Sentence-level rules — length, rhythm, tense, fragments
- AI-avoidance rules — phrases the voice naturally dodges
- Title patterns extracted from real videos
- Quality checklist
- 3 reference transcripts pasted verbatim as voice benchmarks

## Tuning

Default is top 20 videos. For channels with more material, bump it:

```
Analyze @sszuchan with the top 40 videos.
```

If more than 30% of transcripts fail to fetch (disabled, age-gated, etc.), Claude Code will warn and ask whether to continue or re-pull with a larger scan.

## Limitations

- **Transcripts only.** This tool doesn't see B-roll, delivery, or edit pacing. For channels whose magic is primarily visual, the extracted skill will be thinner.
- **Auto-captions vary.** Channels with manually-uploaded subs produce cleaner voice extraction. Most don't have them.
- **Needs ~10 usable transcripts minimum.** Below that, the output skill overfits to a small sample.
- **English-tuned.** The analysis prompts assume English prose rhythm. Other languages will work but may need manual tuning.
- **View counts are lifetime.** An old viral hit will weight the corpus even if the voice has evolved. If that's a problem, re-run with fewer videos, or manually curate.

## Files

```
channel-analyzer/
├── SKILL.md                        # What Claude Code reads when invoked
├── README.md                       # This file
├── scripts/
│   ├── setup_check.py              # Verifies dependencies
│   └── fetch_channel.py            # Pulls metadata + transcripts
└── templates/
    └── skill_template.md           # Scaffold for the generated skill
```
