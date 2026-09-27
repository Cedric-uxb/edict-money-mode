# IBM Bob 2.0 Hackathon Submission Notes

## Project Title

Edict Work Mode: Proof Before Apply

## Challenge Theme

IBM Bob 2.0 Hackathon

## Short Description

Edict Work Mode helps students and early-career builders evaluate work opportunities before spending time, proposal credits, or reputation. It explains each decision, blocks unsafe requests, checks Connects, and keeps submission under human approval.

## Problem

Opportunity pipelines are noisy. Students and early-career builders need a safer way to decide which work is realistic, valuable, and worth pursuing before they spend time, proposal credits, or reputation.

## Solution

The prototype combines transparent fit, speed, trust, money, and risk scoring with hard safety vetoes and a Connects approval gate. A 12-case synthetic evaluation makes rule changes reproducible.

## IBM Bob Usage

Verified IBM Bob work includes:

- Repository-level architecture review
- Identification of a minimal pasted-opportunity parsing workflow
- Reuse of the existing `Opportunity`, scoring, and veto path
- Human review of Bob's broader LLM suggestion before implementation

Evidence is saved in:

- `docs/images/bob_july_project_context.png`
- `docs/images/bob_july_review_recommendation.png`
- `BOB.md`
- commit `61f2faa`

The later synthetic evaluation and hard-veto regression change are not attributed to Bob. A new Bob session was attempted on September 27, but the account returned `Account Not Ready Yet` because a subscription was required.

## Verified Evaluation

- 12 synthetic cases
- Exact agreement: 75.00% to 100.00%
- Veto recall: 57.14% to 100.00%
- Veto precision remained 100.00%
- 9 unit tests passing

These numbers describe the included synthetic rule fixture, not production accuracy.

## Required Links

- GitHub URL: https://github.com/Cedric-uxb/edict-money-mode
- Existing demo video URL: https://drive.google.com/file/d/1RVfHEPMVbFyakTAJXxxs_2ns2aY7pcq1/view
- Refreshed Proof Before Apply demo: pending recording

## Technologies

IBM Bob, Python, Streamlit, pandas, unittest

## Submission Checklist

- Public GitHub repository
- Working prototype or proof of concept
- Clear README with challenge theme, problem, solution, AI approach, architecture, and IBM Bob usage
- Public demo video, maximum 3 minutes
- IBM Bob evidence screenshots in `docs/images/`
- Reproducible baseline and after reports in `evals/`
- No private application logs, resumes, local paths, tokens, or credentials
