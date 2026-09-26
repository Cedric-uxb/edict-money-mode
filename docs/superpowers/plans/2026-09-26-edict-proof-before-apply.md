# Edict Proof Before Apply Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make IBM Bob 2.0's repository-level contribution measurable by adding a reproducible opportunity-screening evaluation, fixing three verified high-risk false negatives, and documenting the real Bob workflow.

**Architecture:** Keep the existing deterministic `EdictMoneyTeam` and Streamlit UI. Add one JSONL fixture set and one standard-library evaluation script; use the results to drive a minimal shared risk-rule change in `edict_money_team.py`. Store the baseline and post-change reports as JSON, then explain only observed Bob actions and verified numbers in `BOB.md` and the existing challenge documents.

**Tech Stack:** Python 3, `unittest`, JSONL, Streamlit, IBM Bob 2.0.

---

### Task 1: Add The Reproducible Evaluation Contract

**Files:**
- Create: `evals/cases.jsonl`
- Create: `tests/test_evals.py`
- Create: `evals/run_eval.py`

- [ ] **Step 1: Write the 12 labeled synthetic cases**

Create `evals/cases.jsonl` with exactly these newline-delimited JSON objects. The cases are synthetic; no real client text or account data is allowed.

```jsonl
{"id":"safe-python-fix","expected":"apply","title":"Fix Python Google Sheets automation","platform":"Upwork","url":"https://example.com/safe-python-fix","budget":"Hourly: $10.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified, 5.0 rating","description":"Small script fix for an API workflow.","tags":["Python","Google Sheets","API","Automation"],"required_connects":8}
{"id":"safe-maps-api","expected":"apply","title":"Google Maps API spreadsheet integration","platform":"Upwork","url":"https://example.com/safe-maps-api","budget":"Hourly: $20.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified","description":"Simple Apps Script setup for a Google Sheets workflow.","tags":["Google Maps API","Google Sheets","Apps Script","API Integration"],"required_connects":12}
{"id":"senior-saas","expected":"veto","title":"Senior production-grade multi-tenant SaaS","platform":"Upwork","url":"https://example.com/senior-saas","budget":"Hourly: $25.00 - $47.00","proposals":"50+","client_signal":"Payment verified","description":"Long-term Kubernetes and Terraform platform requiring SOC 2 and GDPR ownership.","tags":["Python","Kubernetes","Terraform"],"required_connects":18}
{"id":"unrelated-admin","expected":"veto","title":"Copy handwritten addresses into a document","platform":"Upwork","url":"https://example.com/unrelated-admin","budget":"Fixed price","proposals":"10 to 15","client_signal":"Payment verified","description":"Manual data entry with no software or automation work.","tags":["Data Entry"],"required_connects":6}
{"id":"moderate-api-review","expected":"watch","title":"API script with partially defined scope","platform":"Upwork","url":"https://example.com/moderate-api-review","budget":"Hourly: $10.00 - $40.00","proposals":"10 to 15","client_signal":"Payment verified","description":"A script is needed, but acceptance criteria will be supplied after kickoff.","tags":["Python","Automation","API"],"required_connects":10}
{"id":"low-value-entry","expected":"veto","title":"Basic form entry","platform":"Upwork","url":"https://example.com/low-value-entry","budget":"Fixed price","proposals":"20 to 50","client_signal":"New client","description":"Repeated manual form entry with no automation scope.","tags":["Data Entry"],"required_connects":8}
{"id":"slow-platform-rebuild","expected":"veto","title":"Production-grade Kubernetes platform rebuild","platform":"Upwork","url":"https://example.com/slow-platform-rebuild","budget":"Hourly: $30 - $40","proposals":"15 to 20","client_signal":"Payment verified","description":"Senior long-term multi-tenant system with Terraform and warranty requirements.","tags":["Python","Kubernetes","Terraform"],"required_connects":20}
{"id":"safe-chatbot-fix","expected":"apply","title":"Fix a small Python chatbot API","platform":"Upwork","url":"https://example.com/safe-chatbot-fix","budget":"Hourly: $10.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified, 4.8 rating","description":"Simple workflow fix with one failing example and clear output.","tags":["Python","Chatbot","API","Workflow"],"required_connects":8}
{"id":"unpaid-test","expected":"veto","title":"Python automation fix with unpaid test task","platform":"Upwork","url":"https://example.com/unpaid-test","budget":"Hourly: $10.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified, 5.0 rating","description":"Complete an unpaid test task before a contract is offered. Small script and API workflow.","tags":["Python","Automation","API","Google Sheets","Workflow","Chatbot","MCP","OpenAI"],"required_connects":8}
{"id":"off-platform-crypto","expected":"veto","title":"Fast Python API automation paid outside Upwork","platform":"Upwork","url":"https://example.com/off-platform-crypto","budget":"Hourly: $10.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified, 5.0 rating","description":"Client requires crypto payment outside Upwork after a simple script fix.","tags":["Python","Automation","API","Google Sheets","Workflow","Chatbot","MCP","OpenAI"],"required_connects":8}
{"id":"credential-sharing","expected":"veto","title":"Repair a Python workflow using shared login credentials","platform":"Upwork","url":"https://example.com/credential-sharing","budget":"Hourly: $10.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified, 5.0 rating","description":"Client asks the freelancer to share login credentials and send a password before the small API script fix.","tags":["Python","Automation","API","Google Sheets","Workflow","Chatbot","MCP","OpenAI"],"required_connects":8}
{"id":"safe-unknown-connects","expected":"apply","title":"Fix a simple Apps Script workflow","platform":"Upwork","url":"https://example.com/safe-unknown-connects","budget":"Hourly: $20.00 - $40.00","proposals":"Fewer than 5","client_signal":"Payment verified, 4.9 rating","description":"Small Google Sheets automation with one reproducible failure.","tags":["Apps Script","Google Sheets","Automation","API"],"required_connects":0}
```

