# Reviewer Rubric — what makes a brief/charter easy to approve

This is the lens reviewers apply. Use it two ways: (1) to ask sharper follow-up
questions while interviewing the author, and (2) to produce the private readiness
summary. The goal is to catch the weaknesses a reviewer would flag *before* they
do — that's the entire point of this tool.

Score each section as **Strong / Adequate / Needs work** and, for anything below
Strong, name the specific gap and suggest the concrete addition that would fix
it. Be specific ("Outcomes lists activities, not measurable results — add a
target like 'reduce X by Y%'") rather than generic ("add more detail").

This file is the **scoring lens**; the questions to *ask* the author live in
`reviewer-questions.md`. When a criterion below scores weak, that file has the
interview question that fixes it — don't restate questions here.

## Cross-cutting signals reviewers reward

- **Specificity and evidence over adjectives.** "Improves efficiency" is weak;
  "cuts manual reconciliation from ~8 hrs/week to near-zero" is strong. Two
  concrete forms of this: a **baseline number** for today's pain (cost, volume,
  FTE, growth — order-of-magnitude is enough), and a **concrete description of
  the current state** (today's tool/script/manual process). If a reviewer would
  have to write "assuming this is X…" or "how do we know?", the draft is too vague.
- **Outcomes vs. activities.** Reviewers want the *result* (what changes for the
  institution), not a list of tasks.
- **Honest scope and risk.** A clear "what's out of scope" and a named risk with
  a mitigation reads as mature; silence reads as unconsidered.
- **Institutional framing.** Tie the work to OSU's mission, the *Prosperity
  Widely Shared* strategic plan, and any compliance/policy driver.
- **Right altitude.** A brief is directional; a charter is a commitment artifact.
  Don't push solution design into a brief, or leave a charter vague on cost/owner.

## Concept/Idea Brief — per-section criteria

- **Concept Description** — Strong: a crisp problem/opportunity statement and the
  benefit, in plain language. Weak: jumps to a solution without naming the problem.
- **Strategic Alignment** — Strong: names the specific strategic-plan commitment
  or policy it advances. Weak: generic "supports the university."
- **Outcomes / Key Results** — Strong: measurable results or clear capabilities.
  Weak: a list of activities or restated description.
- **Benefits (cost of inaction)** — Strong: concrete consequence of *not* doing
  it (risk, cost, missed opportunity). Weak: restates the benefits of doing it.
- **Risks** — Strong: real risks that could impede the effort. Weak: "none" or
  trivial risks.
- **Define Success** — Strong: an observable end-state someone could verify —
  a deliverable or target ("backup solution implemented with documented SOPs and
  an approved RACI"), not a feeling ("the environment is healthier"). Weak:
  circular ("success is completing the project") or aspirational/unmeasurable
  ("unmeasurable success criteria, not OKRs" is a real reviewer comment).
- **Proposed Solution** — Strong: a directional approach, explicitly not a final
  design. Weak: either empty or an over-specified build spec (wrong altitude).
- **Timeline / Desired Completion** — present and plausible; flag if missing.
- **Prioritization Drivers** — Strong: names the real driver (compliance date,
  dependency, leadership priority). Weak: "ASAP" with no reason.
- **Key Requirements** — concrete must-haves a reviewer can sanity-check.
- **Teams & Skills Needed** — Strong: realistic about who/what it takes. Weak:
  underestimates cross-team involvement (a common reason work needs a charter).

## Project Charter — per-section criteria

- **Business Justification** — the need in business terms, not technical terms.
- **Objectives** — measurable ("reduce cost by X", "increase quality to Y").
- **Risks of Not Fulfilling Objectives** — concrete institutional consequences.
- **Deliverables** — high-level products, not a task list.
- **Scope** — explicitly states what is **and is not** addressed. Missing the
  "not" half is the single most common charter weakness. Also positions the work
  within the systems portfolio: names required integrations and whether it
  replaces or coexists with what exists ("stand-alone system" draws comments).
- **Risks & Dependencies** — named, with at least a mitigation direction.
- **Impact on Stakeholders / Service Desk / other UIT teams** — Strong: names
  the teams and gives a rough order-of-magnitude (ROM) ask per team. Reviewers
  care a lot about hidden downstream load.
- **Data classification & compliance** — states the data classification involved
  and the governing regime(s) (FERPA/HIPAA/GLBA/PCI/CUI). Strong: named explicitly,
  since it drives every security requirement. Weak: left implicit or "TBD" with no
  owner to confirm.
- **Procurement / HECVAT** — answered explicitly (the HECVAT yes/no question is
  required when third-party software/data is involved).
- **Funding (implementation + operational)** — Strong: separates one-time vs.
  recurring and notes the funding year(s). Weak: a single lump or "TBD" with no
  owner to confirm. Never fabricate figures — elicit or mark as placeholder.
- **Accountability (sponsors, PM, SMEs)** — named roles, not blanks. When several
  units share the outcome, a lone sponsor is usually insufficient — reviewers look
  for a steering committee and one clear decision authority (a pending leadership
  transition sharpens this question).
- **Milestones / Timelines** — phased with proposed start/end dates.

## Patterns observed in real submissions

Concrete tells that separate strong submissions from weak ones, seen repeatedly
across approved and commented examples. Coach toward the first half of each pair.

- **Keep Outcomes and Proposed Solution distinct.** A common weakness is pasting
  the same bullets into both. Outcomes = the *results/capabilities* delivered;
  Proposed Solution = the *approach* to get there. If they're identical, one of
  them isn't doing its job.
- **State null values explicitly.** "Value: $0", "Funding: None", "HECVAT: No"
  read as deliberate and considered; blank cells read as forgotten. Don't leave
  a zero or a "no" implied.
- **Charter scope must spell out what's *out*.** An explicit "Out of Scope" list
  is the single strongest scope signal; its absence is the most common charter
  comment. Optional/possible-future items belong here too, clearly marked optional.
- **Keep stakeholder lists consistent across sections.** If a unit appears in the
  narrative, it must also appear in Teams & Skills / UIT Teams Impacted.
  Reviewers cross-check and flag any group named in prose but missing from the list.
- **Be honest about unsecured funding and real risks.** "Funding not yet secured"
  stated up front reads as mature, not weak — hiding it invites a harder comment.
- **Put content in the right section.** Cost-of-inaction belongs in Benefits /
  risk-of-not-doing, not in Outcomes; integration requirements aren't risks.
  Reviewers flag misplaced content ("this is what happens if you don't do this").
- **Let the brief stay light — reviewers defer detail to the charter themselves.**
  It's fine, and correct, to answer a deep question with "that belongs in the
  charter." Reviewers explicitly push detail down a stage; don't let a brief bloat
  into a charter.

## Readiness summary format (private to the author)

Produce this as chat output, never inside the .docx:

```
Readiness check (for your eyes — reviewers make the actual decision)

Strong:   <sections that would sail through>
Tighten:  <section> — <specific gap> → <concrete fix>
Missing:  <required info not yet provided> → who can confirm it
Open placeholders: <every [TBD ...] still in the document>
```
