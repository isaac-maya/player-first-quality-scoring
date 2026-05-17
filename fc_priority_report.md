# FC Release-Window Priority Report

## Sendable Summary

This report turns a defect backlog into a release-window decision using the player-first rule from `player_first_strategy.md`: trust impact and breadth lead, frequency follows, recovery cost adjusts. The output is meant to anchor a go / no-go conversation, not replace it.

- Defects scored: 10
- Block release: 3
- Hold release: 1
- Ship with watch: 2
- Ship: 4

## Release-Window Decision Table

| Priority | Defect | Category | Mode | Trust | Freq /1k | Aband Δ | Decision | Rationale |
| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |
| 1 | FC-201 Perceived input lag during high-pressure online transitions | Input responsiveness | Online Seasons | 5/5 | 38 | 4.2% | Block release | Trust damage and session abandonment both elevated — fix or rollback before ship. |
| 2 | FC-205 Disconnect at full-time whistle in Champions final cancels result | Stability/performance | FUT Champions | 5/5 | 4 | 6.5% | Block release | Trust damage and session abandonment both elevated — fix or rollback before ship. |
| 3 | FC-202 Weekly objective reward not credited after match completion | Progression/reward trust | Ultimate Team | 5/5 | 9 | 1.1% | Hold release | High trust damage even at lower frequency — need owner and ETA before ship. |
| 4 | FC-207 Pack reward animation completes but item missing from club | Progression/reward trust | Ultimate Team | 5/5 | 6 | 2.1% | Block release | Trust damage and session abandonment both elevated — fix or rollback before ship. |
| 5 | FC-204 Skill gap spread widens during off-peak Division Rivals queue | Matchmaking fairness | Division Rivals | 4/5 | 26 | 2.8% | Ship with watch | Compensating control or telemetry watch required during rollout window. |
| 6 | FC-203 Transfer market filter resets when returning from comparison view | UI flow clarity | Ultimate Team | 2/5 | 71 | 0.4% | Ship with watch | Compensating control or telemetry watch required during rollout window. |
| 7 | FC-208 Co-op partner skill rating ignored in matchmaking calculation | Matchmaking fairness | Co-op Seasons | 3/5 | 14 | 1.7% | Ship | Player-impact below release-window threshold; track in next patch. |
| 8 | FC-209 Frame drop during corner kick replay on prior-gen consoles | Stability/performance | Online Seasons | 2/5 | 22 | 0.6% | Ship | Player-impact below release-window threshold; track in next patch. |
| 9 | FC-206 Cursor drift when navigating squad screen with controller | Input responsiveness | Career Mode | 2/5 | 18 | 0.2% | Ship | Player-impact below release-window threshold; track in next patch. |
| 10 | FC-210 Player swap menu obscures opponent name during loading | UI flow clarity | Online Seasons | 1/5 | 31 | 0.1% | Ship | Player-impact below release-window threshold; track in next patch. |

## Top Player-Impact Narrative

**FC-201 — Perceived input lag during high-pressure online transitions** (Online Seasons)

- Player moment: input responsiveness during Online Seasons.
- Telemetry signal: 4.2% abandonment delta, 38 occurrences per 1,000 sessions, 612 support touches.
- Recovery posture: trust damage 5/5, reproducibility 4/5, recovery cost 2/5 — block release.
- Why this ranks first: Trust damage and session abandonment both elevated — fix or rollback before ship.

## Category Coverage

Confirms the backlog is not dominated by one category, so prioritization stays player-first instead of vocal-defect-first.

| Category | Defects in scope |
| --- | ---: |
| Input responsiveness | 2 |
| Matchmaking fairness | 2 |
| Progression/reward trust | 2 |
| Stability/performance | 2 |
| UI flow clarity | 2 |

## How This Connects To The Strategy

- `player_first_strategy.md` defines the rule; this report applies it.
- `defect_taxonomy.md` defines the categories; this report scores within them.
- The release-window decision is meant to be reviewed in the weekly quality forum, not auto-applied.
