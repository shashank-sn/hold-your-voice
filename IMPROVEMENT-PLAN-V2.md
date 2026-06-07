# HYV V2: Voice-First Writing Engine

## Core Reframe

HYV is NOT an AI detector that also does voice. HYV is a **voice-first writing engine** that also happens to catch AI patterns. The difference is in what leads:

**Old framing:** "Scan for AI patterns, then rewrite flagged lines."
**New framing:** "Help people write in their own voice. AI pattern detection is a side effect of knowing what a real voice sounds like."

Everything from the Magnetic Email / Kieran Drew / Signal Engine materials reinforces this: great writing is personal, conversational, story-driven, specific, and opinionated. AI writing fails on ALL of those axes — not just "uses em dashes."

## What the Writing Docs Taught Us

From Kieran Drew's Magnetic Email system, the principles that should become HYV heuristics:

1. **Rule of One** — one problem, one story, one solution. AI tries to cover everything.
2. **Personal perspective** — stories, worldviews, beliefs, weirdness. AI is impersonal.
3. **Don't educate, excite** — AI over-educates and under-excites.
4. **Conversations not speeches** — AI lectures. Humans talk to one person.
5. **Storytelling worship** — "No point without a story, no story without a point." AI makes points without stories.
6. **Respect attention** — AI is verbose. Great writers are ruthless with words.
7. **Connect to create** — "People don't want new, they want familiar." AI tries to be novel.
8. **Hell Yeah not Yeah Yeah** — AI is safe and average. Voice is bold and weird.
9. **Always be asking** — AI explains. Writers invite action.
10. **Reputation over revenue** — AI optimizes for engagement. Voice optimizes for trust.

These become detection signals AND rewrite targets.

## Architecture

```
hold_voice.py          — Core engine (profile, scan, rewrite, evolve)
hold_voice_craft.py    — NEW: Writing craft analysis (storytelling, conversation, specificity)
hold_voice_sync.py     — Cloud sync (existing)
```

Split craft analysis into a separate module to keep the core script focused.
