import unittest

from edict_money_team import EdictMoneyTeam, HubuConnectMonitor, Opportunity


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


if __name__ == "__main__":
    unittest.main()
