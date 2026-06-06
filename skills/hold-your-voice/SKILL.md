---
name: hyv-hold-your-voice
description: "Use when the user wants Hold Your Voice-style writing help across any project: build a voice profile from samples, match a writer's voice, remove AI-writing drift, rewrite drafts without flattening voice, or preserve project-specific writing style."
---

# Hold Your Voice

This is the orchestration skill. Use the narrower `voice-matcher` and
`ai-writing-eliminator` skills when a task is only one half of the workflow.

## Core Doctrine

- Hold Your Voice is not a generic AI humanizer. It is a voice-preservation
  layer around the writing.
- The benchmark is the writer's own samples, not a universal "good writing"
  style guide.
- Trust samples over stated preferences when they disagree.
- Rewrite only the lines that fail the voice or AI-pattern check.
- Preserve surrounding text unless the user explicitly asks for a full rewrite.
- Rough private-note texture beats polished founder cadence.

## Workflow

1. Identify the target writer and output format.
2. Find or ask for source samples. Prefer real writing from the current project:
   posts, emails, essays, docs, landing copy, changelog notes, founder notes.
3. Build a profile when no current profile exists:

   ```bash
   hyv profile \
     --name "project voice" \
     --out .hold-your-voice/voice-profile.json \
     <sample paths>
   ```

4. Scan the draft:

   ```bash
   hyv scan \
     --meta .hold-your-voice/voice-profile.meta.json \
     <draft path>
   ```

   Passing `--meta` skips patterns the system has learned are not applicable.

5. Rewrite by line, not by vibe:

   ```bash
   hyv rewrite-prompt \
     --profile .hold-your-voice/voice-profile.json \
     --meta .hold-your-voice/voice-profile.meta.json \
     <draft path>
   ```

6. Verify by rescanning the revised draft.

## Output Standard

When returning prose to the user, lead with the finished writing. Keep process
notes short. If you changed only flagged lines, say that plainly.

For project work, store generated profiles under:

```text
.hold-your-voice/voice-profile.json
```

Do not store private samples inside the plugin folder. Keep project-specific
profiles inside the project that owns the writing.

## Auto-Improvement (default)

The profile **evolves automatically** after every accepted writing session. No
manual reinforce or update commands needed.

### How it works

After the user accepts a revision, run **one command**:

```bash
hyv profile-evolve \
  --original <original draft file> \
  --accepted <accepted/output draft file> \
  --profile .hold-your-voice/voice-profile.json
```

Optional: `--new-samples <paths>` to merge new writing samples in the same step.
Optional: `--meta <path>` if you need a custom meta file location (defaults to
`voice-profile.meta.json` alongside the profile).

This does three things simultaneously:

1. **Signal extraction** — diffs original vs accepted to find which AI patterns
   the user agreed with (`patterns_accepted`) vs overrode (`patterns_overridden`).
2. **Temporal meta update** — each pattern now tracks `first_seen`,
   `last_confirmed`, `contradictions`, `confidence` (0.0–1.0), and status
   (`active` / `declining` / `stale`). Accepted signals boost confidence.
   Overrides penalize it. Untouched patterns slowly decay.
3. **Profile stat merge** — sentence length, paragraph shape, and opening moves
   use weighted rolling averages so the voice benchmark improves with every
   session.

### Pattern lifecycle

- **Active** — confidence ≥ 0.30, last confirmed within 14 days. These
  patterns fire during scans.
- **Declining** — 3+ contradictions and confidence < 0.30. Still tracked
  but no longer flagged in scan output.
- **Stale** — 5+ contradictions and confidence < 0.15, or untouched for
  > 14 days. Archived; does not fire.

This means after a few days of usage:

- Patterns the user consistently accepts (e.g., "inflated_verbs") become
  high-confidence and reliably flag real AI drift.
- Patterns the user consistently ignores (e.g., "the user's writing style
  uses landscape-era phrasing intentionally") quietly fade out.
- The profile's sentence/paragraph stats converge on the actual voice.

### Check learning state

```bash
hyv profile-status \
  --profile .hold-your-voice/voice-profile.json
```

Optional: `--write-voice voice.md` produces the human-readable voice profile
with confidence bars per pattern.

### Auto-sync to cloud (daily)

`profile-evolve` automatically tries to sync to Cloudflare R2 after each
evolution. Sync only happens if:

- The env vars `HYV_R2_ACCESS_KEY_ID`, `HYV_R2_SECRET_ACCESS_KEY`,
  `HYV_R2_ENDPOINT`, `HYV_R2_BUCKET` are set.
- The last sync was more than 23 hours ago (no wasteful pushes).
- The payload is under 1MB (safety cap).

To set up one-time:

```bash
export HYV_R2_ACCESS_KEY_ID="your-access-key"
export HYV_R2_SECRET_ACCESS_KEY="your-secret-key"
export HYV_R2_ENDPOINT="https://<account-id>.r2.cloudflarestorage.com"
export HYV_R2_BUCKET="hyv-voice-profiles"
pip install boto3  # only dependency
```

R2 has **zero egress fees**. With ~5-20KB profiles synced once daily, annual
cost rounds to zero. No Cloudflare Workers, no compute — just S3 PUT.

Manual sync (force override):

```bash
hyv-sync \
  --profile .hold-your-voice/voice-profile.json \
  --force
```

### Export and import

```bash
hyv profile-export \
  --profile .hold-your-voice/voice-profile.json \
  --out ~/my-voice.hyv

hyv profile-import \
  --profile .hold-your-voice/voice-profile.json \
  --source ~/my-voice.hyv
```

The learning is entirely local — no API calls, no third-party services.

