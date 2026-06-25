# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **Claude skill** (`uit-portfolio`) that guides OSU UIT staff through writing a Concept/Idea Brief or Project Charter for the UIT Portfolio Management process, then emits a filled `.docx` in the official template — plus the **web app that hosts it** (`app.py` + `static/index.html`), modeled on [`dirkpetersen/codecheck`](https://github.com/dirkpetersen/codecheck) (Python/FastAPI, Claude Code streamed over SSE, AWS Bedrock backend).

## Web app

- **Run:** `pip install -r requirements.txt && python app.py` → http://localhost:8000 (`PORT` overrides).
- **`app.py`** — FastAPI backend. Work is organized into persistent **projects** (sidebar list) stored under `~/.uit-portfolio` (`UIT_DATA_DIR` overrides). A chat message runs Claude Code in the project dir via `--output-format stream-json`, streamed to the browser as SSE events (`status`/`activity`/`chunk`/`doc`/`preview`/`done`/`error`). The skill is made resolvable by symlinking it into each project dir's `.claude/skills/`. The live preview pane is driven by `out/content.json` (the section map the skill emits), and the `.docx` is the downloadable artifact.
- **Claude tiers** (`get_claude_bin`): CLI when on PATH (point at Bedrock via `CLAUDE_CODE_USE_BEDROCK=1` in the env) → else **demo mode** (scripted interview that still generates a real `.docx` via `fill_brief.py`). Demo mode is forced inside a Claude Code session (`CLAUDECODE=1`), since nested CLI calls crash.
- **`static/index.html`** — single-file SPA (the editorial "document on a desk" design; the standalone visual mockup is in `mockups/`).
- **Test without a backend:** start the server (demo mode) and exercise `POST /api/projects`, `POST /api/projects/{id}/message` (SSE), `/upload`, `/download/{name}`, `/preview`.

## Skill architecture

All domain logic lives in `.claude/skills/uit-portfolio/`. The model reads the files in this order at runtime:

1. `SKILL.md` — primary runtime instructions (five-step flow, two modes)
2. `references/process-overview.md` — the four-stage governance process and hard boundaries
3. `references/reviewer-questions.md` — the questions reviewers actually raise (the core value of the tool)
4. `references/rubric.md` — per-section quality criteria used during interview and in the readiness summary
5. `references/charter-fields.md` — charter template field map (used only in Charter mode)

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
