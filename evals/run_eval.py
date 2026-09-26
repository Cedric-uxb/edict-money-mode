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
            key: value for key, value in case.items() if key not in {"id", "expected"}
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
