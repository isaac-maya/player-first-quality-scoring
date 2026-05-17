# FC Defect Taxonomy

| Category | Player impact | Evidence | Escalation rule |
| --- | --- | --- | --- |
| Input responsiveness | Player feels loss of control | Frame timing, replay capture, session abandonment | Escalate when online modes or competitive flows are affected |
| Matchmaking fairness | Player questions competitive integrity | Skill delta, latency spread, rematch behavior | Escalate when fairness perception and telemetry both move |
| Progression/reward trust | Player does not trust earned outcomes | Reward ledger, inventory state, support tickets | Escalate immediately if rewards are lost, duplicated, or delayed |
| UI flow clarity | Player cannot complete intended action | Click path, heatmap, support text | Escalate when navigation blocks core loop |
| Stability/performance | Player loses session continuity | Crash logs, disconnects, FPS drops | Escalate by affected mode and recurrence |

## Defect Packet Template

| Field | Example |
| --- | --- |
| Player moment | End-of-match reward screen |
| Symptom | Reward animation completes but item does not appear in inventory |
| Evidence | QA replay, reward ledger mismatch, support-ticket cluster |
| Impact | High trust damage, medium frequency |
| Recommendation | Block release or add server-side reconciliation before launch |
