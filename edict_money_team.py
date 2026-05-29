from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable


@dataclass(frozen=True)
class Opportunity:
    title: str
    platform: str
    url: str
    budget: str = "Unknown"
    proposals: str = "Unknown"
    client_signal: str = "Unknown"
    description: str = ""
    tags: tuple[str, ...] = ()
    required_connects: int = 0


@dataclass(frozen=True)
class ScoredOpportunity:
    opportunity: Opportunity
    fit: int
    speed: int
    trust: int
    money: int
    risk: int
    total: int
    verdict: str
    rationale: tuple[str, ...]


@dataclass(frozen=True)
class DepartmentReport:
    agent_id: str
    office: str
    responsibility: str
    output: tuple[str, ...]


@dataclass(frozen=True)
class ConnectDecision:
    opportunity_title: str
    required_connects: int
    available_connects: int
    status: str
    action: str


@dataclass(frozen=True)
class ConnectReport:
    available_connects: int | None
    decisions: tuple[ConnectDecision, ...]

    def to_markdown_lines(self) -> list[str]:
        lines = ["## 户部 Connects Monitor", ""]
        if self.available_connects is None:
            lines.extend(
                [
                    "- Available connects: unknown",
                    "- Action: inspect Upwork before submitting proposals.",
                    "",
                ]
            )
            return lines

        lines.append(f"- Available connects: {self.available_connects}")
        lines.append("")
        for decision in self.decisions:
            lines.extend(
                [
                    f"### {decision.opportunity_title}",
                    "",
                    f"- Required connects: {decision.required_connects}",
                    f"- Available connects: {decision.available_connects}",
                    f"- Status: {decision.status}",
                    f"- Action: {decision.action}",
                    "",
                ]
            )
        return lines


@dataclass(frozen=True)
class EdictRun:
    mandate: str
    today: str
    stages: tuple[DepartmentReport, ...]
    opportunities: tuple[ScoredOpportunity, ...]
    recommended_actions: tuple[str, ...]
    delivery_playbook: tuple[str, ...]
    connect_report: ConnectReport | None = None

    def to_markdown(self) -> str:
        lines: list[str] = [
            f"# Edict Money Mode Memorial - {self.today}",
            "",
            f"Mandate: {self.mandate}",
            "",
            "## Court Flow",
            "",
        ]

        for stage in self.stages:
            lines.append(f"### {stage.office} ({stage.agent_id})")
            lines.append("")
            lines.append(f"Responsibility: {stage.responsibility}")
            lines.append("")
            for item in stage.output:
                lines.append(f"- {item}")
            lines.append("")

        if self.connect_report is not None:
            lines.extend(self.connect_report.to_markdown_lines())

        lines.append("## Ranked Opportunities")
        lines.append("")
        for index, scored in enumerate(self.opportunities, 1):
            opp = scored.opportunity
            lines.extend(
                [
                    f"### {index}. {opp.title}",
                    "",
                    f"- Platform: {opp.platform}",
                    f"- URL: {opp.url}",
                    f"- Budget: {opp.budget}",
                    f"- Proposals: {opp.proposals}",
                    f"- Client signal: {opp.client_signal}",
                    f"- Required connects: {opp.required_connects}",
                    f"- Tags: {', '.join(opp.tags) if opp.tags else 'None'}",
                    f"- Score: {scored.total}/50 "
                    f"(fit {scored.fit}, speed {scored.speed}, trust {scored.trust}, "
                    f"money {scored.money}, risk penalty {scored.risk})",
                    f"- Verdict: {scored.verdict}",
                    "",
                ]
            )
            for reason in scored.rationale:
                lines.append(f"- {reason}")
            lines.append("")

        lines.append("## Recommended Actions")
        lines.append("")
        for action in self.recommended_actions:
            lines.append(f"- {action}")
        lines.append("")

        lines.append("## Project Landing Playbook")
        lines.append("")
        for step in self.delivery_playbook:
            lines.append(f"- {step}")
        lines.append("")

        return "\n".join(lines)