- [ ] **Step 2: Write the failing evaluation tests**

Create `tests/test_evals.py`:

```python
import json
import unittest
from pathlib import Path

from evals.run_eval import evaluate_cases, load_cases


CASES_PATH = Path(__file__).resolve().parents[1] / "evals" / "cases.jsonl"


class EvaluationTests(unittest.TestCase):
    def test_fixture_contract_is_complete_and_unique(self):
        cases = load_cases(CASES_PATH)

        self.assertEqual(12, len(cases))
        self.assertEqual(12, len({case["id"] for case in cases}))
        self.assertEqual(
            {"apply", "watch", "veto"},
            {case["expected"] for case in cases},
        )

    def test_evaluation_report_is_serializable_and_bounded(self):
        report = evaluate_cases(load_cases(CASES_PATH))

        json.dumps(report)
        self.assertEqual(12, report["case_count"])
        for name in ("agreement", "veto_precision", "veto_recall"):
            self.assertGreaterEqual(report[name], 0.0)
            self.assertLessEqual(report[name], 1.0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest tests.test_evals -v
```

Expected: import failure because `evals.run_eval` does not exist.

- [ ] **Step 4: Implement the smallest evaluation harness**

Create `evals/run_eval.py`:

```python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from edict_money_team import EdictMoneyTeam, Opportunity


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        case = json.loads(line)
        if not isinstance(case, dict) or "id" not in case or "expected" not in case:
            raise ValueError(f"Invalid case at line {line_number}")
        cases.append(case)
    return cases


def evaluate_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    team = EdictMoneyTeam()
    results = []
    for case in cases:
        opportunity_fields = {
            key: value
            for key, value in case.items()
            if key not in {"id", "expected"}
        }
        opportunity_fields["tags"] = tuple(opportunity_fields.get("tags", ()))
        predicted = team.score(Opportunity(**opportunity_fields)).verdict
        results.append(
            {
                "id": case["id"],
                "expected": case["expected"],
                "predicted": predicted,
                "match": predicted == case["expected"],
            }
        )

    true_positive = sum(
        item["expected"] == "veto" and item["predicted"] == "veto"
        for item in results
    )
    predicted_positive = sum(item["predicted"] == "veto" for item in results)
    actual_positive = sum(item["expected"] == "veto" for item in results)
    matches = sum(item["match"] for item in results)
    return {
        "case_count": len(results),
        "agreement": matches / len(results) if results else 0.0,
        "veto_precision": true_positive / predicted_positive if predicted_positive else 0.0,
        "veto_recall": true_positive / actual_positive if actual_positive else 0.0,
        "mismatches": [item for item in results if not item["match"]],
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Edict verdict rules")
    parser.add_argument("--cases", type=Path, default=Path("evals/cases.jsonl"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = evaluate_cases(load_cases(args.cases))
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run the focused and full suites**

Run:

```bash
python3 -m unittest tests.test_evals -v
python3 -m unittest discover -s tests -p "test*.py" -v
```

Expected: 2 evaluation tests pass; all existing tests remain green.

- [ ] **Step 6: Commit the evaluation contract**

```bash
git add evals/cases.jsonl evals/run_eval.py tests/test_evals.py
git commit -m "test: add Edict opportunity evaluation set"
```

### Task 2: Capture The Unmodified Baseline

**Files:**
- Create: `evals/baseline.json`

- [ ] **Step 1: Generate the baseline before changing scoring rules**

Run:

```bash
python3 evals/run_eval.py --output evals/baseline.json
```

Expected: JSON contains 12 cases and lists `unpaid-test`, `off-platform-crypto`, and `credential-sharing` among the mismatches.

- [ ] **Step 2: Verify the report is reproducible**

Record the generated file hash, run the same command again, then compare hashes:

```bash
shasum -a 256 evals/baseline.json > /tmp/edict-baseline.sha256
python3 evals/run_eval.py --output evals/baseline.json
shasum -a 256 -c /tmp/edict-baseline.sha256
```

Expected: `evals/baseline.json: OK`.

- [ ] **Step 3: Commit the observed baseline without editing its numbers**

```bash
git add evals/baseline.json
git commit -m "test: record Edict baseline evaluation"
```

### Task 3: Use IBM Bob To Diagnose The Three False Negatives

**Files:**
- Modify after Bob review: `edict_money_team.py`
- Modify after Bob review: `tests/test_edict_money_team.py`
- Create after Bob review: `BOB.md`

- [ ] **Step 1: Give Bob the repository-context task**

In IBM Bob 2.0, open this repository and send this exact request:

```text
Read edict_money_team.py, tests/test_edict_money_team.py, evals/cases.jsonl, and evals/baseline.json. Explain why unpaid-test, off-platform-crypto, and credential-sharing are false negatives. Propose the smallest shared change that makes those cases veto without changing the public Opportunity or ScoredOpportunity data structures. Add failing unittest coverage first, then implement the fix and run the full test suite plus python3 evals/run_eval.py. Do not add an LLM, dependency, network request, or unrelated refactor.
```

- [ ] **Step 2: Review Bob's proposal before accepting changes**

Accept only a shared risk-rule change in `_risk_penalty` plus focused tests. Reject changes that add dependencies, change unrelated scoring dimensions, fabricate evaluation numbers, or create automatic proposal submission.

- [ ] **Step 3: Write the failing hard-veto test if Bob did not produce it correctly**

Add this method to `EdictMoneyTeamTests`:

```python
    def test_hard_veto_signals_override_positive_fit(self):
        team = EdictMoneyTeam()
        for description in (
            "Complete an unpaid test task before contract.",
            "Accept crypto payment outside Upwork.",
            "Share login credentials and send a password.",
        ):
            with self.subTest(description=description):
                scored = team.score(
                    Opportunity(
                        title="Fast Python API automation",
                        platform="Upwork",
                        url="https://example.com/synthetic-risk",
                        budget="Hourly: $10.00 - $40.00",
                        proposals="Fewer than 5",
                        client_signal="Payment verified, 5.0 rating",
                        description=description,
                        tags=(
                            "Python", "Automation", "API", "Google Sheets",
                            "Workflow", "Chatbot", "MCP", "OpenAI",
                        ),
                        required_connects=8,
                    )
                )
                self.assertEqual("veto", scored.verdict)
                self.assertGreaterEqual(scored.risk, 8)
