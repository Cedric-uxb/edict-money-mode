from __future__ import annotations

import pandas as pd
import streamlit as st

from edict_money_team import EdictMoneyTeam, HubuConnectMonitor, Opportunity, demo_opportunities


st.set_page_config(page_title="Edict Work Mode", page_icon="EW", layout="wide")


def score_rows(team: EdictMoneyTeam, opportunities: tuple[Opportunity, ...]) -> list[dict[str, object]]:
    scored = sorted((team.score(item) for item in opportunities), key=lambda item: item.total, reverse=True)
    return [
        {
            "Title": item.opportunity.title,
            "Platform": item.opportunity.platform,
            "Score": item.total,
            "Verdict": item.verdict,
            "Fit": item.fit,
            "Speed": item.speed,
            "Trust": item.trust,
            "Money": item.money,
            "Risk penalty": item.risk,
            "Required connects": item.opportunity.required_connects,
        }
        for item in scored
    ]


team = EdictMoneyTeam()
opportunities = demo_opportunities()

st.title("Edict Work Mode")
st.caption("IBM Bob wildcard prototype for intelligent work decision support")

left, right = st.columns([0.34, 0.66], gap="large")

with left:
    st.subheader("Decision controls")
    available_connects = st.slider("Available proposal credits / connects", 0, 40, 20)
    run = st.button("Run decision workflow", type="primary", width="stretch")

    st.divider()
    st.metric("Opportunities", len(opportunities))
    st.metric("Departments", len(team.stages))
    st.write("Selected challenge theme: wildcard, Future of Work.")

with right:
    st.subheader("Opportunity board")
    rows = score_rows(team, opportunities)
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

    if run:
        scored = tuple(sorted((team.score(item) for item in opportunities), key=lambda item: item.total, reverse=True))
        connect_report = HubuConnectMonitor().inspect(scored, available_connects)
        result = team.run(
            mandate="Rank work opportunities, block risky choices, and recommend the next approved action.",
            opportunities=opportunities,
            available_connects=available_connects,
        )

        st.subheader("Recommended actions")
        for action in result.recommended_actions:
            st.write(f"- {action}")

        st.subheader("Connects gate")
        if not connect_report.decisions:
            st.info("No apply-ready Upwork opportunities need a connects decision.")
        for decision in connect_report.decisions:
            st.write(
                f"- **{decision.opportunity_title}**: {decision.status}. "
                f"{decision.action}"
            )

        st.subheader("Workflow departments")
        for stage in result.stages:
            with st.expander(f"{stage.office} ({stage.agent_id})"):
                st.write(stage.responsibility)
                for item in stage.output:
                    st.write(f"- {item}")
    else:
        st.info("Run the workflow to generate decisions and action guidance.")