class EdictMoneyTeam:
    """A small local implementation of the Edict 三省六部 workflow for paid work."""

    def __init__(self) -> None:
        self.stages = (
            DepartmentReport(
                "taizi",
                "太子 · 分拣",
                "Turn noisy intent into a clean mandate and reject pure chat.",
                (
                    "Classify the request as revenue work, portfolio work, learning, or admin.",
                    "Extract target platforms, acceptable budget, delivery window, and reputation goal.",
                ),
            ),
            DepartmentReport(
                "zaochao",
                "早朝官 · 情报",
                "Collect market signals and candidate opportunities.",
                (
                    "Search Upwork and Handshake first; later add Reddit, GitHub Issues, LinkedIn, and cold outbound.",
                    "Record source, title, budget, proposal count, client signal, tags, and raw description.",
                ),
            ),
            DepartmentReport(
                "zhongshu",
                "中书省 · 规划",
                "Convert opportunity data into a business plan.",
                (
                    "Rank opportunities by fit, speed, trust, money, and risk.",
                    "Select a small batch rather than chasing every visible project.",
                ),
            ),
            DepartmentReport(
                "menxia",
                "门下省 · 审议封驳",
                "Block bad work before it wastes connects or reputation.",
                (
                    "Veto senior-only, unclear, exploitative, or compliance-risk jobs.",
                    "Require honest capability claims and no fake portfolio statements.",
                ),
            ),
            DepartmentReport(
                "shangshu",
                "尚书省 · 派发",
                "Assign execution departments and define acceptance criteria.",
                (
                    "Route data/API work to 户部, proposal/docs to 礼部, implementation to 兵部, deployment to 工部.",
                    "Set a first-response proposal, milestone plan, and go/no-go gate.",
                ),
            ),
            DepartmentReport(
                "hubu",
                "户部 · 资源核算",
                "Price work, estimate effort, and track ROI.",
                (
                    "Check available Upwork connects and compare against each target's required connects.",
                    "Prefer 1-3 day projects during reputation bootstrap.",
                    "Flag low budgets that are acceptable only for first reviews or strong follow-up potential.",
                ),
            ),
            DepartmentReport(
                "libu",
                "礼部 · 文书",
                "Write client-facing proposals, handoff notes, SOPs, and walkthroughs.",
                (
                    "Generate concise tailored proposals instead of generic templates.",
                    "Prepare final delivery notes that make clients comfortable leaving a review.",
                ),
            ),
            DepartmentReport(
                "bingbu",
                "兵部 · 工程执行",
                "Build the actual project, tests, and fixes.",
                (
                    "Create a reproducible implementation plan from client requirements.",
                    "Ship working code, verify edge cases, and prepare a rollback or support path.",
                ),
            ),
            DepartmentReport(
                "gongbu",
                "工部 · 部署器物",
                "Handle local setup, integrations, deployment, and operational reliability.",
                (
                    "Check API keys, environments, hosting, spreadsheet permissions, and scheduled jobs.",
                    "Package scripts and instructions so the client can keep using the result.",
                ),
            ),
            DepartmentReport(
                "xingbu",
                "刑部 · 合规审计",
                "Review legal, platform, security, and privacy risks.",
                (
                    "Do not submit proposals, spend connects, send client data, or accept contracts without user approval.",
                    "Flag scraping, credential sharing, payment outside platform, and unsafe data handling.",
                ),
            ),
            DepartmentReport(
                "libu_hr",
                "吏部 · 声誉",
                "Improve profile, proof, reviews, and repeatability.",
                (
                    "Track wins, testimonials, reusable snippets, and portfolio artifacts.",
                    "Turn each finished project into stronger profile evidence for the next bid.",
                ),
            ),
        )

    def run(
        self,
        mandate: str,
        opportunities: Iterable[Opportunity],
        available_connects: int | None = None,
    ) -> EdictRun:
        scored = tuple(
            sorted(
                (self.score(opportunity) for opportunity in opportunities),
                key=lambda item: item.total,
                reverse=True,
            )
        )

        connect_report = HubuConnectMonitor().inspect(scored, available_connects)
        recommended = self._recommended_actions(scored, connect_report)
        return EdictRun(
            mandate=mandate,
            today=date.today().isoformat(),
            stages=self.stages,
            opportunities=scored,
            recommended_actions=recommended,
            delivery_playbook=self._delivery_playbook(),
            connect_report=connect_report,
        )

    def score(self, opportunity: Opportunity) -> ScoredOpportunity:
        text = " ".join(
            [
                opportunity.title,
                opportunity.description,
                " ".join(opportunity.tags),
                opportunity.budget,
                opportunity.proposals,
                opportunity.client_signal,
            ]
        ).lower()

        fit = self._fit_score(text)
        speed = self._speed_score(text)
        trust = self._trust_score(text)
        money = self._money_score(text)
        risk = self._risk_penalty(text)
        total = fit + speed + trust + money - risk

        rationale: list[str] = []
        if fit >= 8:
            rationale.append("Strong match with AI automation, Python, API, Google Sheets, or chatbot positioning.")
        if speed >= 8:
            rationale.append("Looks small enough for a fast first milestone.")
        if "fewer than 5" in text:
            rationale.append("Low proposal count improves early-account odds.")
        if risk >= 6:
            rationale.append("Risk is high; do not apply unless scope is narrowed.")
        if money <= 4:
            rationale.append("Money is weak; only worth it for review potential or follow-up work.")

        verdict = "apply" if total >= 27 and risk < 7 else "watch"
        if total < 24 or risk >= 8:
            verdict = "veto"

        return ScoredOpportunity(
            opportunity=opportunity,
            fit=fit,
            speed=speed,
            trust=trust,
            money=money,
            risk=risk,
            total=total,
            verdict=verdict,
            rationale=tuple(rationale),
        )

    @staticmethod
    def _fit_score(text: str) -> int:
        score = 2
        for keyword in (
            "python",
            "automation",
            "api",
            "google sheets",
            "apps script",
            "claude",
            "openai",
            "chatbot",
            "mcp",
            "workflow",
        ):
            if keyword in text:
                score += 1
        return min(score, 10)

    @staticmethod
    def _speed_score(text: str) -> int:
        score = 5
        fast_signals = ("small job", "simple", "fix", "script", "google sheets", "apps script", "initial setup")
        slow_signals = ("senior", "production-grade", "multi-tenant", "kubernetes", "2-3 months", "long-term")
        score += sum(1 for signal in fast_signals if signal in text)
        score -= sum(2 for signal in slow_signals if signal in text)
        return max(1, min(score, 10))

    @staticmethod
    def _trust_score(text: str) -> int:
        score = 4
        if "payment verified" in text:
            score += 3
        if "4." in text or "5.0" in text:
            score += 1
        if "fewer than 5" in text:
            score += 2
        if "50+" in text:
            score -= 2
        return max(1, min(score, 10))

    @staticmethod
    def _money_score(text: str) -> int:
        if "$25" in text or "$5.00 - $10.00" in text:
            return 3
        if "$10.00 - $40.00" in text or "$20.00 - $40.00" in text:
            return 7
        if "$150" in text or "$200" in text:
            return 7
        if "$30" in text or "$40" in text:
            return 8
        return 5

    @staticmethod
    def _risk_penalty(text: str) -> int:
        risk = 1
        for signal in (
            "production-grade",
            "senior",
            "must be available 9am-5pm",
            "video submission",
            "source code and ownership transferred",
            "warranty",
            "50+",
            "kubernetes",
            "terraform",
            "soc 2",
            "gdpr",
        ):
            if signal in text:
                risk += 1
        return min(risk, 10)

    @staticmethod
    def _recommended_actions(
        scored: tuple[ScoredOpportunity, ...],
        connect_report: ConnectReport | None = None,
    ) -> tuple[str, ...]:
        apply_now = [item for item in scored if item.verdict == "apply"][:3]
        if not apply_now:
            return (
                "No safe apply-now opportunity found. Search another batch before spending connects.",
                "Ask 门下省 to loosen or refine criteria only if the pipeline is empty.",
            )

        actions = []
        connect_by_title = {}
        if connect_report is not None:
            connect_by_title = {
                decision.opportunity_title: decision for decision in connect_report.decisions
            }

        for item in apply_now:
            connect_decision = connect_by_title.get(item.opportunity.title)
            if connect_decision and connect_decision.status == "blocked":
                actions.append(
                    f"Hold Upwork proposal for {item.opportunity.title}: {connect_decision.action}"
                )
                continue
            actions.append(
                f"Prepare a tailored proposal for {item.opportunity.platform}: {item.opportunity.title}."
            )
        actions.append("Before submission, user must approve connects spend and final text.")
        return tuple(actions)

    @staticmethod
    def _delivery_playbook() -> tuple[str, ...]:
        return (
            "Intake: ask for repo/sheet/API access, one failing example, expected output, deadline, and success definition.",
            "Diagnosis: reproduce the issue or inspect the workflow before promising a final fix.",
            "Milestone 1: deliver a small working slice or written diagnosis within 24 hours.",
            "Build: 兵部 implements; 工部 handles environment, credentials, and deployment; 礼部 keeps the client updated.",
            "Review: 门下省 checks scope, edge cases, and client-facing claims before delivery.",
            "Delivery: provide working artifact, short Loom/scripted walkthrough outline, and maintenance notes.",
            "Reputation: 吏部 asks for review only after acceptance and records reusable proof for the next proposal.",
        )


