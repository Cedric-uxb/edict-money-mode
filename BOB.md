# IBM Bob Development Evidence

This file separates verified IBM Bob work from later repository changes.

## Verified Bob Contribution

IBM Bob reviewed the Edict repository during the July 2026 prototype work. The retained evidence shows Bob working with the project and recommending one focused improvement: accept pasted opportunity text, convert it into the existing `Opportunity` structure, and reuse the existing scoring and veto workflow.

Evidence:

- `docs/images/bob_july_project_context.png` shows IBM Bob open with the Edict repository and tests.
- `docs/images/bob_july_review_recommendation.png` shows Bob's repository-level recommendation.
- Commit `61f2faa` implements the accepted improvement in `app.py`, `edict_money_team.py`, and `tests/test_edict_money_team.py`.

The full original prompt was not retained, so this repository does not claim an exact prompt transcript. The visible Bob task title starts with `Review app.py, edict_money_team...`.

## Recommendation Review

Bob suggested a text area for unstructured opportunity input and proposed IBM Granite, with other LLMs as fallback, for extraction. The accepted part was the small input-to-`Opportunity` workflow. The prototype kept extraction local and deterministic instead of adding an external model dependency because that was enough for a reproducible, privacy-preserving proof of concept.

This preserved:

- the existing scoring and veto logic;
- human approval before applications or Connects spending;
- inspectable behavior without sending opportunity text to an external service.

## Reproducible Safety Evaluation

In September 2026, a separate local evaluation was added with 12 synthetic cases:

| Metric | Baseline | After risk-rule hardening |
|---|---:|---:|
| Exact agreement | 75.00% | 100.00% |
| Veto precision | 100.00% | 100.00% |
| Veto recall | 57.14% | 100.00% |

The three baseline false negatives were unpaid test work, off-platform cryptocurrency payment, and credential sharing. The follow-up change added one shared hard-veto rule and regression tests.

These figures come from a small synthetic rule fixture, not a learned model, production traffic, or a claim of real-world accuracy. This September change is not attributed to Bob.

Reproduce it with:

```bash
python3 -m unittest discover -s tests -p "test*.py" -v
python3 evals/run_eval.py
```

## Current Access Note

On September 27, 2026, a new Bob review was attempted. IBM authentication succeeded, but the service returned `Account Not Ready Yet` and stated that a subscription was required. No new Bob response or code change was produced in that attempt, so none is claimed here.
