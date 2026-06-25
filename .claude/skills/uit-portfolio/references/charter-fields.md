# Charter template field map & filling guide

The charter (`assets/UIT_Charter_Scope_Statement_Template_v2.docx`) is one large
Word table (~58 rows × up to 10 columns). Unlike the brief, most narrative
sections are a **heading row followed by an empty content row beneath** — write
the author's content into the empty row's first cell, leaving the heading intact.
A few sections are key/value rows (fill the cell to the right), and two are
sub-tables (Project Team; Funding breakdown).

There's intentionally **no fill script for the charter** — it has enough
structural variety (the team table, the itemized funding block, the HECVAT
checkbox) that per-field judgment beats a brittle generic script. Fill it with
python-docx, using the section map below to locate each anchor. Inspect the live
structure first so row indices are current:

```python
import docx
d = docx.Document("assets/UIT_Charter_Scope_Statement_Template_v2.docx")
tb = d.tables[0]
for ri, row in enumerate(tb.rows):
    print(ri, [c.text.strip()[:30] for c in row.cells][:3])
```

## Section anchors (heading text → how to fill)

**1. General Project Information** (key/value — write into the row's later columns)
- `Project Name:` , `Executive Sponsor (1):` , `Project Sponsor (1) (decision maker):` , `Value of project:`

**2. Project Team** (sub-table; header row is `Role | Name | Department | Telephone | E-mail`)
- Rows: `Project Manager:` then several `SME:` rows. Fill names/dept/contact only
  where the author supplied them; leave the rest blank.

**3. Project Scope Statement** (heading row → write into the empty row *below* each)
- `Project Purpose / Business Justification`
- `Objectives (in business terms)`
- `Risks of not Fulfilling Objectives`
- `Business Impacts`
- `Deliverables`
- `Scope` — must capture both **in scope** and **out of scope**
- `Risks`
- `Impact on Stakeholders`
- `Document Location/Links`
- `Project Milestones`
- `Project Timelines`
- `Project Procurement Requirements` — includes the **HECVAT yes/no** question;
  set it only from an explicit author answer
- `Funding Requirements: Implementation and Operation` — itemized: Implementation/
  One-time (Hardware, Software/SaaS/PaaS/IaaS/Licensing, Professional services,
  Training/Travel) and Operational/Recurring (same categories), plus the funding
  year(s). Keep one-time vs. recurring separate.
- `Identify the Impact on Service Desk`
- `Identify all UIT Teams Impacted beyond the primary project team` — include a
  rough order-of-magnitude (ROM) resource request per team
- `Project Resource Requirements`

## Filling helper (heading-then-blank-row pattern)

```python
def fill_below(table, heading_prefix, text):
    for ri, row in enumerate(table.rows):
        if row.cells[0].text.strip().startswith(heading_prefix):
            target = table.rows[ri + 1].cells[0]
            if target.text.strip():
                target.add_paragraph(str(text))
            else:
                target.paragraphs[0].add_run(str(text))
            return True
    return False
```

Same rules as everywhere: only write what the author provided; mark unconfirmed
items as `[TBD — confirm with <who>]`; never fabricate funding, dates, or names.
