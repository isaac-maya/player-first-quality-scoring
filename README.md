# EA FC Quality + Data Strategy Pack

A compact player-first quality artifact for EA Sports FC-adjacent QA, analytics, and player-experience roles. Uses synthetic defects and telemetry to show how trust impact, breadth, and recovery cost can drive a release-window decision — not pretending to simulate game systems, but speaking the language of how FC quality conversations actually move.

## What It Demonstrates In 30 Seconds

- Player-first prioritization is a rule (`player_first_strategy.md`) applied to data (`fc_quality_scorer.py`), not a slogan.
- A defect backlog becomes a release-window decision table with explicit block / hold / ship-with-watch / ship calls.
- Trust damage and session abandonment lead the prioritization; raw frequency does not get to dominate.
- The taxonomy, the strategy, and the scorer are aligned — the same five categories show up across all three files.

## Run

```bash
python3 fc_quality_scorer.py
```

The command refreshes `fc_priority_report.md` from the synthetic defect set.

## Contents

- `fc_quality_scorer.py`: runnable prioritization with 10 synthetic FC defects across 5 taxonomy categories.
- `fc_priority_report.md`: generated release-window decision table and top-impact narrative.
- `fc_quality_notebook.ipynb`: compact analytics notebook for the same scoring logic.
- `player_first_strategy.md`: quality strategy written for gameplay and player-experience stakeholders.
- `defect_taxonomy.md`: defect classes, evidence sources, and escalation rules.
- `outreach_note.md`: Serena Bacon-facing sharing note.

## Quality Themes

The synthetic defects span the five categories from `defect_taxonomy.md`:

1. Input responsiveness — perceived control during high-pressure moments.
2. Progression/reward trust — Ultimate Team and weekly objective credibility.
3. Matchmaking fairness — competitive integrity in Division Rivals and Co-op.
4. UI flow clarity — transfer market, squad management, in-match menus.
5. Stability/performance — disconnects, frame drops, session continuity.

## Why It Fits EA Sports FC

FC quality conversations are not about defect count; they are about player trust under pressure. A weekly-objective reward that does not credit can damage trust more than a UI bug that affects ten times as many sessions. This pack reflects that conversation: the scorer applies the prioritization rule from the strategy doc, and the resulting decision table is something a QA, design, or analytics partner could actually use in a release readiness review.

The synthetic dataset is grounded in known FC pain shapes (input lag in online modes, Ultimate Team pack credibility, FUT Champions disconnect at the worst possible moment) without claiming insider knowledge of EA systems.

## Outreach Hook

I built a small FC quality artifact that turns a synthetic defect backlog into a release-window decision using a player-first rule — trust impact and breadth before frequency. The decision table, taxonomy, and strategy all use the same five categories so the artifact reads as one coherent conversation, not three separate documents.
