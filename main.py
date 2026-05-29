from __future__ import annotations

import argparse
from pathlib import Path

from edict_money_team import EdictMoneyTeam, demo_opportunities


def run_demo(available_connects: int) -> Path:
    team = EdictMoneyTeam()
    memorial = team.run(
        mandate="Build a 三省六部 agent team that finds paid work, wins quick jobs, lands projects, and turns delivery into reputation.",
        opportunities=demo_opportunities(),
        available_connects=available_connects,
    )

    output_path = Path("output/edict_money_memorial.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(memorial.to_markdown(), encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Edict local command center")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the revenue-focused 三省六部 workflow on sample opportunities.",
    )
    parser.add_argument(
        "--connects",
        type=int,
        default=0,
        help="Available Upwork connects for 户部 resource checks.",
    )
    args = parser.parse_args()

    if args.demo:
        output_path = run_demo(args.connects)
        print(f"Edict Money Mode memorial written to {output_path}")
        return

    print("Use: python3 main.py --demo")


if __name__ == "__main__":
    main()