```

- [ ] **Step 4: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest tests.test_edict_money_team.EdictMoneyTeamTests.test_hard_veto_signals_override_positive_fit -v
```

Expected: FAIL because the current positive signals outweigh each unsafe phrase.

- [ ] **Step 5: Apply the minimum shared fix**

At module level in `edict_money_team.py`, add:

```python
HARD_VETO_SIGNALS = (
    "unpaid test",
    "free test task",
    "outside upwork",
    "crypto payment",
    "pay in crypto",
    "share login credentials",
    "send a password",
    "credential sharing",
)
```

At the start of `_risk_penalty`, add:

```python
        if any(signal in text for signal in HARD_VETO_SIGNALS):
            return 10
```

- [ ] **Step 6: Verify GREEN and run the full suite**

Run:

```bash
python3 -m unittest tests.test_edict_money_team.EdictMoneyTeamTests.test_hard_veto_signals_override_positive_fit -v
python3 -m unittest discover -s tests -p "test*.py" -v
```

Expected: all tests pass.

- [ ] **Step 7: Record only real Bob evidence**

Create `BOB.md` with the exact prompt used, files Bob actually inspected, Bob's diagnosis, accepted diff, rejected suggestions and reasons, commands actually run, and their real outputs. Do not write a result that was not observed in Bob or the terminal.

