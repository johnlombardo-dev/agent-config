from __future__ import annotations

import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]


class SkillRequirementTests(unittest.TestCase):
    def test_discovery_skill_routes_ten_lanes_and_keeps_executable_evidence(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        techniques = (SKILL_ROOT / "references" / "evidence-techniques.md").read_text(
            encoding="utf-8"
        )

        for lane in (
            "Domain and value integrity",
            "Accessibility and interaction",
            "Public contract",
            "Lifecycle and resource ownership",
            "Security, privacy, and trust",
            "Persistence, migration, and recovery",
            "Concurrency, workflow, and ordering",
            "Performance, capacity, and backpressure",
            "External protocol and integration",
            "Operations, configuration, and deployment",
        ):
            self.assertIn(lane, skill)

        for technique in (
            "closure matrix",
            "observable read",
            "fake, stub, or recorded fixture",
            "public boundaries",
            "property or metamorphic checks",
            "differential probes",
            "shared-oracle parity matrices",
            "covering arrays",
            "targeted mutations",
        ):
            self.assertIn(technique, techniques)

        self.assertIn("A path or keyword alone", skill)
        self.assertIn("More than three lanes", skill)
        self.assertIn("`exercised`, `gap`, or `not applicable`", skill)
        self.assertIn("A finding settles only its violated invariant", skill)
        self.assertIn("Do not call a lane complete", skill)
        self.assertIn("ROUTING:", skill)
        lanes = SKILL_ROOT / "references" / "lanes"
        self.assertEqual(len(list(lanes.glob("*.md"))), 10)

    def test_lane_oracles_cover_escaped_system_review_blind_spots(self) -> None:
        lanes = SKILL_ROOT / "references" / "lanes"
        expected = {
            "performance-capacity-backpressure.md": (
                "each independent scale variable",
                "public boundary",
            ),
            "persistence-migration-recovery.md": (
                "durable artifact set",
                "every retained artifact",
            ),
            "security-privacy-trust.md": (
                "attacker-known",
                "recompute dependent fields",
                "transition that can begin",
                "acting credential cannot mint",
                "authenticated context",
                "re-exports",
                "incremental ceilings",
                "output policies",
                "runtime reachability",
            ),
            "operations-configuration-deployment.md": (
                "prove invocation",
                "resulting operational state",
            ),
        }
        for filename, phrases in expected.items():
            playbook = (lanes / filename).read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase, playbook)

    def test_skills_keep_bounded_authority_and_results(self) -> None:
        discovery = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        repair = (REPOSITORY_ROOT / "skills" / "verify-repair-seam" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("Do not implement fixes", discovery)
        self.assertIn("Stop after this batch", discovery)
        self.assertIn("does not own implementation", discovery)
        self.assertIn("verified | failed | blocked", repair)
        self.assertIn("Do not edit the repair", repair)
        self.assertIn("Stop after this seam", repair)

    def test_state_machine_warning_and_benchmark_thresholds_remain(self) -> None:
        agents = (REPOSITORY_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        benchmark = (SKILL_ROOT / "references" / "benchmark.md").read_text(encoding="utf-8")

        self.assertIn("emergent state machines and actor-like protocols", agents)
        self.assertIn("Recommend XState v5", agents)
        self.assertIn("The worst state machine is the one you don't know you're writing.", agents)
        self.assertIn("25 percent more weighted recall", benchmark)
        self.assertIn("five-point precision loss", benchmark)
        self.assertIn("60 percent of baseline token cost", benchmark)
        self.assertIn("cross-boundary cases", benchmark)
        self.assertIn("composed outcome fails", benchmark)

    def test_failed_pilot_is_not_wired_into_sslg(self) -> None:
        report = json.loads(
            (SKILL_ROOT / "evals" / "pilot-holdout-report.json").read_text(encoding="utf-8")
        )
        sslg = (
            REPOSITORY_ROOT / "skills" / "scale-sol-luna-goals" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertFalse(report["discovery"]["gate_passed"])
        self.assertFalse(report["repair"]["gate_passed"])
        self.assertNotIn("$evidence-first-review", sslg)
        self.assertNotIn("$verify-repair-seam", sslg)


if __name__ == "__main__":
    unittest.main()
