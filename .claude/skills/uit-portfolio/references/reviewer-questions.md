# What reviewers actually ask — anticipate these

These are the recurring questions UIT reviewers raise on real submissions,
distilled into general rules. Asking them *before* a reviewer has to is the whole
point of this tool — it's how a vague submission becomes one that sails through.

**The questions are split into two tiers, and the tier you use depends on the
mode.** This split matters: a Concept Brief is meant to be *lightweight and
directional*. Interrogating a business partner about SLAs, HECVAT, and itemized
recurring costs while they're trying to submit an early-stage idea defeats the
purpose of Stage 1 and makes the tool feel like a bureaucratic barrier.

- **Brief mode → ask only Tier 1.** Keep it light. Do **not** pull Tier 2
  operational/commitment questions into a brief — that detail is deliberately
  deferred to the charter, and asking for it now is premature and off-putting.
- **Charter mode → Tier 1 is assumed done; focus on Tier 2.** The brief and its
  reviewer comments already cover Tier 1; the charter is where the heavy
  operational and commitment detail gets nailed down.

Within the right tier, use judgment — raise the questions that plainly apply to
this kind of work, framed as "a reviewer will ask…". If something genuinely
doesn't apply, note it as explicitly out of scope rather than leaving it silent.

---

## Tier 1 — Concept Brief (directional, lightweight)

Just enough to answer "is this worth advancing?" Keep each of these to a single,
plain question. These are the only questions to ask in **brief mode**.

- **Problem clarity.** What's the actual problem or opportunity, and who feels it?
  (Not the solution — the need.)
- **Desired outcomes.** What changes for the institution if this works? Push for a
  *result*, not a list of activities.
- **Strategic alignment.** Which specific strategic-plan commitment or policy does
  this advance? (A named goal, not "supports the university.") Offer the author a
  pick-list from `strategic-plan.md` rather than asking them to recall a goal.
- **Directional scope.** Roughly what's included — and is this *adding something
  new* or *replacing/retiring* existing systems? Which units, broadly?
- **Who's impacted / who should be at the table.** Which teams or partner units
  does this touch? Flag early if security/OIS or distributed IT clearly need to be
  involved — but at a "who to loop in" level, not a compliance deep-dive.
- **Major dependencies.** Does this clearly depend on, or enable, other work? A
  directional yes/no with the name of the other effort is enough here.
- **Rough resource sense (ROM).** A ballpark feel for people / tech / budget —
  order-of-magnitude only. Is any funding already identified, or is this still
  "on the radar"? Do **not** itemize costs at this stage.
- **Prioritization driver.** What's driving the timing — a compliance date, a
  dependency, a leadership ask? ("ASAP" without a reason is weak.) If the driver
  is "audit findings" or "security/compliance obligations," nudge for the *actual*
  findings — even directionally — because a bare label is something a reviewer
  can't weigh (see Tier 2 "Make the drivers concrete").
