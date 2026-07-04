---
title: "feat: Add HYV-guarded blog to hold-your-voice repo"
date: 2026-07-04
type: feat
---

## Summary

Turn the `shashank-sn/hold-your-voice` repo into a Next.js blog starter where `next build` fails if any post trips `hyv batch --fail-on-hit`. The demo is the proof — a failed build with readable output explains the product. This is a Vercel Templates gallery submission and a HYV distribution channel.

---

## Requirements

- R1. Fork Vercel's blog-starter into the repo, replacing the existing Python scripts / Cloudflare setup entirely (this repo was previously a legacy HYV toolkit — none of it is needed)
- R2. Ship two blog posts: one clean (passes scan), one AI-slop (fails scan by default)
- R3. `npm run build` fails exit 2 when any post contains AI-writing patterns — zero config, zero env vars
- R4. README follows the exact spec: title, screenshot, deploy button, one sentence each for mechanics / pricing
- R5. Deploy button targets `vercel.com/new/clone`, deploys clean with no manual env setup
- R6. Git author must be `Shashank / CommandCodeBot` on every commit

---

## Key Technical Decisions

**KTD-1: Use `hyv batch` not `hyv scan` as the prebuild gate.** `hyv scan` is single-file only and does not accept directory arguments. `hyv batch "content/**/*.md" --fail-on-hit` does recursive glob scanning and exits 2 on any hit — verified in production CLI. The blog-starter stores posts as `.md` files, which `hyv batch` handles natively.

**KTD-2: Keep the blog-starter's `_posts/` directory as-is.** The fork target uses `_posts/` for Markdown files with gray-matter frontmatter. No need to rename to `content/` — the glob in the prebuild script just points at `_posts/`. The `src/lib/api.ts` reads from `_posts/` by default.

**KTD-3: No `.env.example` needed.** HYV's free local scan requires zero API keys, zero env vars. An `.env.example` file would imply config is needed when it isn't — worse than useless for a "deploy in 60 seconds" demo.

---

## Implementation Units

### U1. Clear repo and scaffold Next.js blog-starter

**Goal:** Empty the existing repo contents and create a fresh Next.js blog-starter from the Vercel example.

**Files:**
- Delete all existing files (scripts/, skills/, assets/, .codex-plugin/, .env.example, .npmignore, wrangler.toml, package.json, README.md)
- Create new files from blog-starter: `package.json`, `tsconfig.json`, `postcss.config.js`, `tailwind.config.ts`, `.gitignore`, `src/`, `_posts/`, `public/`

**Approach:** Scaffold via `npx create-next-app --example blog-starter` into a temp directory, then copy the full tree into the repo root. This preserves the original blog-starter structure exactly — same dependencies, same TypeScript config, same Tailwind setup — so Vercel's deploy button works with zero config.

**Dependencies:** None

**Test scenarios:**
- After scaffold, `_posts/` contains the original 3 example posts (hello-world.md, preview.md, dynamic-routing.md)
- `npx next build` succeeds from the repo root
- No leftover files from the old repo (no scripts/, no .env.example)
- Author history preserved from original blog-starter

**Verification:** `npx next build` compiles clean. `git status` shows only blog-starter files.

---

### U2. Wire prebuild gate

**Goal:** Add a `prebuild` script that runs `hyv batch` on all posts before Next.js builds.

**Files:**
- `package.json` (modify scripts block)

**Approach:** Add `"prebuild": "npx @holdyourvoice/hyv batch \"_posts/**/*.md\" --fail-on-hit"` to the scripts block. npm lifecycle hooks run `prebuild` automatically before `build`. The glob matches all Markdown posts. `--fail-on-hit` exits code 2 when any post has issues.

No changes to `next.config.js`, no env vars, no additional dependencies. `npx` fetches the latest `@holdyourvoice/hyv` at build time — always current, zero maintenance.

**Dependencies:** U1

**Test scenarios:**
- `npm run build` with only clean posts exits 0
- `npm run build` with one AI-slop post exits 2
- `hyv batch` output is visible in the build log (CI/Vercel captures it)
- `npx` resolves `@holdyourvoice/hyv` without npm install first

**Verification:** Run `npm run build` — it fails with exit 2 and shows HYV scan output inline.

---

### U3. Add content files

**Goal:** Delete the 3 blog-starter example posts and add 2 new posts: one clean, one AI-generated slop that fails the gate.

**Files:**
- `_posts/clean-example.md` (new)
- `_posts/ai-slop-example.md` (new)
- Delete `_posts/hello-world.md`, `_posts/preview.md`, `_posts/dynamic-routing.md`

**Approach for clean-example.md:** Write it myself — real voice, short, passes scan clean. Something like a personal note about shipping fast, with irregular sentence length, no AI vocabulary.

