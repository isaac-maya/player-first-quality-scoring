"""Streamlit app for the Player-First FC Quality Scoring demo.

Lets visitors tune the 4 priority factors with sliders, see the score and release decision
update live, and load any sample defect into the sliders to see why it was scored that way.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pandas as pd
import streamlit as st

from fc_quality_scorer import DEFECTS, Defect, priority_score, release_decision

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="Player-First Quality Scoring — Isaac Maya",
    page_icon="🎮",
    layout="wide",
)

st.title("🎮 Player-First Quality Scoring")
st.markdown(
    "**Tune the model, watch the release decision change.**  \n"
    "_Built to demonstrate: Game QA · Player Experience · Sports Analytics_"
)

with st.expander("📖 Why this exists", expanded=True):
    st.markdown(
        """
Most defect prioritization is engineer-first: severity, frequency, complexity. **This model is
player-first:** how often does it happen per 1k matches, how much does it move abandonment, how much
support volume does it generate, how much trust does it damage?

Tune the four factors with the sliders below and watch the release decision shift in real time.
The formula is transparent — a model you can argue with is a model you can trust.
"""
    )

with st.expander("🎯 What you're looking at"):
    st.markdown(
        """
- ✅ Four player-impact factors with live sliders
- ✅ Transparent scoring formula (no black box)
- ✅ Release decision derived from score + threshold rules — visible, not magic
- ✅ Sample defect library — load any defect into the sliders to see why it scored that way
- ✅ Domain-transferable — the model framework works for any consumer product, not just FC
"""
    )

# ---------- Try it ----------
st.divider()
st.header("🧪 Try it")

defect_options = ["(blank — tune manually)"] + [f"{d.id} — {d.title}" for d in DEFECTS]
defect_pick = st.selectbox("Load a sample defect into the sliders", options=defect_options)

if defect_pick == "(blank — tune manually)":
    base = Defect(
        id="custom", category="Custom", title="Manual tune", mode="—",
        frequency_per_1k=20, abandonment_delta_pct=2.0, support_volume=200,
        trust_damage=3, reproducibility=3, recovery_cost=3,
    )
else:
    chosen_id = defect_pick.split(" — ")[0]
    base = next(d for d in DEFECTS if d.id == chosen_id)
    st.caption(f"Loaded **{base.id}** — {base.category} during {base.mode}.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Player-impact factors")
    freq = st.slider("Frequency per 1,000 sessions", 0, 200, base.frequency_per_1k)
    aband = st.slider("Abandonment delta %", 0.0, 10.0, float(base.abandonment_delta_pct), 0.1)
    support = st.slider("Support volume (tickets/touches)", 0, 1000, base.support_volume)
    trust = st.slider("Trust damage (1–5)", 1, 5, base.trust_damage)
with col2:
    st.subheader("Recovery factors")
    repro = st.slider("Reproducibility (1–5)", 1, 5, base.reproducibility)
    recov = st.slider("Recovery cost — engineering effort to fix (1–5)", 1, 5, base.recovery_cost)

tuned = replace(
    base, frequency_per_1k=freq, abandonment_delta_pct=aband, support_volume=support,
    trust_damage=trust, reproducibility=repro, recovery_cost=recov,
)
score = priority_score(tuned)
decision, rationale = release_decision(tuned, score)

DECISION_STYLE = {
    "Block release": ("🛑", "error"),
    "Hold release": ("⚠️", "warning"),
    "Ship with watch": ("👀", "info"),
    "Ship": ("✅", "success"),
}
icon, kind = DECISION_STYLE.get(decision, ("ℹ️", "info"))
getattr(st, kind)(f"{icon} **{decision}** — score `{score}` — _{rationale}_")

st.markdown("### Formula (visible, arguable)")
st.latex(r"""
\text{score} = \underbrace{\text{trust} \times 12}_{\text{trust weight}}
+ \underbrace{\text{freq} \times 0.4 + \text{aband} \times 4 + \text{support} \times 0.03}_{\text{breadth}}
+ \underbrace{\text{repro} \times 4}_{\text{repro weight}}
- \underbrace{\text{recovery} \times 2}_{\text{cost penalty}}
""")
st.caption(
    "Decision rules layer on top of the score: any defect with trust ≥ 5 AND abandonment ≥ 1.5% is auto-blocked; "
    "any reward/progression issue is auto-held until server-side reconciliation. The score determines the rest."
)

# ---------- Sample defect library ----------
st.divider()
st.subheader("📚 Sample defect library")
st.caption("All 10 sample defects, sorted by priority score. Click a row's defect ID in the dropdown above to load it.")
scored = []
for d in DEFECTS:
    s = priority_score(d)
    dec, ra = release_decision(d, s)
    scored.append({
        "ID": d.id, "Title": d.title, "Mode": d.mode, "Category": d.category,
        "Score": s, "Decision": dec, "Trust": d.trust_damage,
        "Freq/1k": d.frequency_per_1k, "Aband %": d.abandonment_delta_pct,
    })
df = pd.DataFrame(scored).sort_values("Score", ascending=False)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
with st.expander("🧪 How to test it (guided tour)", expanded=True):
    st.markdown(
        """
**Step 1 — Load a Block-level defect.** Pick `FC-205 — Disconnect at full-time whistle in Champions
final`. See the 🛑 **Block release** decision. This one has trust 5/5 and abandonment 6.5% — both
elevated. The model can't justify shipping this.

**Step 2 — Drop abandonment to 0.** Move the slider. Decision flips to ⚠️ **Hold release**. Lowering
one factor changed the verdict — the model is doing real work, not weighting one factor 100%.

**Step 3 — Break it on purpose.** Push `Frequency per 1,000` to max (200) with everything else at
minimum. Should still resolve to ✅ **Ship** — proves frequency without trust damage isn't a release
blocker. That's the player-first contract: trust > volume.

**Step 4 — Try a reward/progression case.** Pick `FC-202 — Weekly objective reward not credited`.
Note it's auto-held even with relatively low frequency — the *category* triggers a special rule
because reward credibility issues need server-side reconciliation, not a code fix.

**Step 5 — Read the formula.** It's right there above. Argue with it. Adjust the trust multiplier
mentally. That's how a model gets trusted — by surviving scrutiny, not by being hidden.
"""
    )

with st.expander("💼 What this proves about me"):
    st.markdown(
        """
**For Game QA roles:** I prioritize from the player's seat. The model bakes in that disconnects matter
more than UI quirks, even when UI quirks happen more often.

**For Player Experience roles:** I make the trade-off math visible. Sliders + formula + decision rules
are all in one place — you can argue with any of them in a meeting.

**For Sports Analytics roles:** I build models I can defend, not just deploy. The category-specific
auto-hold (reward credibility) shows that domain knowledge can override the score where it matters.

---

**Isaac Maya** — QA · Agentic AI · Data Quality  \n
📧 theisaacmaya@icloud.com · 💼 [LinkedIn](https://linkedin.com/in/isaac-maya) · 🔗 [Source](https://github.com/isaac-maya/player-first-quality-scoring) · 📝 [Essays](https://isaac-maya.github.io/essays/)
"""
    )