- [ ] **Step 8: Commit the Bob-driven fix and evidence**

```bash
git add edict_money_team.py tests/test_edict_money_team.py BOB.md
git commit -m "fix: veto unsafe opportunity signals"
```

### Task 4: Record The Post-Change Evaluation

**Files:**
- Create: `evals/after.json`
- Test: `tests/test_evals.py`

- [ ] **Step 1: Add a regression assertion for the three fixed cases**

Add this method to `EvaluationTests`:

```python
    def test_known_high_risk_cases_are_vetoed(self):
        report = evaluate_cases(load_cases(CASES_PATH))
        predictions = {
            item["id"]: item["predicted"] for item in report["results"]
        }

        for case_id in (
            "unpaid-test",
            "off-platform-crypto",
            "credential-sharing",
        ):
            self.assertEqual("veto", predictions[case_id])
```

- [ ] **Step 2: Generate the post-change report**

Run:

```bash
python3 evals/run_eval.py --output evals/after.json
```

Expected: veto recall and exact agreement are greater than or equal to their values in `evals/baseline.json`, and all three target cases predict `veto`.

- [ ] **Step 3: Compare reports without hand-editing metrics**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path

before = json.loads(Path("evals/baseline.json").read_text())
after = json.loads(Path("evals/after.json").read_text())
assert after["agreement"] >= before["agreement"]
assert after["veto_recall"] >= before["veto_recall"]
print({
    "agreement": [before["agreement"], after["agreement"]],
    "veto_recall": [before["veto_recall"], after["veto_recall"]],
})
PY
```

Expected: assertions pass and the terminal prints the observed before/after values.

- [ ] **Step 4: Commit the verified report**

```bash
git add evals/after.json tests/test_evals.py
git commit -m "test: record Bob-assisted evaluation improvement"
```

### Task 5: Reframe The Public Evidence And Demo

**Files:**
- Modify: `README.md`
- Modify: `SUBMISSION.md`
- Modify: `demo_script.md`
- Modify: `项目总纲.md`

- [ ] **Step 1: Update README with observed evidence**

Add a concise section near the top containing: the `Proof Before Apply` one-line claim; links to `evals/cases.jsonl`, `evals/baseline.json`, `evals/after.json`, and `BOB.md`; the observed before/after agreement and veto recall; and an explicit note that this is a small synthetic rule evaluation, not model accuracy or proof of employment suitability.

- [ ] **Step 2: Replace the demo story with one path**

Make `demo_script.md` show only: paste the `unpaid-test` case, run the workflow, show the veto and rationale, show the before/after report, show the Connects approval gate, and finish on `BOB.md`. Keep spoken material under 2 minutes 40 seconds.

- [ ] **Step 3: Update submission fields without overclaiming**

Use `Edict Work Mode: Proof Before Apply` as the title and describe IBM Bob as the repository-context development partner that diagnosed three measured false negatives and verified the fix. Do not claim that Bob is embedded at runtime or that the synthetic fixture set measures real-world accuracy.

- [ ] **Step 4: Run final verification**

Run:

```bash
python3 -m unittest discover -s tests -p "test*.py" -v
python3 evals/run_eval.py
git diff --check
git grep -nE '(/Users/dengxu|@drew\.edu|ASSEMBLYAI_API_KEY=.+|gh[pousr]_[A-Za-z0-9]+)' -- .
```

Expected: tests pass; evaluation is reproducible; `git diff --check` passes; secret/path scan has no private-value matches.

- [ ] **Step 5: Commit challenge documentation**

```bash
git add README.md SUBMISSION.md demo_script.md 项目总纲.md
git commit -m "docs: present Edict proof-before-apply evidence"
```
