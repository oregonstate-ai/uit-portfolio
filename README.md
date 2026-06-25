# uit-portfolio

Create, refine, and validate a submission to the OSU **UIT project portfolio**
process — a Concept/Idea Brief or a Project Charter — through a chat-assisted
interface, ending in a filled `.docx` in the official template.

This repository has two parts:

1. **The skill** (exists today) — a Claude skill that does the actual work:
   interviews the author, anticipates reviewer questions, and generates the
   document. It lives in [`.claude/skills/uit-portfolio/`](.claude/skills/uit-portfolio/).
2. **The web app** (planned, to be built here) — a chat + wizard front end that
   hosts the skill so non-technical staff can use it in a browser.

---

## The skill (today)

The skill is the brain of the whole tool. It guides an author — a UIT engineer
or a non-technical business partner — from a rough idea or an uploaded document
to a strong submission, then emits the official `.docx`.

- **Two auto-detected modes:** a **Concept/Idea Brief** (Stage 1, the default),
  or a **Project Charter** (Stage 2), detected when an uploaded brief contains
  Word reviewer comments.
- **Reviewer anticipation is the point.** It asks the questions UIT reviewers
  actually raise — scope in/out, stakeholders, funding commitment, dependencies,
  post-go-live ownership, security/compliance — *before* a reviewer has to.
- **Two hard rules:** it never invents facts (unknowns become visible
  `[TBD — confirm with …]` placeholders) and it never decides (no pass/fail,
  no approval, no ranking — that stays with human reviewers).

Maintainer and runtime documentation lives in the skill folder:
[`.claude/skills/uit-portfolio/README.md`](.claude/skills/uit-portfolio/README.md)
(the *why* and architecture) and `SKILL.md` (the runtime instructions the model
follows).

---

## The web app

The app lives **in this repository** (`app.py` + `static/index.html`), modeled on
[`dirkpetersen/codecheck`](https://github.com/dirkpetersen/codecheck):

### Run it locally

```bash
pip install -r requirements.txt
python app.py                 # serves http://localhost:8000  (override with PORT=…)
```

Copy `.env.default` → `.env` to configure. The app auto-detects how to reach Claude:

- **Production:** the **Claude Code CLI** must be on PATH (`~/.local/bin/claude`).
  Point it at AWS Bedrock by setting `CLAUDE_CODE_USE_BEDROCK=1` (+ AWS vars) in the
  environment — Claude Code reads those itself.
- **No CLI / inside a Claude Code session:** the app falls back to **demo mode** — a
  scripted interview that still generates a real `.docx` via the skill, so the whole
  flow (chat → live preview → download) is runnable with zero credentials.

Projects (uploads, generated docs, transcripts) persist under `~/.uit-portfolio`
(override with `UIT_DATA_DIR`).

### How it's wired

- **Backend:** Python / FastAPI.
- **Engine:** the app shells out to Claude Code and streams the agent's tool
  calls and output to the browser over **SSE**, so the user watches the
  assistant work in real time.
- **Model backend:** Claude Code pointed at **AWS Bedrock**, keeping inference
  inside an OSU-approved boundary.
- **Sessions, not chats:** like codecheck, a left-hand panel lists prior work —
  here labeled **projects**, so a user can return to an earlier project and
  refine it.

### Look and feel

- A polished, professional UI in **Oregon State colors** — Beaver orange as the
  accent, against black, gray, and white. Much cleaner than the codecheck
  baseline.
- A **standard chat interface** that can always attach one or more files.
- Encourage **voice input** — prompt the user that they can dictate with
  **Windows key + H**.

### Guided flow (the wizard)

1. **Start by choosing the document.** Ask up front: *Project Brief* or *Project
   Charter?* Make clear that the **brief is the first step** and the **charter is
   the second**.
   - **Charter** → the user must first **upload an approved brief**.
   - **Brief** → launch a chat prompt that asks what they think needs to be done,
     **why**, what the **benefit** is, what the **risks** are, whether they have
     a **proposed solution**, and **who should sponsor** it.
2. **Iterate with adaptive question UI.** After each answer, ask the next
   questions in whatever form fits:
   - a **multi-line form** for open answers,
   - **checkboxes** when multiple answers can be true,
   - **radio buttons** when exactly one is true.

   In every case, always include a **free-form "other"** option so the user can
   write their own answer, and **keep offering file upload** so they can
   strengthen the proposal with supporting documents at any step.
3. **Regenerate on every iteration.** Each round of answers regenerates the
   document (the brief, or the charter), and the **latest version is always
   available for download**.

### Dependencies between modes

A **brief must exist first**. Developing a charter requires uploading an
(approved) brief as the starting point — the app enforces this ordering.

---

## Repository layout

```
uit-portfolio/
├── README.md                      # this file
├── CLAUDE.md                      # guidance for Claude Code in this repo
└── .claude/skills/uit-portfolio/  # the skill (brief & charter assistant)
    ├── SKILL.md                   # runtime instructions
    ├── README.md                  # skill maintainer guide
    ├── references/                # process, reviewer questions, rubric, charter fields
    ├── scripts/fill_brief.py      # fills the brief template from a JSON content map
    └── assets/                    # blank official .docx templates only
```

> **Data handling:** this repo is public and carries **zero business data**.
> Bundled assets are blank templates only; `references/` holds abstracted rules,
> not real project names, figures, or contacts. See the skill README for the
> full publishing rules.
