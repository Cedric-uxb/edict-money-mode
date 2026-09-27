# Edict Work Mode: Proof Before Apply

Edict Work Mode is a transparent decision-support prototype for checking work opportunities before a user spends time, proposal credits, or reputation.

It scores opportunities, blocks bad fits and unsafe requests, checks resource constraints, and produces a concrete action plan while keeping every external action under human approval.

## Reproducible Safety Result

The repository includes 12 synthetic opportunity cases and stores both reports:

| Metric | [Baseline](evals/baseline.json) | [After](evals/after.json) |
|---|---:|---:|
| Exact agreement | 75.00% | 100.00% |
| Veto precision | 100.00% | 100.00% |
| Veto recall | 57.14% | 100.00% |

The fixed cases cover unpaid test work, off-platform cryptocurrency payment, and credential sharing. See the [fixture set](evals/cases.jsonl), [evaluation script](evals/run_eval.py), and [IBM Bob evidence log](BOB.md).

This is a small synthetic rule evaluation. It is not model accuracy, production validation, or proof that an opportunity is suitable for employment.

## IBM Technology Evidence

IBM Bob reviewed the repository and identified the opportunity parsing improvement implemented in commit `61f2faa`. The screenshots and [development evidence log](BOB.md) distinguish that verified work from later local evaluation changes.

![IBM Bob open on the July project](docs/images/bob_july_project_context.png)

![IBM Bob reviewing the July project architecture](docs/images/bob_july_review_recommendation.png)

## Challenge Fit

- Challenge: IBM Bob 2.0 Hackathon, September 2026
- Project story: Proof Before Apply
- Focus: workflow automation, decision intelligence, and human-approved AI co-worker behavior

## Problem Statement

Students and early-career builders often face noisy opportunity pipelines: freelance projects, internships, AI evaluation work, automation tasks, and remote roles. Applying everywhere wastes time and can create reputation risk.

The problem is not only finding opportunities. The harder problem is deciding which ones are safe, realistic, worth pursuing, and aligned with current proof of skill.

## Solution

Edict Work Mode turns opportunity review into a structured decision workflow.

It:

- Scores opportunities by fit, speed, trust, money, and risk.
- Parses pasted opportunity text into structured fields for scoring.
- Vetoes unrealistic or unsafe work before action.
- Checks whether proposal credits/connects are sufficient.
- Produces recommended next actions.
- Keeps final submission, spending, and client communication under human approval.

## AI Approach and Architecture

The prototype models an AI-assisted "court" workflow. Each department has a narrow responsibility:

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

The current proof of concept uses deterministic Python scoring rules so every decision can be inspected. Future versions can add IBM Granite or another language model layer for opportunity parsing and proposal drafting, while keeping the same human approval gates.

The pasted-text parser is intentionally local and transparent for the demo. It extracts common fields such as platform, budget, proposal count, client signal, skills, and required connects without sending private opportunity text to an external service.

## IBM Bob Usage

IBM Bob was used during the original prototype development.

Bob was used to:

- Review `app.py`, `edict_money_team.py`, and `README.md`.
- Explain the current architecture and challenge fit.
- Identify strengths, limitations, and weak assumptions in the prototype.
- Recommend one high-impact, minimal next improvement: adding opportunity parsing while reusing the existing scoring and veto workflow.
- Keep file changes human-approved instead of letting the assistant submit or spend anything automatically.

The evidence screenshots are shown near the top of this README and saved in `docs/images/`. `BOB.md` records the accepted recommendation, the implementation commit, and the current access limitation without attributing later work to Bob.

## Project Structure

```text
.
├── app.py                    # Streamlit prototype
├── BOB.md                    # Verified Bob contribution and evidence boundary
├── edict_money_team.py       # Decision workflow and scoring logic
├── evals/                    # Synthetic cases and before/after reports
├── main.py                   # Command-line demo
├── examples/sample_memorial.md
├── docs/edict_money_mode.md
├── tests/test_edict_money_team.py
├── requirements.txt
└── SUBMISSION.md
```

## Quick Start

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Run the command-line demo:

```bash
python3 main.py --demo --connects 20
```

Run tests:

```bash
python3 -m unittest discover -s tests -p "test*.py" -v
python3 evals/run_eval.py
```

Run the Streamlit prototype:

```bash
python3 -m streamlit run app.py
```

## Safety and Privacy

- The public repo uses sanitized example opportunities.
- Real application logs, resumes, private notes, and proposal drafts must stay out of Git.
- The system does not submit proposals or spend proposal credits automatically.
- Human approval is required before any external action.

## Limitations

This is a proof of concept. The scoring rules and synthetic labels were written by the project author and are intentionally small. The app does not import live platform data, establish identity or eligibility, guarantee safety, draft final proposals, or submit applications.

## Future Improvements

- Add CSV/JSON import for opportunity snapshots.
- Add an IBM Granite or other LLM-powered parser for unstructured opportunity text.
- Add proposal drafting with mandatory human approval.
- Add a persistent opportunity board.
- Add a richer web dashboard and explainability view.
