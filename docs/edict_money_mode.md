# Edict Money Mode

This repository now has a local, runnable prototype of a revenue-focused Edict workflow.

It follows the public Edict idea of:

```text
You -> 太子 -> 中书省 -> 门下省 -> 尚书省 -> 六部/吏部 -> 奏折
```

The point is not "agents talking for fun." The point is a controlled pipeline that finds work, filters it, wins it, ships it, and turns the result into stronger reputation.

## Offices

- 太子: classifies the user's mandate and turns vague intent into a clean task.
- 早朝官: gathers opportunity intelligence from Upwork, Handshake, and later other channels.
- 中书省: plans the business strategy and ranks opportunities.
- 门下省: reviews risks and vetoes bad jobs before spending connects or reputation.
- 尚书省: dispatches work to the right execution departments.
- 户部: handles pricing, budget, ROI, and effort estimates.
- 礼部: writes proposals, client updates, documentation, and handoff notes.
- 兵部: implements the actual technical work.
- 工部: handles setup, deployment, credentials, integrations, and operations.
- 刑部: reviews platform rules, privacy, contracts, and unsafe client requests.
- 吏部: tracks reputation, profile proof, reusable wins, and portfolio growth.

## Run It

```bash
python3 main.py --demo
```

This creates:

```text
output/edict_money_memorial.md
```

To simulate the Upwork connects gate:

```bash
python3 main.py --demo --connects 0
python3 main.py --demo --connects 20
```

The 户部 Connects Monitor blocks Upwork submissions when connects are insufficient and marks them ready when available connects meet the job requirement.

```text
IF available_connects >= required_connects
AND 门下省 verdict is apply
AND job is remote/online
THEN trigger 礼部 proposal drafting and final user approval
```

## Project Landing Loop

```text
find opportunity
score opportunity
draft proposal
user approves submission
client responds
intake materials
diagnose
build
review
deliver
ask for review
archive proof
```

## Channel Strategy

Use Handshake as the current volume channel because it supports remote internships and does not require Upwork connects. Use Upwork selectively only when 户部 confirms enough connects for a high-fit quick job. Add AI training and remote-job channels as pipeline expansion, but keep the same remote-only and safety filters.

Priority channels:

- Handshake: main daily application channel for remote internships, AI evaluation, software, data, and automation roles.
- Upwork: high-fit quick contracts only; blocked when connects are insufficient.
- AI training/evaluation: Handshake AI, DataAnnotation, Outlier, Alignerr, Mercor, micro1, Mindrift, RWS TrainAI, Welocalize.
- Remote startup/jobs: Wellfound, Y Combinator Work at a Startup, LinkedIn remote, Indeed remote, ZipRecruiter remote, RemoteOK, We Work Remotely.
- Freelance alternatives: Contra, Freelancer, Guru, PeoplePerHour, Fiverr. Use these after the resume, GitHub, and portfolio proof are stronger.

Daily target while reputation is low:

```text
3-5 Handshake remote applications
1-2 AI training/evaluation applications
0-2 Upwork proposals only when connects are available
1 portfolio/proof improvement
```

## Safety Rules

- Do not submit proposals without user approval.
- Do not spend connects without user approval.
- Do not claim experience we do not have.
- Do not move payment outside the platform.
- Do not ask the user to paste passwords or API secrets into chat.
- Do not accept projects with unclear scope unless the first milestone is paid discovery.
