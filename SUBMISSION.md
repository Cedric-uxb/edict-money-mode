# IBM Bob 2.0 Hackathon Submission Notes

## Project Title

Edict Work Mode: Proof Before Apply

## Submission Form Copy

### Submission Title

Edict Work Mode: Proof Before Apply

### Short Description

Edict helps early-career builders inspect work opportunities, veto unsafe requests, check proposal credits, and keep every application under human approval.

### Long Description

Students and early-career builders often face noisy opportunity pipelines: freelance jobs, internships, automation tasks, and remote roles. A listing can look attractive because it matches their technical skills, yet still contain unsafe conditions such as unpaid test work, off-platform payment, or credential sharing. Applying indiscriminately wastes time, proposal credits, and reputation.

Edict Work Mode turns this decision into a transparent workflow. A user pastes an opportunity, and Edict extracts common fields, scores fit, speed, trust, money, and risk, then returns apply, watch, or veto with reasons. A Connects gate checks whether the user has enough proposal credits, while every application, message, and spend remains under human approval. The interface makes the decision visible before action instead of automating a risky submission.

The project is designed for students and early-career AI builders who need a practical filter, not another generic task manager. Its key differentiator is reproducibility: twelve synthetic cases are stored in the repository with baseline and post-change reports. The baseline found three false negatives. One shared hard-veto rule raised exact agreement from 75% to 100% and veto recall from 57.14% to 100% while veto precision remained 100%. These are fixture results, not production or model-accuracy claims.

### IBM Bob Usage Statement

IBM Bob was used as a repository-context development partner during the original Edict prototype work. Bob reviewed `app.py`, `edict_money_team.py`, and the project documentation, explained the existing architecture, and recommended one focused improvement: add a pasted-opportunity input, convert the text into the existing `Opportunity` structure, and reuse the existing scoring and veto workflow instead of rebuilding the application. The accepted implementation is preserved in commit `61f2faa`, with corresponding parser tests and two screenshots in `docs/images/`.

Bob also proposed an IBM Granite or other LLM parser. We reviewed that suggestion but deliberately kept the first parser local and deterministic because it was sufficient for the proof of concept, avoided transmitting opportunity text, and preserved inspectability and human approval. `BOB.md` documents the accepted recommendation, evidence, and boundary. A new Bob session was attempted on September 27, 2026, but IBM returned `Account Not Ready Yet` and required a subscription; therefore the later twelve-case safety evaluation and hard-veto regression are not attributed to Bob. This separation keeps the submission specific and verifiable.

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
- Standard MIT License with copyright held by Qizhong Deng
- No private application logs, resumes, local paths, tokens, or credentials
