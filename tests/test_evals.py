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

    def test_known_high_risk_cases_are_vetoed(self):
        report = evaluate_cases(load_cases(CASES_PATH))
        predictions = {item["id"]: item["predicted"] for item in report["results"]}

        for case_id in ("unpaid-test", "off-platform-crypto", "credential-sharing"):
            self.assertEqual("veto", predictions[case_id])


if __name__ == "__main__":
    unittest.main()
