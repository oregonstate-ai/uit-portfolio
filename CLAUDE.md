# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude skill** (`uit-portfolio`) that guides OSU UIT staff through writing a Concept/Idea Brief or Project Charter for the UIT Portfolio Management process, then emits a filled `.docx` in the official template — plus the **web app that hosts it** (`app.py` + `static/index.html`), modeled on [`dirkpetersen/codecheck`](https://github.com/dirkpetersen/codecheck) (Python/FastAPI, Claude Code streamed over SSE, AWS Bedrock backend).

## Web app

- **Run:** `pip install -r requirements.txt && python app.py` → http://localhost:8000 (`PORT` overrides). Copy `.env.default` → `.env` to configure (auto-loaded via `python-dotenv`).
- **`app.py`** — FastAPI backend. Work is organized into persistent **projects** (sidebar list) stored under `~/.uit-portfolio` (`UIT_DATA_DIR` overrides); each project dir holds `meta.json`, `messages.json`, `uploads/`, and `out/`. A chat message runs Claude Code in the project dir via `--output-format stream-json`, streamed to the browser as SSE events (`project`/`status`/`activity`/`chunk`/`doc`/`preview`/`done`/`error`, plus `trace` events that feed the raw "Claude Code console" popup). The skill is made resolvable by symlinking it into each project dir's `.claude/skills/`. The live preview pane is driven by `out/content.json` (the section map the skill emits), and the `.docx` is the downloadable artifact.
- **Claude tiers** (`get_claude_bin`): CLI when on PATH (point at Bedrock via `CLAUDE_CODE_USE_BEDROCK=1` in the env) → else **demo mode** (scripted interview that still generates a real `.docx` via `fill_brief.py`). Demo mode is forced inside a Claude Code session (`CLAUDECODE=1`), since nested CLI calls crash. CLI runs default to `--effort high` (`UIT_CLAUDE_EFFORT` overrides).
- **Model id is Bedrock-aware** (`resolve_model`). On Bedrock the `--model` value MUST be a full inference-profile id (`global.anthropic.claude-opus-4-8`); the bare first-party alias (`claude-opus-4-8`) is rejected with *"model identifier is invalid"*. Resolution order: explicit `UIT_CLAUDE_MODEL` → on Bedrock, `ANTHROPIC_MODEL`/`ANTHROPIC_DEFAULT_OPUS_MODEL` from the env → else the short alias for the first-party API. The `[1m]` suffix (1M-token context) works with either form. Do **not** hardcode a short alias in the `--model` flag.
- **`PREAMBLE` is a deliberate duplication of the skill's rules**, restated for the headless web-app context (brevity, working-dir paths, the two hard rules, batch-of-5 questions). It is injected only on the first turn. When you change a behavioral rule, change it in **both** `PREAMBLE` (app.py) and `SKILL.md` or they will drift.
- **Required Anthropic skills come in two flavors.** `FILE_SKILLS` (`docx`, `pdf`, `pptx`, `xlsx`) are filesystem skills under `~/.claude/skills/`: `app.py` existence-checks them (`missing_skills()` / `docx_skill_available()` guard — the brief template is never filled without `docx`) and symlinks them into each project so Claude reads uploads with the matching skill. `claude-api` is a **built-in CLI skill** (no file on disk) — it can't be checked or symlinked, so it's enforced only via the `PREAMBLE`, which tells the model to consult it for any Claude/Anthropic API guidance. Do **not** add `claude-api` to `missing_skills` — it would report missing forever. `/api/version` reports `missing_skills`; the SPA shows a startup warning listing any absent file-skills.
- **Charter is never auto-switched, but it is pre-selected.** `/upload` only *reports* `has_comments` (via `word/comments.xml`), `is_brief` (`_is_concept_brief` matches ≥3 official-template headings, so a commented strategy paper doesn't qualify), and `suggested_mode`. When the upload is a brief **with** reviewer comments, `suggested_mode` is `"charter"` and the SPA marks the "Build the Charter" choice as primary/default — but the mode still changes only through an explicit user click → `POST /mode`. The project title is promoted from the skill's `concept_title` in `out/content.json`, never from the user's first message.
- **`static/index.html`** — single-file SPA (the editorial "document on a desk" design; the standalone visual mockup is in `mockups/`). Served with `no-store` since all HTML/CSS/JS live in this one file.
- **Test without a backend:** start the server (demo mode) and exercise `POST /api/projects`, `POST /api/projects/{id}/message` (SSE), `/upload`, `/download/{name}`, `/preview`.

## Skill architecture

All domain logic lives in `.claude/skills/uit-portfolio/`. The model reads the files in this order at runtime:

1. `SKILL.md` — primary runtime instructions (five-step flow, two modes)
2. `references/process-overview.md` — the four-stage governance process and hard boundaries
3. `references/reviewer-questions.md` — the questions reviewers actually raise (the core value of the tool)
4. `references/rubric.md` — per-section quality criteria used during interview and in the readiness summary
5. `references/strategic-plan.md` — OSU strategic-plan goals, presented as a pick-list for the Strategic Alignment section. **Currently a placeholder** between the `STRATEGIC-PLAN-CONTENT:START/END` markers; populate by running the OSU strategic plan PDF through the `pdf` skill and pasting the goal list as a pickable list. The skill falls back to an open-ended question until then.
6. `references/charter-fields.md` — charter template field map (used only in Charter mode)

**Two auto-detected modes:**
- **Brief mode** (default, Stage 1): idea or early document → `ConceptBrief_Template.docx`
- **Charter mode** (Stage 2): a brief that came back with Word reviewer comments → `UIT_Charter_Scope_Statement_Template_v2.docx`. Triggered by presence of `word/comments.xml` in the uploaded `.docx`.

## Generating documents

**Brief** — uses `scripts/fill_brief.py` with a JSON content map:

```bash
python3 .claude/skills/uit-portfolio/scripts/fill_brief.py \
  --template .claude/skills/uit-portfolio/assets/ConceptBrief_Template.docx \
  --out MyProject_Concept_Brief.docx \
  --content content.json
```

Requires `python-docx` (`pip install python-docx`). All `content.json` keys are optional — omitted keys are left blank. Valid keys are listed at the top of `scripts/fill_brief.py`.

**Charter** — no script; fill `assets/UIT_Charter_Scope_Statement_Template_v2.docx` with python-docx directly. Inspect live structure first:

```python
import docx
d = docx.Document(".claude/skills/uit-portfolio/assets/UIT_Charter_Scope_Statement_Template_v2.docx")
tb = d.tables[0]
for ri, row in enumerate(tb.rows):
    print(ri, [c.text.strip()[:30] for c in row.cells][:3])
```

Use the `fill_below()` helper in `references/charter-fields.md` for the heading-then-blank-row pattern that most charter sections use.

## Detecting Word comments

```bash
python3 -c "import zipfile; z=zipfile.ZipFile('FILE.docx'); print('HAS_COMMENTS' if 'word/comments.xml' in z.namelist() and z.read('word/comments.xml').strip() else 'no comments')"
```

## Running evals

Use the `skill-creator` skill. Test prompts are in `evals/evals.json`. The charter eval (`charter-from-commented-brief`) requires a real `.docx` with Word reviewer comments — keep those files out of the repo (they contain business data); store them locally in a sibling `uit-portfolio-workspace/` directory.

## Hard rules the skill must never violate

- **Never invent facts.** Funding numbers, dates, names, HECVAT answers → only from the author. Unknown → `[TBD — confirm with <who>]`.
- **Never decide.** No pass/fail, no "approved," no prioritization ranking. Readiness feedback is for the author only.

## Data-handling constraint

The repo is public. Bundled assets are **blank templates only** (document metadata scrubbed). `references/` contains abstracted rules — no project names, dollar figures, or unit-specific detail from real submissions. Do not add filled samples or personal contacts. The sibling directories (`process/`, `samples-brief/`, `samples-charter/`, `templates/`, `uit-portfolio-workspace/`) contain internal OSU materials and are excluded by `.gitignore`.