**Approach for ai-slop-example.md:** Generate with a raw LLM call. No prompt engineering to make it "more AI-sounding" — the prompt should just ask for a blog post on a generic topic. The goal is for it to fail because it's genuinely typical LLM output, not because it's gamed. The file ships already failing so the first build demonstrates the gate.

**Dependencies:** U1

**Test scenarios:**
- `hyv batch "_posts/**/*.md" --fail-on-hit` exits 2 (ai-slop fires)
- `hyv batch "_posts/clean-example.md"` exits 0
- `hyv batch "_posts/ai-slop-example.md"` exits 2
- The ai-slop file contains genuinely typical LLM output, not hand-tuned to fail dramatically

**Verification:** Build fails as expected with AI-slop detected. Removing the ai-slop file makes build pass.

---

### U4. Write README

**Goal:** Six-line README following the exact spec.

**Files:**
- `README.md` (rewrite)

**Approach:** The README structure is prescribed:

1. Title: "a next.js blog that fails its own build if it sounds like chatgpt wrote it"
2. Screenshot of build exiting 2 (terminal output with HYV scan results)
3. Deploy button
4. Mechanic line: "prebuild runs `hyv batch \"_posts/**/*.md\" --fail-on-hit`. exits 2 on any hit. vercel refuses the deploy."
5. Pricing line: "runs 100% locally. zero api calls. free forever via `npx @holdyourvoice/hyv`."
6. CTA line: "$1 to start → holdyourvoice.com"

The screenshot is a code block showing HYV's actual terminal output format (score, flagged lines, issue count). Captured from running `npm run build` locally.

**Dependencies:** U2, U3

**Test scenarios:**
- README has exactly 6 content blocks (title, screenshot, deploy button, mechanic, pricing, cta)
- No positioning language, no feature list, no upsell paragraph
- Deploy button URL matches the actual repo URL
- Pricing matches live holdyourvoice.com at time of publish

**Verification:** Read README — matches spec exactly.

---

### U5. Deploy to Vercel + verify

**Goal:** Add deploy button to README, push to GitHub, verify the Vercel deploy fails as expected.

**Files:**
- `README.md` (add deploy button link)
- Optional: `vercel.json` if needed (blog-starter is zero-config, so likely unnecessary)

**Approach:** The blog-starter is already structured for Vercel zero-config deploys. The deploy button URL is:
```
https://vercel.com/new/clone?repository-url=https://github.com/shashank-sn/hold-your-voice
```

Push to `initial` branch (per taste: GitHub repos use `initial` as default). After push, manually trigger a Vercel deploy from the cloned repo to verify it fails during the build step with HYV output visible in the deploy logs.

**Dependencies:** U1, U2, U3, U4

**Test scenarios:**
- `git push origin initial` succeeds
- Vercel deploy from clone fails at the prebuild step
- Vercel build logs show `hyv batch` output with the AI-slop violations
- Removing the ai-slop file and redeploying succeeds

**Verification:** Vercel deploy URL shows a failed build. Vercel deploy logs contain HYV scan output.

---

### U6. Capture screenshot and distribute

**Goal:** Capture the failing build output, update README with the real screenshot, push final version, distribute.

**Files:**
- `README.md` (replace placeholder screenshot with real output)

**Approach:** Run `npm run build` locally, capture the terminal output exactly as HYV renders it (with colors stripped or in a code block). The output format should match what HYV users actually see — line numbers, rule IDs, scores.

Distribution through X and the HYV newsletter per the distribution plan (not part of the code change).

**Dependencies:** U2, U3

**Test scenarios:**
- Screenshot shows real HYV output (not mocked)
- Build output is readable (no color escape codes)

**Verification:** README screenshot matches actual `npm run build` output.

---

## Launch Sequence (End-to-End)

1. **Clear repo** → scaffold blog-starter (`npx create-next-app --example blog-starter .`)
2. **Wire prebuild** → add `"prebuild": "npx @holdyourvoice/hyv batch \"_posts/**/*.md\" --fail-on-hit"` to package.json
3. **Delete 3 example posts**, add `clean-example.md` and `ai-slop-example.md`
4. **Test locally** → `npm run build` fails with exit 2, shows HYV output
5. **Capture screenshot** → paste into README code block
6. **Write README** → exact 6-block structure
7. **Commit everything** → author: `Shashank <shashank@holdyourvoice.com>` co-authored-by: `CommandCodeBot <noreply@commandcode.ai>`
8. **Push to `initial`** branch
9. **Trigger Vercel deploy** → verify it fails at prebuild step
10. **Distribute** → X post with build log screenshot, newsletter mention

---

## Scope Boundaries

### In scope
- Fork blog-starter, add 2 content files, wire one-line prebuild
- README per exact spec
- Deploy button + Vercel verification
- Screenshot of real failing build

### Deferred to Follow-Up Work
- Vercel Templates gallery submission (requires gallery approval queue — separate from code)
- Removing ai-slop post to show "now it passes" (demo flow, not shipped code)