class HubuConnectMonitor:
    """Checks whether Upwork proposal resources are sufficient before dispatch."""

    def inspect(
        self,
        scored: Iterable[ScoredOpportunity],
        available_connects: int | None,
    ) -> ConnectReport:
        decisions = []
        if available_connects is None:
            return ConnectReport(available_connects=None, decisions=())

        for item in scored:
            opportunity = item.opportunity
            if opportunity.platform.lower() != "upwork":
                continue
            if item.verdict != "apply":
                continue
            decisions.append(
                self._inspect_one(
                    title=opportunity.title,
                    required=opportunity.required_connects,
                    available=available_connects,
                )
            )

        return ConnectReport(available_connects=available_connects, decisions=tuple(decisions))

    @staticmethod
    def _inspect_one(title: str, required: int, available: int) -> ConnectDecision:
        if required <= 0:
            return ConnectDecision(
                opportunity_title=title,
                required_connects=required,
                available_connects=available,
                status="unknown",
                action="Open Upwork detail page and read required connects before dispatch.",
            )

        if available >= required:
            return ConnectDecision(
                opportunity_title=title,
                required_connects=required,
                available_connects=available,
                status="ready",
                action="Trigger 礼部 proposal drafting and final user approval.",
            )

        shortage = required - available
        return ConnectDecision(
            opportunity_title=title,
            required_connects=required,
            available_connects=available,
            status="blocked",
            action=f"Need {shortage} more connects before proposal can be submitted.",
        )


