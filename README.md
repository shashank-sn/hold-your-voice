# Hold Your Voice

Portable writing-voice toolkit. Works in any AI coding tool or terminal.
Zero dependencies outside Python 3.10+.

- build a voice profile from a writer's own samples
- scan drafts for AI-writing patterns (220+ rules across 31 regex patterns)
- rewrite only the flagged lines — no flattening
- **profile evolves with every session** — patterns you accept get stronger,
  patterns you ignore fade away
- auto-sync profiles to Cloudflare R2 for backup (near-zero cost)

## Install

```bash
npm install -g hold-your-voice
```

Or clone and run directly:

```bash
git clone https://github.com/holdyourvoice/hold-your-voice.git
cd hold-your-voice
python3 scripts/hold_voice.py --help
```

## Quick start

### 1. Build a voice profile

```bash
hyv profile \
  --name "my voice" \
  --out .hold-your-voice/voice-profile.json \
  path/to/writing-samples/
```

### 2. Scan a draft for AI patterns

```bash
hyv scan --meta .hold-your-voice/voice-profile.meta.json draft.md
```

### 3. Rewrite flagged lines only

```bash
hyv rewrite-prompt \
  --profile .hold-your-voice/voice-profile.json \
  --meta .hold-your-voice/voice-profile.meta.json \
  draft.md
```

### 4. After user accepts the revision, evolve the profile

```bash
hyv profile-evolve \
  --original draft.md \
  --accepted accepted.md \
  --profile .hold-your-voice/voice-profile.json
```

This automatically diffs original vs accepted, extracts which patterns the user
kept and which they overrode, updates temporal confidence weights, merges new
stats, and **auto-syncs to Cloudflare R2** if configured.

## Cloud sync (optional)

Set once:

```bash
export HYV_R2_ACCESS_KEY_ID="your-access-key"
export HYV_R2_SECRET_ACCESS_KEY="your-secret-key"
export HYV_R2_ENDPOINT="https://<account>.r2.cloudflarestorage.com"
export HYV_R2_BUCKET="hyv-voice-profiles"
pip install boto3
```

`profile-evolve` auto-syncs after every session (> 23h since last sync).
R2 has zero egress fees. With ~20KB profiles, annual cost is $0.

## What the learning does

After a few days of use:

- `ai_vocab_density` — confidence 0.76 → reliably catches AI-speak
- `inflated_verbs` — confidence 0.32 → user removes most of these
- `em_dash` — confidence 0.08 → user uses em dashes, pattern auto-suppressed

Patterns track `first_seen`, `last_confirmed`, per-date contradictions,
`status` (active/declining/stale), and `source_samples` for full provenance.
Untouched patterns decay over 14 days. Contradicted patterns drop to declining
after 3 overrides, stale after 5.

## Commands

| Command | What it does |
|---------|-------------|
| `hyv profile` | Build voice profile from samples |
| `hyv scan` | Flag AI-writing patterns in a draft |
| `hyv rewrite-prompt` | Generate line-level rewrite prompt |
| `hyv profile-evolve` | **Auto-evolve** — extract signals + update meta + merge stats |
| `hyv profile-update` | Merge new samples into existing profile (rolling averages) |
| `hyv profile-status` | Pretty-print learning state with confidence bars |
| `hyv reinforce` | Diff original vs accepted, emit signal report |
| `hyv profile-export` | Bundle profile into .hyv file |
| `hyv profile-import` | Import .hyv bundle |
| `hyv-sync` | Manually sync to R2 (runs automatically via evolve) |

## Why `.hold-your-voice/`

Profiles live in your project. They're not hidden in `~/.codex/` or `~/.commandcode/` —
they're in `.hold-your-voice/` at the root of whatever project you're writing for.
Portable. Version-control-able. No global state.

## Changelog

### 0.2.0 — auto-improving profiles

- `profile-evolve` replaces manual reinforce + update — one command per session
- Temporal pattern confidence tracking (active/declining/stale lifecycle)
- `scan --meta` and `rewrite-prompt --meta` filter out learned-not-applicable patterns
- Voice.md as standard readable output (`profile-status --write-voice`)
- Auto-sync to Cloudflare R2 with daily rate-limiting and 1MB safety cap
- Universal `hyv` / `hyv-sync` CLI — works in any tool, not just Codex

### 0.1.0 — initial

- `profile`, `scan`, `rewrite-prompt` commands
- 220+ AI-writing pattern detection (31 regex + 9 structural signals)
- `reinforce`, `profile-update`, `profile-export/import`

