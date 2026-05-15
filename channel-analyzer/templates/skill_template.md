---
name: <channel-handle>-writer
description: <Write a description that triggers when the user wants to write in this channel's voice. Include the creator name, the format (shorts/long-form/essays), the length range, and several trigger phrases. Follow the pattern of shorts-writer's description: explicit about what it produces, what topics or formats it covers, and what NOT to use it for. ~80-120 words.>
---

# <Creator Name> writer

## What this skill produces

<1 paragraph. Word count range, runtime range, format type (short / long essay / commentary / tutorial), and the one-line thesis of what this writer is actually doing. Match the opening of shorts-writer — be specific about output shape.>

## Provenance

Reverse-engineered from <N> videos by <@handle> (<date range>), weighted toward top performers by view count. Reference transcripts at the bottom of this file are the voice benchmark — match their cadence and rhythm, not their topics.

## Voice and philosophy

<2-3 paragraphs. What is this writer actually doing at the sentence level? What system or worldview underlies the scripts? What is the emotional register — authoritative, conversational, provocative, analytical? What do they do that generic AI output does not?

End this section with any vocabulary rules — words the writer demonstrably never uses, or that would break the voice if they appeared.>

## Structure

<If the channel has a consistent beat structure, document it with timing estimates per beat and rules for each. If the structure is looser, describe the patterns you observed and name them honestly as tendencies rather than rules. Do not invent a beat structure that isn't in the source.

For each beat or section, include:
- Approximate timing / word count
- What the beat accomplishes
- Specific rules for that beat (opening patterns, required elements, things to avoid)
- 1-2 examples pulled or paraphrased from the reference transcripts>

## Sentence-level style rules

**Sentence length:** <Observed default range. Do they run long? Alternate? Default short with occasional rolling sentences?>

**Rhythm:** <How does the writer create momentum? Short-long alternation? Repetition? Fragments? Be specific.>

**Tense:** <Present tense? Past? Mixed with purpose?>

**Direct address:** <Do they use "you"? When? How often?>

**Data usage:** <How are numbers deployed? Escalating cascades? Single anchor figures? Always with a named source?>

**Never use:** <List of phrases the writer demonstrably avoids. Include generic AI tells the voice happens to dodge, plus any words that would specifically break this writer's voice.>

**Incomplete sentences / fragments:** <When and how, if at all.>

## AI-avoidance rules

<Hard rules that prevent the output from sliding into generic AI prose. The mirror-contrast rule below is a strong default — keep it unless the source writer demonstrably uses mirrored contrasts as a stylistic choice.>

**The mirror-contrast rule.** The single biggest AI writing tell is mirrored contrast constructions:
- "It's not X, it's Y"
- "Not X — Y"
- "They weren't X. They were Y."
- Any phrasing where the second clause mirrors the grammatical shape of the first

Cut these entirely. State the direct claim instead.

<Add channel-specific AI-avoidance rules here — patterns the writer naturally dodges that an AI would reach for.>

## Title rules

<Extract 2-4 title formats from videos.json. For each, give the pattern and 1-2 examples. Note what kinds of titles the writer avoids.>

## Quality checklist

- [ ] <8-12 checkboxes. Each should be a specific, testable question about the draft. Mirror the style of shorts-writer's checklist but tailor to this voice.>
- [ ] Does it sound like a person talking when read aloud?

---

## Reference transcripts — match this voice and cadence, not these topics

These are <N> top-performing scripts from <@handle>. When writing a new script, use these as the voice benchmark. Extract cadence, sentence rhythm, how evidence is stacked, and how the close lands. Do not copy topics or subject matter.

---

### Reference 1: <Video Title>
*<views> views · <runtime> seconds*
*<URL>*

<Transcript pasted verbatim. Preserve paragraph breaks where possible — listen for natural pauses when reading the auto-captioned text and break accordingly.>

---

### Reference 2: <Video Title>
*<views> views · <runtime> seconds*
*<URL>*

<Transcript pasted verbatim.>

---

### Reference 3: <Video Title>
*<views> views · <runtime> seconds*
*<URL>*

<Transcript pasted verbatim.>
