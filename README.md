# Edict Money Mode

Edict Money Mode is a small Python command center for a revenue-focused agent workflow. It models an "imperial court" team that can inspect work opportunities, score them, block bad fits, check Upwork connects, and produce a concrete action memorial.

The project is intentionally practical: it is built around finding remote software, automation, AI, and data work, then turning each project into stronger portfolio proof.

## What It Does

- Scores opportunities by fit, speed, trust, money, and risk.
- Blocks unsafe or unrealistic jobs before wasting reputation.
- Checks whether Upwork connects are sufficient before proposal work starts.
- Produces a Markdown "memorial" with ranked opportunities and next actions.
- Defines execution departments for proposals, engineering, deployment, compliance, and reputation.

## Court Structure

```text
User mandate
  -> 太子: classify the request
  -> 早朝官: gather opportunity intelligence
  -> 中书省: rank and plan
  -> 门下省: veto bad work
  -> 尚书省: dispatch execution
  -> 户部: budget and connects
  -> 礼部: proposals and communication
  -> 兵部: implementation
  -> 工部: deployment and operations
  -> 刑部: compliance and safety
  -> 吏部: reputation and portfolio proof
```

## Quick Start

```bash
python3 main.py --demo
```

Simulate the Upwork connects gate:

```bash
python3 main.py --demo --connects 0
python3 main.py --demo --connects 20
```

The command writes:

```text
output/edict_money_memorial.md
```

`output/` is ignored by git because local runs may contain private application notes. A public sample is included at [examples/sample_memorial.md](examples/sample_memorial.md).

## Example Use Case

The demo ranks opportunities such as:

- AI automation fixes
- Google Sheets and API integrations
- small Python workflow debugging jobs
- risky senior-only projects that should be vetoed

The goal is not to apply everywhere. The goal is to choose a small batch of realistic remote opportunities, prepare honest proposals, and ship work that creates review-worthy proof.

## Safety Rules

- Do not submit proposals without final user approval.
- Do not spend Upwork connects without approval.
- Do not claim skills or experience that are not true.
- Do not move payment outside the platform.
- Do not store secrets, resumes, or application logs in the public repo.

## Project Status

This is an early local prototype. Next planned improvements:

- Add real platform importers for Handshake and Upwork job snapshots.
- Add proposal drafting templates.
- Add delivery checklists for accepted projects.
- Add a small web dashboard for the court flow and opportunity board.

