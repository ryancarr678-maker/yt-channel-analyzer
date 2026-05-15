---
name: channel-analyzer
description: Reverse-engineer a YouTube channel's scriptwriting voice into a reusable writing skill. Use this skill when the user wants to analyze a YouTube channel, study a scriptwriter's style, build a script generator based on someone's content, create a writing skill from a creator's videos, or turn a channel's voice into a SKILL.md file. Triggers include phrases like "analyze this channel," "build a skill from @handle," "reverse engineer their voice," "study how [creator] writes," or any request to turn a channel's transcripts into a writing style guide. Takes a YouTube channel URL, fetches the top N videos by view count, pulls their transcripts, analyzes the corpus for voice patterns (hook structure, sentence cadence, evidence-stacking habits, closing styles, forbidden phrases), and produces a new SKILL.md that can be dropped into ~/.claude/skills/ for reuse. Do NOT use for analyzing individual videos, writing a single script, or pulling transcripts without analysis — this skill's output is a reusable writing voice guide, not ad-hoc content.
---

# Channel Analyzer

## What this skill produces

A new `SKILL.md` file — structured like `shorts-writer` — that captures the voice, beat structure, sentence-level patterns, and AI-avoidance rules extracted from a specific YouTube channel's top-performing scripts. The output is a standalone skill the user can drop into `~/.claude/skills/` and invoke later to generate new scripts in that channel's voice.

## When to run this skill

The user provides a YouTube channel URL or handle (e.g. `@sszuchan`, `youtube.com/@mkbhd`, or a full channel URL). They want a reusable writing skill, not a one-off analysis.

If the user provides anything other than a channel URL or handle — a single video, a topic, a request to write a script — stop and redirect. This skill analyzes channels only.

## The pipeline

Execute these steps in order. Do not skip.

### Step 1 — Environment check

Run the setup script to verify Python dependencies are installed:

```bash
python3 scripts/setup_check.py
```

If it reports missing packages, install them:

```bash
pip install --break-system-packages yt-dlp youtube-transcript-api
```

`yt-dlp` is used for channel enumeration and view counts because it doesn't require a Google API key. `youtube-transcript-api` pulls transcripts without auth.

### Step 2 — Fetch channel metadata

Run the fetcher with the channel URL or handle the user provided, and the number of videos to analyze (default: 20, max: 50):

```bash
python3 scripts/fetch_channel.py "<channel_url_or_handle>" --top 20 --out corpus/
```

This writes two things to `corpus/`:
- `videos.json` — sorted list of top-N videos by view count with title, URL, views, duration, upload date
- `transcripts/<video_id>.txt` — one transcript per video, with a header containing metadata

If more than 30% of videos fail to produce transcripts (auto-captions disabled, private, age-gated), warn the user. Ask whether to continue with the smaller corpus or to bump `--top` higher to compensate.

### Step 3 — Read the corpus yourself

Before writing any analysis, **read every transcript in `corpus/transcripts/`**. Do not summarize based on filenames or titles. Voice lives in sentence rhythm — you cannot extract it without reading the text.

As you read, keep notes on:

- **Opening patterns.** How do the first 2-3 sentences work? Do they anchor in time/person/place? Do they use questions, claims, or scene-setting?
- **Named concepts.** Does the writer coin or repeat specific terms as mental handles?
- **Evidence habits.** How is data deployed? How many examples per argument? How specific are the numbers?
- **Sentence length and rhythm.** Short-long alternation? Fragment usage? Comma density?
- **Closing style.** Aphorism? Call to action? Question? Escalation?
- **Forbidden tells.** Phrases the writer consistently avoids that a generic AI would reach for (mirrored contrasts, "essentially," "here's the thing," etc.).
- **Topic anchors.** What domains do they return to? What kinds of specific detail do they favor?
- **Cadence signatures.** Read passages aloud in your head. What does the rhythm feel like?

### Step 4 — Pick 3 reference transcripts

