"""Player-first FC defect prioritization with release-window decisioning."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).parent
REPORT_PATH = ROOT / "fc_priority_report.md"


@dataclass(frozen=True)
class Defect:
    id: str
    category: str
    title: str
    mode: str
    frequency_per_1k: int
    abandonment_delta_pct: float
    support_volume: int
    trust_damage: int
    reproducibility: int
    recovery_cost: int


DEFECTS: list[Defect] = [
    Defect("FC-201", "Input responsiveness", "Perceived input lag during high-pressure online transitions",
           "Online Seasons", 38, 4.2, 612, 5, 4, 2),
    Defect("FC-202", "Progression/reward trust", "Weekly objective reward not credited after match completion",
           "Ultimate Team", 9, 1.1, 487, 5, 5, 1),
    Defect("FC-203", "UI flow clarity", "Transfer market filter resets when returning from comparison view",
           "Ultimate Team", 71, 0.4, 154, 2, 5, 5),
    Defect("FC-204", "Matchmaking fairness", "Skill gap spread widens during off-peak Division Rivals queue",
           "Division Rivals", 26, 2.8, 298, 4, 3, 3),
    Defect("FC-205", "Stability/performance", "Disconnect at full-time whistle in Champions final cancels result",
           "FUT Champions", 4, 6.5, 731, 5, 2, 1),
    Defect("FC-206", "Input responsiveness", "Cursor drift when navigating squad screen with controller",
           "Career Mode", 18, 0.2, 62, 2, 4, 4),
    Defect("FC-207", "Progression/reward trust", "Pack reward animation completes but item missing from club",
           "Ultimate Team", 6, 2.1, 354, 5, 4, 2),
    Defect("FC-208", "Matchmaking fairness", "Co-op partner skill rating ignored in matchmaking calculation",
           "Co-op Seasons", 14, 1.7, 121, 3, 3, 4),
    Defect("FC-209", "Stability/performance", "Frame drop during corner kick replay on prior-gen consoles",
           "Online Seasons", 22, 0.6, 89, 2, 4, 4),
    Defect("FC-210", "UI flow clarity", "Player swap menu obscures opponent name during loading",
           "Online Seasons", 31, 0.1, 28, 1, 5, 5),
]


def priority_score(defect: Defect) -> float:
    trust = defect.trust_damage * 12
    breadth = defect.frequency_per_1k * 0.4 + defect.abandonment_delta_pct * 4 + defect.support_volume * 0.03
    repro = defect.reproducibility * 4
    recovery_penalty = defect.recovery_cost * 2
    return round(trust + breadth + repro - recovery_penalty, 1)


def release_decision(defect: Defect, score: float) -> tuple[str, str]:
    if defect.trust_damage >= 5 and defect.abandonment_delta_pct >= 1.5:
        return "Block release", "Trust damage and session abandonment both elevated — fix or rollback before ship."
    if defect.trust_damage >= 5:
        return "Hold release", "High trust damage even at lower frequency — need owner and ETA before ship."
    if defect.category == "Progression/reward trust":
        return "Hold release", "Reward credibility issues are not safe to ship without server-side reconciliation."
    if score >= 60:
        return "Ship with watch", "Compensating control or telemetry watch required during rollout window."
    return "Ship", "Player-impact below release-window threshold; track in next patch."


def render_report(scored: list[tuple[Defect, float, str, str]]) -> str:
    blockers = [row for row in scored if row[2] == "Block release"]
    holds = [row for row in scored if row[2] == "Hold release"]
    watches = [row for row in scored if row[2] == "Ship with watch"]
    shippable = [row for row in scored if row[2] == "Ship"]

    categories = sorted({defect.category for defect, *_ in scored})
    coverage = {
        cat: sum(1 for defect, *_ in scored if defect.category == cat)
        for cat in categories
    }

    lines = [
        "# FC Release-Window Priority Report",
        "",
        "## Sendable Summary",
        "",
        "This report turns a defect backlog into a release-window decision using the player-first rule from `player_first_strategy.md`: trust impact and breadth lead, frequency follows, recovery cost adjusts. The output is meant to anchor a go / no-go conversation, not replace it.",
        "",
        f"- Defects scored: {len(scored)}",
        f"- Block release: {len(blockers)}",
        f"- Hold release: {len(holds)}",
        f"- Ship with watch: {len(watches)}",
        f"- Ship: {len(shippable)}",
        "",
        "## Release-Window Decision Table",
        "",
        "| Priority | Defect | Category | Mode | Trust | Freq /1k | Aband Δ | Decision | Rationale |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for index, (defect, score, decision, rationale) in enumerate(scored, start=1):
        lines.append(
            f"| {index} | {defect.id} {defect.title} | {defect.category} | {defect.mode} | "
            f"{defect.trust_damage}/5 | {defect.frequency_per_1k} | {defect.abandonment_delta_pct:.1f}% | "
            f"{decision} | {rationale} |"
        )

    lines.extend([
        "",
        "## Top Player-Impact Narrative",
        "",
    ])
    top_defect, top_score, top_decision, top_rationale = scored[0]
    lines.extend([
        f"**{top_defect.id} — {top_defect.title}** ({top_defect.mode})",
        "",
        f"- Player moment: {top_defect.category.lower()} during {top_defect.mode}.",
        f"- Telemetry signal: {top_defect.abandonment_delta_pct:.1f}% abandonment delta, "
        f"{top_defect.frequency_per_1k} occurrences per 1,000 sessions, "
        f"{top_defect.support_volume} support touches.",
        f"- Recovery posture: trust damage {top_defect.trust_damage}/5, reproducibility {top_defect.reproducibility}/5, "
        f"recovery cost {top_defect.recovery_cost}/5 — {top_decision.lower()}.",
        f"- Why this ranks first: {top_rationale}",
        "",
        "## Category Coverage",
        "",
        "Confirms the backlog is not dominated by one category, so prioritization stays player-first instead of vocal-defect-first.",
        "",
        "| Category | Defects in scope |",
        "| --- | ---: |",
    ])
    for category in categories:
        lines.append(f"| {category} | {coverage[category]} |")

    lines.extend([
        "",
        "## How This Connects To The Strategy",
        "",
        "- `player_first_strategy.md` defines the rule; this report applies it.",
        "- `defect_taxonomy.md` defines the categories; this report scores within them.",
        "- The release-window decision is meant to be reviewed in the weekly quality forum, not auto-applied.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    scored = []
    for defect in DEFECTS:
        score = priority_score(defect)
        decision, rationale = release_decision(defect, score)
        scored.append((defect, score, decision, rationale))
    scored.sort(key=lambda row: row[1], reverse=True)
    REPORT_PATH.write_text(render_report(scored), encoding="utf-8")
    print(f"Scored {len(scored)} FC defects; report written to {REPORT_PATH.name}.")


if __name__ == "__main__":
    main()
