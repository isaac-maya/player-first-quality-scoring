# Player-First FC Quality Strategy

## Strategy

Quality should start from the player moment, not the defect label. A matchmaking issue, input delay, or reward inconsistency matters because it changes trust: did the player feel in control, treated fairly, and correctly rewarded?

## Evidence Model

| Signal | What it tells us | Example use |
| --- | --- | --- |
| Defect reports | Repro steps and visible symptom | Confirm the bug is real and repeatable |
| Gameplay telemetry | Frequency and affected cohorts | Separate loud issues from broad issues |
| Session outcomes | Abandonment, rematches, mode switching | Estimate player impact |
| Support/community language | Frustration shape and player expectation | Improve prioritization narrative |
| QA replay notes | Controlled evidence and regression coverage | Prevent recurrence |

## Prioritization Rule

Prioritize defects by player trust impact, breadth, reproducibility, and recovery path. A rare progression bug that damages reward trust can outrank a more frequent visual issue.

## Example Decision

If two issues compete for a release window:

- Input delay in online match transitions gets priority when telemetry shows session abandonment rises after the defect appears.
- Cosmetic menu clipping waits unless it blocks navigation or affects a key monetization/progression flow.

## Operating Cadence

Weekly quality review should include one table that joins defect count, telemetry impact, affected modes, player language, and release recommendation. The goal is not more data; it is a better go/no-go conversation.