Choose 3 transcripts that best represent the channel's voice. Prioritize:
1. Highest view count (performance signal)
2. Representative of the dominant format (if the channel has a clear one)
3. Clean transcripts — auto-captions with heavy errors hurt more than they help

These will be embedded verbatim in the output SKILL.md as voice benchmarks, following the pattern at the bottom of `shorts-writer`.

### Step 5 — Write the new SKILL.md

Use the template in `templates/skill_template.md` as the scaffold. Fill in every section based on what you observed in Step 3. Specifically:

- **Name and description.** Use the channel's creator name or handle. The description must include enough trigger phrases that Claude Code will route style requests to this skill. Follow the pattern of `shorts-writer`'s description.
- **Voice and philosophy.** 2-3 paragraphs. What is this writer actually doing? What system or worldview underlies the scripts? What is the emotional register?
- **Structure.** If the writer follows a repeatable beat structure (like Sam Szuchan's 5-beat arc), document it with timing estimates. If they don't, describe the looser patterns you see and name them honestly as patterns rather than rules.
- **Sentence-level style rules.** Specific, observed habits. Sentence length defaults, tense choices, rhythm rules, direct-address patterns. Include at least one "never use" list drawn from phrases the writer demonstrably avoids.
- **AI-avoidance rules.** Any specific tells this channel's voice naturally dodges — these become hard rules in the output skill. The mirror-contrast rule from `shorts-writer` is a strong default; keep or adapt it.
- **Title rules.** Extract patterns from actual video titles in `videos.json`.
- **Quality checklist.** 8-12 checkboxes that a generated script should pass.
- **Reference transcripts.** The 3 chosen in Step 4, pasted verbatim with view count, runtime, and URL headers — match the format used in `shorts-writer`.

Output the new skill to `~/output/<channel-handle>-writer/SKILL.md`. Create the directory if it doesn't exist.

### Step 6 — Report to the user

Tell the user:
1. How many transcripts were successfully analyzed (and how many failed, if any).
2. The top 3 videos chosen as references, with view counts.
3. The path to the generated skill.
4. Installation instructions: copy the folder to `~/.claude/skills/` and the skill will be available in future Claude Code sessions.

Offer to run a test generation — give them a topic, and produce one script using the newly written skill to verify voice capture.

## Quality bar for the output skill

The generated SKILL.md must be usable by a future Claude instance with zero additional context. That means:

- Every rule must be specific enough to act on. "Use strong verbs" is useless. "Open with a named person and a year" is actionable.
- The reference transcripts must be present verbatim at the bottom — they are the voice benchmark when instructions get abstract.
- The description field must trigger reliably. Test it mentally: if a user typed "help me write in [creator]'s style," would this skill surface?
- Do not copy `shorts-writer` wholesale. A channel with a different format needs a different beat structure. Copying the 5-beat arc when the source doesn't use one produces garbage output.

## What this skill deliberately doesn't do

- **Does not train or fine-tune anything.** It produces a prompt-level skill that steers Claude's generation.
- **Does not analyze visual or audio style.** Transcripts only. If a channel's magic is in its B-roll or delivery, this tool will miss it — say so in the output.
- **Does not handle channels with under ~10 usable transcripts.** If the corpus is too thin, the skill will overfit. Warn the user and stop.
- **Does not copy copyrighted material into the skill beyond the 3 reference transcripts.** Reference transcripts are for voice calibration in a personal tool; do not redistribute the resulting skill publicly without the creator's permission.

## Failure modes and how to handle them

- **Transcripts are all auto-captioned and messy.** Proceed, but flag in the output skill's description that cadence extraction may be approximate. Recommend the user manually clean 1-2 transcripts for better reference quality.
- **Channel is primarily non-English.** Either analyze in the source language (preserving voice) or tell the user this tool is tuned for English and recommend manual review.
- **Channel has wildly varying formats (long essays + shorts + vlogs).** Ask the user which format to focus on before analyzing. A skill that tries to cover three formats ends up covering none.
- **Top videos are all one viral hit and unrelated content.** Flag this. Offer to weight by recency instead, or to filter by duration (e.g. shorts only).
