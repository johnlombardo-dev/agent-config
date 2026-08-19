from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]


class ShapeLunaContractTests(unittest.TestCase):
    def test_skill_shapes_exactly_one_next_dispatch(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())

        for phrase in (
            "exactly one dependency-ready worker contract",
            "Optimize for the next dispatch",
            "Name at most one provisional successor",
            "Re-shape after integration, a blocker, or a material scope revision",
            "A map is not a prerequisite for this skill",
            "Defined",
            "Decision-ready",
            "Safe",
            "Checkable",
            "## Compact worker contract",
            "## Full additions",
            "READY",
            "PREREQUISITE",
            "NO-OP",
        ):
            self.assertIn(phrase, normalized)

        self.assertNotIn("dispatch waves", normalized)
        self.assertNotIn("shared-surface ledger", normalized)

    def test_statechart_work_is_a_hard_high_capability_escalation(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())

        for phrase in (
            "## Luna eligibility gate",
            "designs or implements a state-chart, state machine, actor protocol",
            "Never split an escalated outcome merely to avoid the escalation",
            "fixes the capability floor and reasoning effort independently",
            "Use `xhigh` by default for state-chart design",
            "Use `max` only when a named irreducible interaction spans",
            "A state-chart label, file count, or broad task size does not independently justify `max`",
            "unnecessary `max` reasoning can reopen frozen decisions",
            "Never select `ultra`",
            "If the selected route is unavailable, the work remains pending rather than falling back to Luna",
            "caller-approved bounded coupled-decision mandate",
            "`ESCALATE`",
        ):
            self.assertIn(phrase, normalized)

    def test_shaper_returns_logical_routes_and_leaves_runtime_fields_to_caller(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())

        for phrase in (
            "logical parent-only record",
            "do not fill caller-owned runtime fields",
            "ROUTE REQUIREMENT: execution-worker role",
            "Those fields are not part of the shaper result",
            "The caller must freeze the coupled questions",
        ):
            self.assertIn(phrase.lower(), normalized.lower())

        self.assertNotIn("ROUTE: logical role, current runtime mapping", skill)

    def test_orchestrators_use_singular_shaper_without_duplicate_schema(self) -> None:
        for consumer_name in ("scale-sol-luna-goals", "deliver-sol-luna-goals"):
            consumer = REPOSITORY_ROOT / "skills" / consumer_name
            skill = (consumer / "SKILL.md").read_text(encoding="utf-8")
            routing = (consumer / "references" / "runtime-routing.md").read_text(
                encoding="utf-8"
            )
            normalized_consumer = " ".join(skill.split())

            self.assertIn("../shape-luna-contract/SKILL.md", skill)
            self.assertIn("exactly one dependency-ready outcome", skill)
            self.assertIn("Never send an `ESCALATE` outcome to Luna", skill)
            self.assertIn("Luna work must also be Decision-ready", normalized_consumer)
            self.assertIn("bounded coupled-decision mandate", skill)
            self.assertIn("accepted escalation envelope", skill)
            self.assertIn("caller-owned runtime fields", skill)
            self.assertIn("GPT-5.6 Sol with `high`, `xhigh`, or `max` effort", routing)
            self.assertIn("Use `xhigh` by default to design or semantically verify", routing)
            self.assertIn("When selecting `max`, record the trigger", routing)
            self.assertIn("Never use `ultra`", routing)
            self.assertIn("Do not silently substitute", routing)
            self.assertIn("bounded coupled-decision mandate", routing)
            self.assertIn("must return any decision", routing)
            self.assertNotIn("## Compact worker contract", skill)
            self.assertNotIn("## Full additions", skill)

        deliver_skill = (
            REPOSITORY_ROOT / "skills" / "deliver-sol-luna-goals" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "An indivisible escalation may instead proceed to shaping",
            " ".join(deliver_skill.split()),
        )

        scale_packets = (
            REPOSITORY_ROOT
            / "skills"
            / "scale-sol-luna-goals"
            / "references"
            / "task-packets.md"
        ).read_text(encoding="utf-8")
        normalized_packets = " ".join(scale_packets.split())
        self.assertNotIn("Compact Luna contract", scale_packets)
        self.assertNotIn("Full Luna additions", scale_packets)
        self.assertIn("$shape-luna-contract at the orchestrator-resolved skill path", scale_packets)
        self.assertIn("Use exactly one return envelope", scale_packets)
        self.assertIn("MODE: research or shaped", scale_packets)
        self.assertIn(
            "use `MODE: research` and `STATUS: GO`, `NO-GO`, or `PREREQUISITE`",
            scale_packets,
        )
        self.assertIn(
            "use `MODE: shaped` and `STATUS: READY`, `ESCALATE`",
            scale_packets,
        )
        self.assertIn("does not wrap or rename the final shaper status", normalized_packets)
        self.assertNotIn("RETURN: GO, NO-GO, ESCALATE, or PREREQUISITE", scale_packets)


if __name__ == "__main__":
    unittest.main()
