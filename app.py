from __future__ import annotations

import pandas as pd
import streamlit as st

from edict_money_team import EdictMoneyTeam, HubuConnectMonitor, Opportunity, demo_opportunities, parse_opportunity_text


st.set_page_config(page_title="Edict Work Mode", page_icon="EW", layout="wide")


def score_rows(team: EdictMoneyTeam, opportunities: tuple[Opportunity, ...]) -> list[dict[str, object]]:
    scored = sorted((team.score(item) for item in opportunities), key=lambda item: item.total, reverse=True)
    return [
        {
            "Title": item.opportunity.title,
            "Verdict": item.verdict,
            "Risk penalty": item.risk,
            "Score": item.total,
            "Reason": "; ".join(item.rationale) if item.rationale else "Standard scoring applied",
            "Platform": item.opportunity.platform,
            "Fit": item.fit,
            "Speed": item.speed,
            "Trust": item.trust,
            "Money": item.money,
            "Required connects": item.opportunity.required_connects,
        }
        for item in scored
    ]


team = EdictMoneyTeam()
opportunities = demo_opportunities()

st.title("Edict Work Mode")
st.caption("Proof Before Apply - transparent work opportunity decision support")

left, right = st.columns([0.34, 0.66], gap="large")
parsed = None

with left:
    st.subheader("Decision controls")
    available_connects = st.slider("Available proposal credits / connects", 0, 40, 20)
    pasted_opportunity = st.text_area(
        "Paste opportunity text",
        placeholder="Title\nPlatform: Upwork\nBudget: Hourly: $10.00 - $40.00\nProposals: Fewer than 5\nClient: Payment verified\nConnects: 8\nSkills: Python, API, Automation",
        height=190,
    )
    if pasted_opportunity.strip():
        try:
            parsed = parse_opportunity_text(pasted_opportunity)
            opportunities = (*opportunities, parsed)
            st.success(f"Parsed: {parsed.title}")
        except ValueError as error:
            st.warning(str(error))
    run = st.button("Run decision workflow", type="primary", width="stretch")

    st.divider()
    st.metric("Opportunities", len(opportunities))
    st.metric("Departments", len(team.stages))
    st.write("IBM Bob 2.0 Hackathon project: Proof Before Apply.")

with right:
    if parsed is not None:
        parsed_score = team.score(parsed)
        st.subheader("Pasted opportunity decision")
        verdict_col, risk_col, score_col = st.columns(3)
        verdict_col.metric("Verdict", parsed_score.verdict.upper())
        risk_col.metric("Risk penalty", f"{parsed_score.risk}/10")
        score_col.metric("Total score", f"{parsed_score.total}/50")
        if parsed_score.verdict == "veto":
            st.error("Blocked before application")
        for reason in parsed_score.rationale:
            st.write(f"- {reason}")

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