def demo_opportunities() -> tuple[Opportunity, ...]:
    return (
        Opportunity(
            title="Looking for a dev to fix a Claude Code workflow (MCP + Python + Google Sheets)",
            platform="Upwork",
            url="https://www.upwork.com/jobs/Looking-for-dev-fix-Claude-Code-workflow-MCP-Python-Google-Sheets_~022060129249474370493/",
            budget="Fixed price, estimated budget: $25",
            proposals="Fewer than 5",
            client_signal="Payment verified, 4.4 rating, $4K+ spent",
            tags=("Python", "Automation", "API", "Claude", "Google Sheets", "MCP"),
            required_connects=0,
            description="Broken Claude Code Desktop workflow with Python engine, bash wrapper, MCP servers, Meta Ads, Shopify, and Google Sheets. Needs reliability work.",
        ),
        Opportunity(
            title="Google Maps API",
            platform="Upwork",
            url="https://www.upwork.com/jobs/Google-Maps-API_~022060086389373582083/",
            budget="Hourly: $10.00 - $40.00",
            proposals="Fewer than 5",
            client_signal="Payment verified, new client",
            tags=("Google Maps API", "Google Sheets", "Apps Script", "API Integration"),
            required_connects=18,
            description="Connect property addresses in Google Sheets to Google Maps APIs, geocode addresses, generate Street View URLs, and populate sheet outputs.",
        ),
        Opportunity(
            title="Senior Python/AI Engineer - multi-agent SaaS",
            platform="Upwork",
            url="https://www.upwork.com/",
            budget="Hourly: $25.00 - $47.00",
            proposals="15 to 20",
            client_signal="Payment verified, 5.0 rating, $100K+ spent",
            tags=("Python", "FastAPI", "Supabase", "Claude", "Next.js"),
            description="Senior production multi-tenant SaaS, RLS, eval harness, Next.js UI, observability, 2-3 months.",
        ),
    )
