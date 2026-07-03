import unittest

from edict_money_team import EdictMoneyTeam, HubuConnectMonitor, Opportunity, parse_opportunity_text


class EdictMoneyTeamTests(unittest.TestCase):
    def test_high_fit_quick_job_is_apply(self):
        team = EdictMoneyTeam()
        scored = team.score(
            Opportunity(
                title="Fix Python Google Sheets automation",
                platform="Upwork",
                url="https://example.com/job",
                budget="Hourly: $10.00 - $40.00",
                proposals="Fewer than 5",
                client_signal="Payment verified, 5.0 rating",
                tags=("Python", "Google Sheets", "API", "Automation"),
                description="Small script fix for an API workflow.",
                required_connects=8,
            )
        )

        self.assertEqual(scored.verdict, "apply")
        self.assertGreaterEqual(scored.total, 27)
        self.assertGreater(len(scored.rationale), 0, "Rationale should be provided for apply verdict")
        self.assertTrue(
            any("Low proposal count" in reason for reason in scored.rationale),
            "Should mention low proposal count as a positive factor"
        )

    def test_senior_long_term_work_is_vetoed(self):
        team = EdictMoneyTeam()
        scored = team.score(
            Opportunity(
                title="Senior production-grade multi-tenant SaaS",
                platform="Upwork",
                url="https://example.com/job",
                budget="Hourly: $25.00 - $47.00",
                proposals="50+",
                client_signal="Payment verified",
                tags=("Python", "Kubernetes", "Terraform"),
                description="Senior long-term production-grade SaaS with SOC 2 and GDPR requirements.",
            )
        )

        self.assertEqual(scored.verdict, "veto")
        self.assertGreater(len(scored.rationale), 0, "Rationale should be provided for veto verdict")
        self.assertTrue(
            any("Risk is high" in reason for reason in scored.rationale),
            "Should mention high risk for veto verdict"
        )

    def test_connect_monitor_blocks_when_connects_are_insufficient(self):
        team = EdictMoneyTeam()
        scored = [
            team.score(
                Opportunity(
                    title="Fix Python Google Sheets API automation",
                    platform="Upwork",
                    url="https://example.com/job",
                    budget="Hourly: $10.00 - $40.00",
                    proposals="Fewer than 5",
                    client_signal="Payment verified, 5.0 rating",
                    tags=("Python", "Google Sheets", "API", "Automation", "workflow"),
                    description="Small script fix for a Google Sheets API automation workflow.",
                    required_connects=18,
                )
            )
        ]

        report = HubuConnectMonitor().inspect(scored, available_connects=5)

        self.assertEqual(report.decisions[0].status, "blocked")
        self.assertIn("Need 13 more connects", report.decisions[0].action)

    def test_parse_opportunity_text_extracts_common_job_fields(self):
        opportunity = parse_opportunity_text(
            """
            Fix Google Sheets API automation
            Platform: Upwork
            Budget: Hourly: $10.00 - $40.00
            Proposals: Fewer than 5
            Client: Payment verified, 5.0 rating
            Connects: 8
            Skills: Python, Google Sheets, API, Automation

            Need a small script fix for a Google Sheets API workflow.
            """
        )

        self.assertEqual(opportunity.title, "Fix Google Sheets API automation")
        self.assertEqual(opportunity.platform, "Upwork")
        self.assertEqual(opportunity.budget, "Hourly: $10.00 - $40.00")
        self.assertEqual(opportunity.proposals, "Fewer than 5")
        self.assertEqual(opportunity.client_signal, "Payment verified, 5.0 rating")
        self.assertEqual(opportunity.required_connects, 8)
        self.assertIn("Python", opportunity.tags)

    def test_parse_opportunity_text_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            parse_opportunity_text("  \n  ")


if __name__ == "__main__":
    unittest.main()
