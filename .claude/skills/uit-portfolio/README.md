# uit-portfolio — developer & maintainer guide

A Claude **skill** that guides OSU UIT staff and business partners through writing
a high-quality **Concept/Idea Brief** or **Project Charter** for the UIT Portfolio
Management process, and emits a filled `.docx` in the official template.

This README is for the humans who maintain and deploy the skill. The runtime
instructions the model follows live in `SKILL.md`; this document explains the
*why*, the architecture it plugs into, the data-handling rules, and how it was
validated.

---

## Where it runs (application architecture)

The skill is the **brain** of a web chat application. The app is modeled on
[`dirkpetersen/codecheck`](https://github.com/dirkpetersen/codecheck):

- **Backend:** Python / FastAPI.
- **Engine:** the app shells out to Claude Code
  (`claude --output-format stream-json --verbose`) and streams the agent's tool
  calls and output to a browser chat over **SSE** (server-sent events) — the user
  watches the assistant work in real time.
- **Model backend:** Claude Code pointed at **AWS Bedrock**
  (`CLAUDE_CODE_USE_BEDROCK=1`), so inference stays inside an OSU-approved
  boundary. The skill is model-agnostic and behaves identically on the Anthropic
  API if that path is ever approved.
- **Inputs:** the user uploads a `.docx`/`.pptx`/`.xlsx`/`.pdf` or types an idea;
  the app hands the file(s) + chat to Claude Code, which loads this skill.
- **State:** **stateless** — the session produces a downloadable `.docx`; nothing
  is persisted server-side.

The app supplies the harness and the streaming UI; **all domain logic lives in
this skill**, so the process can evolve here without touching the app.

---

## How it works (runtime summary)

Full detail is in `SKILL.md`. In brief, two auto-detected modes:

- **Concept Brief mode** (default, Stage 1): idea or early document → brief.
- **Charter mode** (Stage 2): a brief that came back **with reviewer comments** →
  charter. The trigger is the presence of `word/comments.xml` in an uploaded Word
  brief (Word stores comments separately from body text, so this is a clean signal).

Five steps: **determine mode → ingest & map → interview (asking the questions
reviewers will ask) → generate the `.docx` → deliver a private readiness summary.**

### File map

| Path | Purpose |
|------|---------|
| `SKILL.md` | Runtime instructions for the model (kept lean) |
| `references/process-overview.md` | The 4-stage governance process + the boundaries the assistant must respect |
| `references/reviewer-questions.md` | **The core value:** the questions UIT reviewers actually ask, to raise proactively in the interview — split into Tier 1 (brief) and Tier 2 (charter) so brief mode stays lightweight |
| `references/rubric.md` | Per-section quality rubric + strong/weak patterns observed in real submissions |
| `references/charter-fields.md` | Charter template field map + python-docx filling guide |
| `scripts/fill_brief.py` | Fills the brief template from a JSON content map (tested) |
| `assets/*.docx` | **Blank** official templates only (author metadata scrubbed) |

---

## Design decisions & rationale

- **One skill, two modes** rather than two skills — brief and charter share
  ingestion, the rubric, and the reviewer-question machinery, and the stage is
  auto-detectable.
- **Comment-detection trigger** for charter mode — concrete and reliable; mirrors
  the real workflow ("it came back from review, now charter it").
- **Real `.docx` in the official template** — reviewers trust a correctly
  formatted artifact far more than chat text. `fill_brief.py` preserves the
  template's styling and leaves the reviewer/decision rows blank.
- **Reviewer-anticipation is the point.** The tool's job is to surface the
  weaknesses a reviewer would flag *before* they do. The interview is driven by
  `references/reviewer-questions.md`, distilled from real reviewer feedback.
- **Two hard rules, everywhere:** (1) **never invent facts** — funding, dates,
  names, HECVAT/procurement answers come from the author; unknowns become visible
  `[TBD — confirm with …]` placeholders; (2) **never decide** — no approval, no
  pass/fail, no prioritization. Those keep a human in the loop, consistent with
  OSU's AI-use posture.
- **Audience-adaptive tone** — gentler and jargon-free for business partners,
  terser for technical staff.

---

## Data handling & publishability — READ BEFORE PUBLISHING

This skill is designed to be **published publicly (GitHub) while carrying zero
business data.** Keep it that way:

- **No filled samples are bundled.** Real briefs/charters were read **only during
  skill creation** to distill patterns; their substance lives in `references/` as
  **abstracted rules** (no names, project nouns, dollar figures, or unit-specific
  detail).
- **Bundled assets are BLANK templates only**, and their document metadata
  (author / last-modified-by) was scrubbed to remove staff names.
- **No personal contacts.** The intake coordinator's name/email and the deadline
  schedule are intentionally generalized in `process-overview.md` and meant to be
  **injected at runtime** by the app.
- **When you add rules from new reviewer feedback, abstract them.** If you can
  tell which specific project a rule came from, it's not abstract enough.

**Safe to publish:** this folder (`.claude/skills/uit-portfolio/`) only.
**Do NOT publish** the surrounding repo — `process/`, `samples-brief/`,
`samples-charter/`, `templates/`, and the eval workspace
(`.claude/skills/uit-portfolio-workspace/`) all contain internal OSU materials.
The repo root `.gitignore` excludes these as a safeguard, but the cleanest
release is to publish this skill folder as its own repository.

---

## How it was validated

Built and tested with the `skill-creator` workflow.

- **Method:** the skill was run against a **no-skill baseline** on two scenarios —
  (1) an open-ended request to turn a rough idea into a brief, and (2) a charter
  built from a brief that carried reviewer comments — then graded against
  objective assertions and compared in the skill-creator viewer.
- **Findings (directional; one run per configuration):**
  - The skill passed all checks; the baseline missed several.
  - **Largest gap on open-ended brief authoring:** without the skill, a model
    tends to invent its own document structure instead of the official template,
    and may confidently assert an intake process that doesn't match OSU's
    documented Pipeline → Charter → EARB → Asana flow.
  - **Smaller gap on the charter** when the source brief already contains the
    answers inline — there the skill's edge is placeholder discipline (not
    asserting unconfirmed funding as fact) and forcing an explicit out-of-scope list.
  - Consistent skill wins: official-template fidelity, asking the reviewer
    questions up front, no invented funding/dates, and never rendering a decision.
- **The eval harness and its outputs contain business data** (they exercise real
  documents) and live **outside** the published skill, in the sibling
  `…-workspace/` directory. Not for publication.

### Re-running the evals / iterating

Use `skill-creator`. The test prompts live in `evals/evals.json`. The harness
spawns with-skill and baseline runs per prompt, grades them, and opens a review
viewer. To keep coverage honest, add prompts for new edge cases (e.g. a thin idea
that *shouldn't* need a charter; a multi-file upload; a non-OSU request that
should *not* trigger the skill).

### Updating the rules from new feedback

When new commented briefs/charters appear, read them **in a creation session
only**, and fold any **new** recurring reviewer question into
`references/reviewer-questions.md` and any new quality signal into
`references/rubric.md` — always abstracted, never verbatim.
