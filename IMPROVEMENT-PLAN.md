# HYV Improvement Plan: Detection & Output Quality

## Executive Summary

After analyzing the competitive landscape (GPTZero, Turnitin, Originality.ai, Walter Writes, StealthGPT, Ryne AI, WriteHuman, and 10+ other tools), the AI detection and humanizer market in 2026 has evolved significantly. HYV occupies a unique position — voice-preserving AI pattern detection with self-improving profiles — but has substantial gaps in detection sophistication and output quality that need addressing.

**HYV's core competitive advantage:** It's the only tool that detects AI patterns AND preserves the writer's specific voice. Every competitor is either a pure detector (GPTZero, Turnitin) or a generic humanizer (Walter, Ryne) that destroys voice in the process. This is the wedge. The plan doubles down on it.

---

## Part 1: Detection Improvements

### Current State
- 220+ regex patterns across 31 composite rules + 9 structural signals
- Surface-level pattern matching (word/phrase detection)
- Structural analysis: burstiness, paragraph uniformity, contraction density, formal hedging, intensifiers, fragment ratio
- Self-improving temporal pattern weights

### Gap Analysis vs. Competitors

| Detection Signal | GPTZero | Originality.ai | Turnitin | HYV (current) |
|---|---|---|---|---|
| Perplexity scoring | ✓ (primary) | ✓ (classifier input) | ✓ (AIR-1) | ✗ |
| Burstiness analysis | ✓ (primary) | ✓ | ✓ | ✓ (basic) |
| Neural classifier | ✓ | ✓ (transformer) | ✓ (AIR-1) | ✗ |
| Sentence-level highlighting | ✓ | ✗ | ✓ | ✓ |
| Vocabulary diversity metrics | ✓ | ✓ | ✓ | ✗ |
| N-gram analysis | implied | ✓ | ✓ | ✗ |
| Paraphrase resistance | moderate | 96.7% (RAID) | high | untested |
| Embedding similarity | unknown | ✓ | ✓ | ✗ |

### Detection Improvements (Priority Order)

#### D1. Add Perplexity Proxy Scoring
**Why:** Every major detector uses perplexity as a primary signal. HYV ignores it entirely.

**What:** Implement a lightweight perplexity estimation without requiring a full LLM:
- Use character-level and word-level n-gram frequency analysis against a reference corpus
- Score each sentence for "predictability" based on common bigram/trigram transitions
- Flag sentences with unusually low perplexity (highly predictable = AI-like)
- Use a bundled reference frequency table (pre-computed from diverse human writing)

**Implementation approach:**
```python
def estimate_perplexity_proxy(sentence: str, freq_table: dict) -> float:
    """Estimate perplexity using bigram transition frequencies."""
    tokens = tokenize(sentence)
    bigrams = list(zip(tokens[:-1], tokens[1:]))
    log_prob = sum(
        -math.log2(freq_table.get(bigram, freq_table.get("<unk>", 1e-6)))
        for bigram in bigrams
    )
    return log_prob / max(1, len(bigrams))
```

- Bundle a ~2MB reference frequency table (pre-computed from Project Gutenberg, Wikipedia, diverse blogs)
- Add `perplexity_proxy` to each flagged line in scan output
- Include threshold calibration per content domain

#### D2. Vocabulary Diversity Scoring
**Why:** AI text has measurably lower vocabulary diversity than human text. GPTZero and Originality.ai both use this.

