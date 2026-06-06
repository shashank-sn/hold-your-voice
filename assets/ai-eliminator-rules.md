# AI Eliminator Rules (v2 — 220+ patterns + structural signals)

Use these rules to remove AI-generated cadence without erasing the writer.

## Core Rule

Fix the exact line that drifted. Do not rewrite a whole draft when one sentence
is the problem. Preserve clean surrounding lines.

## Detection Coverage

The algorithm now detects 220+ named AI writing patterns organized across 31
composite regex rules, plus structural/rhythmic analysis of: burstiness
(sentence length variance), paragraph rhythm uniformity, contraction density,
formal hedging, generic intensifiers, fragment ratio, over-structured list
patterns, and uniform sentence rhythm within paragraphs.

## Banned Pattern Categories

### Binary reframing & negation (#1, #210-212)
- "It's not X, it's Y" / "The point isn't X, it's Y"
- "You don't need X, you need Y"
- "Not just X, but Y" / "Not only... but also"

### Staccato drama (#2, #95, #96)
- Short punchy sentence runs: "No X. No Y. Just Z."
- Perfectly even sentence rhythm throughout paragraphs
- Three short sentences in a row (performance cadence)

### Landscape/era grandstanding (#3, #181-188)
- "In today's fast-paced world" / "ever-evolving landscape"
- "Now more than ever" / "as never before"
- "Has never been more important"
- "In the digital age" / "new era of X"
- "The rise of X" / "increasingly + adjective"

### Truth/reality posturing (#22, #110, #161-163)
- "The truth is" / "the reality is" / "here's the truth"
- "The harsh/ugly/brutal reality" / "real talk"
- "Brutal honesty" / "reality check"

### Hedging & non-committal (#4, #53-55, #89, #197-199)
- "It depends, but" / "no one-size-fits-all"
- "It can be tempting to" / "you might be tempted to"
- "In many ways" / "at first it might seem"

### Transitions & balance (#7, #38-40, #81, #91, #203)
- "On the one hand / on the other hand"
- "On the flip side" / "that said" / "however"
- "Moreover / furthermore / in addition" chains
- "At first glance vs on closer inspection"

### Let's/invitation patterns (#5, #63-65, #80, #127)
- "Let's dive in" / "let's explore" / "let's break it down"
- "Delve into" / "dive deeper" / "deep dive"
- "Navigate the complex landscape"

### Empathy opener (#21, #74-75, #107, #164-165)
- "It's easy to feel X" / "you're not alone"
- "You're not imagining it" / "you deserve"
- "Shouting into the void"

### Founder/thought-leader cadence (#72-73, #104-109)
- "Here's the thing" / "and honestly?"
- "Here's the kicker" / "the part most people miss"
- "What nobody's saying" / "the best part?"
- "Same X. Better Y." / "the moment X becomes Y"

### Marketing verbs (#61-62, #83, #114-117, #145-150)
- "Unlock the power of" / "harness the power of"
- "Transform/elevate/take to the next level"
- "Master the art of" / "game-changer"
- "Supercharge / turbocharge / on steroids"

### Journey/destination clichés (#59, #84, #122, #144, #214-215)
- "X isn't a destination; it's a journey"
- "No matter where you are on your journey"
- "Embark on" / "you're still early" / "it's still day one"

### Metaphor clusters (#18, #120-121, #159-160, #167-168, #173-180)
- "Beacon / lighthouse / tapestry / symphony / tides"
- "Silent killer / hidden gem / tip of the iceberg"
- "North star / double-edged sword / blessing and a curse"
- "Noise vs signal" / "X is the new Y"
- "Flood / avalanche / tsunami of X"

### Guide/article framing (#11-13, #27-28, #136-138)
- "You're in the right place" / "here's a step-by-step guide"
- "First, second, third" / "key takeaways" / "actionable tips"
- "In this article/guide/post" / "this piece explores"

### Wrapping/closing (#9, #14-15, #51-52, #66, #93, #103, #189, #217)
- "At the end of the day" / "the bottom line is"
- "In conclusion / in summary / to recap"
- "Let that sink in" / "only time will tell"
- "Curious what others think" / "let me know if you need help"

### UX/business buzzwords (#92, #123-126, #155-157)
- "Robust, scalable, innovative, impactful"
- "Seamless experience" / "frictionless journey"
- "Pain points" / "wealth of insights"

### Story/temporal templates (#17, #32-33, #113, #216, #218-219)
- "Imagine this / picture this"
- "Storytelling has been around for centuries"
- "Little did I know" / "at first I was skeptical"
- "The best time was X, the second-best time is now"

## Structural Signals (Beyond Individual Words)

- **Low burstiness**: Sentence lengths all similar (coefficient of variation < 0.35)
- **Mechanical paragraphs**: All paragraphs nearly identical sentence count
- **Over-structured lists**: Rigid 3-item lists throughout
- **Uniform paragraph rhythm**: Most sentences fall in 12-22 word range
- **Low contractions**: < 0.8 contractions per 100 words (overly formal)
- **Formal hedging density**: 2+ institutional hedging phrases
- **Generic intensifiers**: 3+ "remarkably/incredibly/amazingly" instances
- **No fragments**: Zero sentence fragments in 20+ sentences (over-polished)

## What To Do Instead

- Start from rough private-note material: an exact edit, meeting fragment,
  dashboard annoyance, customer confusion, half-remembered sentence, or internal
  contradiction.
- Let the idea move because the logic moves, not because line breaks perform.
- Prefer concrete scenes, mechanisms, quoted language, and specific stakes.
- Let some pieces end on a detail, hesitation, unresolved thought, or awkwardly
  specific observation.
- If a line sounds like a maxim, a carousel, or a model trying to be sharp,
  make it plainer and more grounded.
