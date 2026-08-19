from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]
CONTRACT_SKILL_ROOT = REPOSITORY_ROOT / "skills" / "shape-luna-contract"


class NoReviewPhaseTests(unittest.TestCase):
    def test_active_skill_contract_has_no_review_phase(self) -> None:
        active_files = [
            SKILL_ROOT / "SKILL.md",
            SKILL_ROOT / "agents" / "openai.yaml",
            SKILL_ROOT / "references" / "runtime-routing.md",
            SKILL_ROOT / "references" / "task-packets.md",
            CONTRACT_SKILL_ROOT / "SKILL.md",
        ]
        active_text = "\n".join(
            path.read_text(encoding="utf-8") for path in active_files
        )

        for obsolete in (
            "review-convergence",
            "review-agent",
            "review-phase",
            "hosted review",
            "local gate",
            "hosted gate",
        ):
            self.assertNotIn(obsolete, active_text)

        self.assertFalse((SKILL_ROOT / "references" / "review-convergence.md").exists())

    def test_delivery_does_not_start_a_replacement_review_loop(self) -> None:
        delivery = (SKILL_ROOT / "references" / "delivery.md").read_text(
            encoding="utf-8"
        )
        metrics = (SKILL_ROOT / "references" / "outcome-metrics.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("SSLG has no code-review phase", delivery)
        self.assertIn("Do not request code review", delivery)
        self.assertIn("Append `subagent_started`", metrics)
        self.assertIn("Append `subagent_outcome`", metrics)
        self.assertIn("It never modifies an existing line", metrics)
        self.assertIn("must not calculate durations", metrics)

    def test_pre_delivery_qa_keeps_the_four_risk_classes(self) -> None:
        skill = (CONTRACT_SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized_skill = " ".join(skill.lower().split())
        single_line_skill = " ".join(skill.split())

        for risk_class in (
            "value integrity",
            "accessibility and interaction",
            "public contract",
            "lifecycle and rendering",
        ):
            self.assertIn(risk_class, normalized_skill)

        for bounded_requirement in (
            "one or two affected QA seams",
            "one invariant",
            "cheapest faithful check",
            "one adjacent counterexample",
        ):
            self.assertIn(bounded_requirement, single_line_skill)

        orchestrator = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Reuse unchanged baselines and successful checks", orchestrator)


if __name__ == "__main__":
    unittest.main()