**What:** Add per-paragraph and per-document metrics:
- Type-token ratio (TTR) — unique words / total words
- Hapax legomena ratio — words appearing exactly once / total words
- Vocabulary richness score (Yule's K or similar)
- Flag paragraphs with suspiciously uniform vocabulary

**Thresholds:**
- TTR < 0.45 on paragraphs > 50 words = flag
- Yule's K > 200 = unusually repetitive (AI-like)
- Hapax ratio < 0.40 = low lexical diversity

#### D3. N-gram Repetition Detection
**Why:** AI models repeat specific n-gram patterns at rates humans don't. Current detection misses this entirely.

**What:** 
- Track trigram and 4-gram frequencies across the document
- Flag repeated trigrams that appear 3+ times in a document (humans vary phrasing)
- Detect "AI echo" — where the same syntactic structure repeats across paragraphs
- Add `ngram_echo` as a new structural signal

#### D4. Sentence Probability Gradient Analysis
**Why:** Human writing has high variance in sentence "surprise" — some sentences are predictable, others are creative. AI writing has flat gradients.

**What:**
- Score each sentence's novelty relative to the preceding sentence
- Compute the variance of the novelty gradient across the document
- Low variance = flat gradient = AI-like
- This is HYV's burstiness concept but at the semantic level, not just length

#### D5. AI Vocabulary Density Expansion
**Why:** The current `ai_vocab_density` regex catches obvious words but misses newer AI patterns and context-dependent usage.

**What:**
- Add 50+ new terms that have emerged in 2025-2026 AI output (model-specific fingerprints)
- Add context-aware detection: "leverage" alone isn't AI, but "leverage the power of" is
- Track phrase co-occurrence patterns (3+ AI-buzzwords in a single sentence)
- Add per-model fingerprinting: GPT-4o vs Claude vs Gemini have different vocab tendencies

**New terms to add:**
```
tapestry (already caught), but also: 
- "in the realm of"
- "it's worth diving into"
- "the intersection of"
- "a nuanced understanding"
- "the broader implications"
- "shed light on" (already caught, expand context)
- "robust framework" (compound detection)
- "inherently"
- "underscores"
- "arguably"
- "notably"
- "intrinsically"
- "fundamentally"
```

#### D6. Cross-Pattern Density Scoring
**Why:** Individual pattern matches are weak signals. The *density* of multiple patterns in proximity is a strong signal.

**What:**
- Compute a "pattern density score" per paragraph: (number of distinct pattern hits) / (paragraph word count)
- Paragraphs with density > 0.05 (5% of words trigger patterns) = high-confidence AI flag
- This reduces false positives (a single "let's dive in" doesn't mean AI, but "let's dive in" + "robust" + "in the realm of" in one paragraph does)

#### D7. Structural Signal Additions

**New structural signals:**
- **List uniformity**: AI lists tend to have items of identical length and structure. Measure coefficient of variation across list item lengths.
- **Transition predictability**: AI uses formulaic transitions (Furthermore, Moreover, In addition). Track transition variety.
- **Quote/attribution absence**: AI rarely uses direct quotes. Flag documents > 500 words with zero quotes.
- **Specificity score**: Count proper nouns, numbers, dates, specific names. AI text is measurably less specific.
- **Hedging-to-assertion ratio**: AI hedges more than humans. Track "might/could/perhaps" density vs. definitive statements.

---

## Part 2: Output Quality Improvements

### Current State
- Generates a rewrite prompt for external LLM execution
- Line-level precision (flagged lines only)
- Voice profile constrains the rewrite
- No direct rewriting capability
- No preview or iteration

### Gap Analysis vs. Competitors

| Output Feature | Walter Writes | Ryne AI | StealthWriter | HYV (current) |
|---|---|---|---|---|
| Direct rewriting | ✓ | ✓ | ✓ | ✗ (prompt only) |
| Sentence alternatives | ✗ | ✓ | ✓ | ✗ |
| Voice preservation | partial | partial | ✗ | ✓ (unique) |
| Real-time preview | ✓ | ✓ | ✓ | ✗ |
| Tone modes | ✓ | ✓ (10+ models) | ✓ (3 modes) | ✗ |
| Detection verification | built-in | built-in | ✗ | ✗ |
| Self-improving | ✗ | ✗ | ✗ | ✓ (unique) |

### Output Improvements (Priority Order)

#### O1. Built-in Detection Verification Loop
**Why:** Every successful humanizer (Walter, Ryne, WriteHuman) has built-in verification. HYV generates a rewrite but never verifies it worked.

**What:**
- After rewrite, automatically re-scan the output
- If AI patterns remain, flag them and suggest second-pass rewrites
- Add `hyv verify` command: scan → rewrite → re-scan → report delta
- Show before/after pattern count comparison

```bash
hyv verify draft.md
# Output: 
# Before: 23 AI patterns detected
# After:  3 AI patterns detected (87% reduction)
# Remaining:
#   - line 14: ai_vocab_density ("underscore")
#   - line 27: founder_cadence ("here's the thing")
#   - line 41: em_dash
```

#### O2. Sentence-Level Alternative Generation
**Why:** StealthWriter's killer feature is clicking on a sentence and cycling through alternatives. This is table-stakes for 2026 humanizers.

**What:**
- For each flagged line, generate 3 alternative rewrites
- Rank alternatives by: (a) voice profile match, (b) pattern reduction, (c) meaning preservation
- Add `--alternatives N` flag to `rewrite-prompt` command
- Output format: JSON array of alternatives per line

#### O3. Rewrite Quality Scoring
**Why:** HYV rewrites blindly — it has no idea if the output is actually better.

**What:**
- Score each rewrite on three axes:
  - **Voice match**: cosine similarity to voice profile anchors (0-1)
  - **Pattern reduction**: how many AI patterns were eliminated
  - **Meaning preservation**: semantic similarity to original (using simple overlap metrics)
- Include scores in rewrite output
- Reject rewrites that score below thresholds

#### O4. Domain-Specific Rewrite Modes
**Why:** Walter Writes and StealthWriter offer tone modes. A blog post needs different rewriting than a technical doc.

**What:**
- Add `--mode` flag: `blog`, `email`, `technical`, `social`, `academic`, `default`
- Each mode adjusts:
  - Acceptable vocabulary complexity
  - Sentence length targets
  - Formality level
  - Which patterns to aggressively target vs. tolerate
- Blog mode: tolerate contractions, casual openers, shorter sentences
- Technical mode: tolerate domain jargon, longer sentences, passive voice
- Social mode: maximize lowercase, minimal structure, no lists

#### O5. Inline Diff Output
**Why:** Users need to see exactly what changed. Current output is a prompt — they never see the actual diff.

**What:**
- Add `--diff` flag to show inline changes
- Use standard diff format (red/green) for terminal output
- For JSON output, include original line alongside replacement
- Add `--accept` / `--reject` per-line interactive mode

#### O6. Rewrite Confidence Calibration
**Why:** Some rewrites are confident (clear AI pattern → clear fix). Others are uncertain (ambiguous pattern, context-dependent). Users should know the difference.

**What:**
- Tag each rewrite with confidence: `high`, `medium`, `low`
- High: direct pattern match, clear replacement (e.g., "leverage the power of" → "use")
- Medium: pattern detected but replacement is context-dependent
- Low: structural signal (e.g., low burstiness) — no line-level fix available
- Low-confidence rewrites should suggest structural changes, not line edits

---

## Part 3: Voice Profiling Improvements

### Current State
- Statistical profiling: sentence length, paragraph shape, case style, argument pattern
- Opening move extraction
- Anchor paragraph selection
- Temporal pattern confidence tracking (self-improving)

### Profiling Improvements

#### V1. Vocabulary Fingerprint
**Why:** The most distinctive aspect of a writer's voice is their word choices. Current profiling ignores this.

**What:**
- Extract top 50 distinctive words/phrases (highest TF-IDF vs. a general corpus)
- Track preferred sentence starters (first 2-3 words of paragraphs)
- Identify "signature phrases" — recurring 2-4 word combinations unique to the writer
- Use this fingerprint to constrain rewrites: prefer words from the writer's vocabulary

#### V2. Emotional Tone Mapping
**Why:** Writers have consistent emotional registers. AI text tends toward neutral-positive. Profiling should capture the writer's emotional range.

**What:**
- Score each sample on simple axes: formality (1-10), energy (1-10), cynicism (1-10)
- Use keyword-based scoring (not sentiment analysis ML)
- Profile stores the writer's typical range
- Rewrites that drift outside the range get flagged

#### V3. Rhythm Fingerprint
**Why:** Current profiling captures average sentence length and variance. But rhythm is more than that — it's about the *pattern* of short and long sentences.

**What:**
- Capture the typical sentence length sequence pattern (e.g., "long-short-medium-short" vs "medium-medium-medium")
- Store as a Markov transition matrix: P(next_length | current_length)
- Use this to validate that rewrites match the writer's rhythm pattern
- Flag rewrites that violate the rhythm transition probabilities

#### V4. Format-Specific Profiles
**Why:** The same writer sounds different in tweets vs. blog posts vs. emails. One profile per writer isn't enough.

**What:**
- Allow multiple profiles per project: `voice-profile.email.json`, `voice-profile.blog.json`
- Add `--format` flag to `hyv profile` to tag samples by format
- Scan and rewrite commands automatically select the right profile based on detected format
- Fall back to general profile when format is ambiguous

#### V5. Profile Strength Scoring
**Why:** A profile built from 3 short samples is weaker than one built from 15 long samples. Users should know how reliable their profile is.

**What:**
- Compute and display a "profile strength" score (0-100)
- Based on: source count, total word count, diversity of samples, recency of samples
- Display in `profile-status` output
- Warn when scan/rewrite is using a weak profile (< 50 strength)

---

## Part 4: Architecture & Distribution Improvements

#### A1. Perplexity Reference Data Bundling
- Pre-compute and bundle a compressed bigram/trigram frequency table (~2MB)
- Use it for perplexity proxy calculations
- Allow users to provide their own reference corpus for domain-specific calibration

#### A2. Incremental Pattern Database
- Ship a `patterns.json` that can be updated independently of the main script
- Users can add custom patterns: `hyv add-pattern "my_company_catchphrase" --regex "..."`
- Community pattern sharing: `hyv patterns export` / `hyv patterns import`

#### A3. Editor Integration Hooks
- Add `hyv watch <file>` — continuous scan on file change
- Output JSON that editors can consume (VS Code extension, etc.)
- Add `--format editor-json` for structured output with line numbers and quick-fix suggestions

#### A4. Web UI (Stretch)
- Simple local web UI for scan results visualization
- Before/after comparison with highlighted changes
- Voice profile visualization (confidence bars, pattern lifecycle)

---

## Implementation Priority

### Phase 1: Detection Foundation (Highest Impact)
1. **D1** — Perplexity proxy scoring (closes the biggest gap vs. competitors)
2. **D2** — Vocabulary diversity scoring (TTR, Yule's K)
3. **D5** — AI vocabulary density expansion
4. **D6** — Cross-pattern density scoring
5. **V1** — Vocabulary fingerprint (enables better rewrite constraints)

### Phase 2: Output Quality
6. **O1** — Built-in verification loop
7. **O3** — Rewrite quality scoring
8. **V3** — Rhythm fingerprint
9. **O2** — Sentence-level alternatives
10. **O5** — Inline diff output

### Phase 3: Advanced Detection
11. **D3** — N-gram repetition detection
12. **D4** — Sentence probability gradient analysis
13. **D7** — Structural signal additions
14. **V2** — Emotional tone mapping

### Phase 4: Polish & Distribution
15. **O4** — Domain-specific rewrite modes
16. **V4** — Format-specific profiles
17. **V5** — Profile strength scoring
18. **A2** — Incremental pattern database
19. **O6** — Rewrite confidence calibration
20. **A3** — Editor integration hooks

---

## Competitive Positioning Statement

**For writers and content creators who use AI but don't want to sound like AI, HYV is the only tool that detects AI patterns while preserving your specific voice — and gets better at it every time you use it.**

Unlike generic humanizers (Walter, Ryne, StealthGPT) that rewrite your text into generic "human-sounding" prose, HYV learns YOUR voice from YOUR writing samples and only fixes the lines that drifted. Unlike pure detectors (GPTZero, Turnitin) that just flag problems, HYV fixes them — surgically, not wholesale.

The self-improving profile system means HYV is the only tool that adapts to YOUR writing over time. Patterns you consistently accept get stronger. Patterns you override fade away. After a week of use, HYV knows your voice better than any generic humanizer ever could.

---

## Key Metrics to Track

- **Detection accuracy**: Test against the same 500-essay corpus used in the StudySolutions benchmark
- **False positive rate**: Especially on ESL writers and technical prose
- **Paraphrase resistance**: Can HYV catch AI text that has been paraphrased by QuillBot?
- **Voice preservation score**: Human evaluation — does the rewritten text still sound like the original writer?
- **Pattern reduction rate**: Average % of AI patterns eliminated per rewrite
- **Profile convergence**: How many sessions before the profile stabilizes?

---

## What NOT to Do

1. **Don't build a neural classifier.** HYV's strength is zero-dependency, local-first, transparent detection. Adding ML models destroys that positioning. Leave neural classifiers to GPTZero and Originality.ai.
2. **Don't become a generic humanizer.** The market is flooded with them. HYV's wedge is voice preservation + self-improvement. Don't dilute it.
3. **Don't add API dependencies.** The rewrite prompt approach (output a prompt for external LLM) is actually a strength — it means HYV works with any model, no API keys needed. Keep this.
4. **Don't chase detection evasion.** HYV should help writers sound like themselves, not help them game detectors. The framing matters.
5. **Don't add bloat.** Keep the zero-dependency, single-file Python script ethos. Every feature should work offline.