- **Desired completion / timeline.** When does the author want this done — even a
  rough quarter or fiscal year is fine. This is a simple, directly-askable fact;
  **ask it rather than leaving the date blank or `[TBD]`.** (A "desired completion
  date" the author was never asked about is a self-inflicted gap.)
- **Quantify the status quo.** Put a rough number on today's pain — current cost,
  support volume, manual hours, risk exposure, or growth rate. Reviewers ask "how
  do we know this is a real/growing problem?"; a baseline figure pre-empts that.
  Order-of-magnitude is fine — the point is *some* evidence, not precision.
- **Contention with in-flight work.** Does this draw on the same scarce people as
  a major program already underway or already approved? Flag the overlap
  directionally — reviewers weigh every new idea against committed capacity, and
  this is one of their most frequent comments.
- **Decision authority (especially cross-unit).** Who is the single accountable
  decision-maker? When several units share the outcome — or a leadership
  transition is underway — a lone sponsor is often not enough; flag the likely
  need for a steering committee. Directional only here; the governance model is
  charter-level.

---

## Tier 2 — Project Charter (commitment, operational detail)

Only ask these in **charter mode**. This is where reviewers probe hard, and
where vague answers cost the most. When converting a commented brief, treat each
reviewer comment as a required input: every question below that a reviewer raised
must be visibly answered somewhere in the charter.

### Scope precision (the #1 source of charter comments)
- Exactly **what is in and what is out**? Name the systems, units, and data
  classes covered — and explicitly the ones that are *not*.
- Does it **retire or replace** anything existing, or only add new?
- Does it cover **migrating existing data/state**, or only new going forward?
- Pin down vague scope words ("all", "centralized", "low-cost") to concrete bounds.

### Stakeholders and downstream load
- Is **every impacted unit/team named** in "UIT Teams Impacted" — not just in the
  narrative? Reviewers cross-check and flag groups mentioned in prose but missing
  from the list.
- For each impacted team, a **rough order-of-magnitude (ROM) resource request**.
  (Don't invent the numbers — elicit them or mark `[TBD]`; reviewers care a lot
  about hidden downstream load.)

### Dependencies and sequencing
- Is each dependency **hard (blocking)** or merely **helpful**? Be explicit.
- Does everything go live at once, or is there a **prioritized order**?

### Funding (probed hard)
- **Source**, and whether it's **committed, requested, or hoped-for**.
- **One-time vs. recurring** (on-prem capital vs. cloud operating cost), and the
  **funding year(s)**.
- Has **any of it already been purchased/deployed** (e.g., a prior PoC)?
- Who funds it if work must **start before** dedicated funding arrives?
- If funds aren't secured, frame it as "on the radar pending funding," not
  "prioritize now" — asking to prioritize unfunded work is itself flagged.

### Operations after go-live (frequently missing)
- **Who owns** technical management and data/quality stewardship after launch?
- **Ongoing processes, standards, governance**; what use/data is **eligible vs not**?
  (The people side — OCM, comms, support load — has its own subsection below.)

### Security, compliance, and risk surface
- **Data classification — name it first.** What classification of data does this
  touch (e.g. public vs. internal vs. restricted), and which regime governs it
  (**FERPA, HIPAA, GLBA, PCI-DSS, CUI**, …)? Classification drives the storage,
  access, and compliance requirements, so state it explicitly — reviewers flag a
  charter that leaves it implicit. If unknown, mark `[TBD — confirm data
  classification with OIS]` rather than guessing.
- Involve **OIS** when third-party or regulated data is in play. Will it **meet
  the applicable compliance regime(s)**? Name them, don't gesture at "compliance."
- Does it open **new access paths / attack surface**? What standards must all
  participants then meet?
- **HECVAT**: required when a third party handles OSU data — answer yes/no
  explicitly, and confirm whether an existing HECVAT is current or a new one is needed.
- **Zero Trust Architecture (ZTA) fit.** Does it align with the institution's ZTA
  direction, and what ZTA controls apply — e.g. geo/anomaly checks on sensitive
  automated actions?
- **Security telemetry.** Does it feed logs/events to the SOC/SIEM so activity can
  be correlated with the wider environment? Is that a stated requirement?
- **Accessibility (WCAG).** Treat as a requirement, *including* in specialized or
  clinical settings where it's easy to overlook.
- **Vendor data destruction.** For SaaS/third-party engagements, require confirmation
  that OSU data is destroyed (with proof) when the engagement ends.

### Make the drivers concrete
- "Audit findings" and "security obligations" as bare labels are **unreviewable**.
  Enumerate the specific findings/obligations, or mark `[TBD — list from the audit
  out-brief]`. A driver a reviewer can't see is one they can't weigh.
- Likewise, **describe the current-state process concretely** (what tool/script/
  manual step exists today) so reviewers don't have to write "assuming this is…".

### Holistic portfolio fit
- Frame the work within the **broader systems portfolio**, not as a standalone
  system. Name the **required integrations** with other enterprise systems, and
  state whether the new thing **replaces or coexists with** what's there today.

### Change management, communications, and support load
- Reviewers expect a named **OCM / communications plan**: who is affected, how
  they're informed and trained, how multiple teams end up using it the *same*
  way (process owners engaged early), and how this lands against any concurrent
  onboarding/enrollment process.
- **Support / Service Desk impact:** what new support calls will this generate and
  how are they handled? Is there a **fallback path** when the new flow fails for a
  user? Plan a **small-scale pilot** group before broad rollout.

### Dependencies on fixed external dates
- If a hard external date — a tool **deprecation**, a concurrent enterprise
  **go-live** — falls before this completes, state the **operational risk/impact
  and the contingency**. Reviewers probe what happens if the two timelines don't line up.

### Build vs. buy, and procurement timing
- For **commodity** capabilities, justify a custom build or a long
  requirements-gathering path over buying an established solution.
- Note **license-term flexibility** (month-to-month vs. annual lock-in) and whether
  **vendor negotiations must start now** to hit the timeline.

### Resilience and service levels
- Is **backup and recovery** in scope? It changes sizing and cost materially.
- **Redundancy / SLA / uptime** expectations — they drive design and cost, and
  partners often have expectations worth confirming.

### Performance and capacity
- Will it **perform under realistic, concurrent load**?
- Are **quotas / QoS / fair-use limits** needed so one heavy user can't degrade
  everyone? What mitigations?

### Architecture clarity
- Name the **architecture or standard** it conforms to — and if it **deviates**,
  say so and why.
- **On-prem vs. cloud**: state the choice and the rationale (latency, bandwidth,
  long-term cost).
