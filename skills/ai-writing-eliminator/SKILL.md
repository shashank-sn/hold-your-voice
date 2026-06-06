---
name: ai-writing-eliminator
description: Use when the user wants to remove AI writing patterns, humanize a draft, make prose less generic, scan for AI cadence, or rewrite only the lines that sound synthetic.
---

# AI Writing Eliminator (v2)

This skill removes machine-shaped writing without destroying the draft. The
algorithm now detects 220+ named AI writing patterns across 31 composite regex
rules, plus 9 structural/rhythmic signals (burstiness, paragraph uniformity,
contraction density, formal hedging, intensifier overuse, fragment ratio,
staccato detection, over-structured lists, uniform sentence rhythm).

## Non-Negotiables

- Fix flagged lines only unless the user asks for a full rewrite.
- Preserve the original argument and local meaning.
- Do not add praise, summaries, preambles, CTAs, or extra sections.
- Do not replace specific roughness with smooth generic prose.
- After editing, rescan the result.

## Scan

- Fix flagged lines only unless the user asks for a full rewrite.
- Preserve the original argument and local meaning.
- Do not add praise, summaries, preambles, CTAs, or extra sections.
- Do not replace specific roughness with smooth generic prose.
- After editing, rescan the result.

## Scan

Use the helper script when a draft is in a file:

```bash
hyv scan <draft path>
```

For pasted text, apply the same rules manually from
`assets/ai-eliminator-rules.md`.

## Repair Prompt

When a model rewrite is needed, generate a line-level prompt:

```bash
hyv rewrite-prompt \
  --profile .hold-your-voice/voice-profile.json \
  <draft path>
```

If there is no profile, still repair the AI patterns, but do not claim the
result is voice-matched.

## Bad Fixes

Reject fixes that:

- turn the draft into a tidy founder post
- make every paragraph land as a lesson
- replace a concrete scene with an abstract principle
- use dramatic line breaks to fake rhythm
- make the writer sound more professional but less specific

