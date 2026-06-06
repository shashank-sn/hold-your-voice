---
name: voice-matcher
description: Use when the user wants to write from their own writing, build a voice profile from samples, match an existing writer's style, or make new copy sound like a project/person without copying generic style advice.
---

# Voice Matcher

Build from the writer's own writing. Do not invent a voice from adjectives.

## Source Hierarchy

1. User-provided samples in the conversation.
2. Project files the user identifies as their own writing.
3. Obvious authored prose in the repo, such as essays, posts, emails, public
   copy, changelog entries, or founder notes.
4. `assets/economic-drift-voice.md` only when the user asks for Shashank's or
   "my" voice and no better current samples exist.

## Profile Build

Run the portable profiler when files are available:

```bash
hyv profile \
  --name "project voice" \
  --out .hold-your-voice/voice-profile.json \
  <sample paths>
```

The profile is a working benchmark, not a literary biography. It should capture:

- sentence rhythm
- paragraph shape
- openings
- argument pattern
- recurring concrete textures
- things the writer avoids
- sample anchors that prove the profile

## Writing Method

- Start from the user's requested point, not from decorative tone imitation.
- Use the profile as a constraint system.
- Match cadence and thinking pattern before vocabulary.
- Keep the writer's roughness when it is part of the voice.
- Do not sand the draft into smooth, generic competence.
- After drafting, run an AI-pattern scan and repair only weak lines.

## Verification

Before handing back final copy, ask:

- Does the opening sound like a real observation rather than a template?
- Could this line belong unchanged to five other people? If yes, rewrite it.
- Are there profile anchors that justify this cadence?
- Did the rewrite preserve the user's meaning and risk appetite?

