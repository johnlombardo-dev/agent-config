from __future__ import annotations

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SKILL_ROOT.parents[1]


class MapLunaContractsTests(unittest.TestCase):
    def test_map_owns_only_set_level_coordination(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())

        for phrase in (
            "dependency-aware contract map",
            "../shape-luna-contract/SKILL.md",
            "Do not copy, summarize, or redefine those rules here",
            "## Set validity",
            "Complete",
            "Non-overlapping",
            "Connected",
            "Closed",
            "## Contract graph",
            "## Shared-surface ledger",
            "## Unified validation plan",
            "dispatch waves",
            "CRITERION | PRODUCING NODES | OBSERVING CHECK",
        ):
            self.assertIn(phrase, normalized)

        self.assertNotIn("## Compact worker contract", skill)
        self.assertNotIn("## Full additions", skill)

    def test_goal_coverage_counts_all_execution_nodes(self) -> None:
        skill = " ".join(
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").split()
        )

        for phrase in (
            "owning execution node and an observing validation check",
            "The mapped execution-node set must be",
            "whether it is a shaped Luna contract or a `requires-higher-capability` escalation node",
            "each high-capability escalation node's acceptance and verification checks",
            "SURFACE | NODES | MUTATION OWNER/ORDER",
            "CRITERION | PRODUCING NODES | OBSERVING CHECK",
            "a `requires-higher-capability` node contributes the acceptance and verification checks",
        ):
            self.assertIn(phrase, skill)

        self.assertNotIn("maps to at least one contract", skill)
        self.assertNotIn("CRITERION | PRODUCING CONTRACTS", skill)

    def test_map_preserves_non_luna_work(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized = " ".join(skill.split())

        for phrase in (
            "A per-node `ESCALATE` becomes a `requires-higher-capability` graph node",
            "do not split it again to manufacture Luna work",
            "before splitting it",
            "do not partition it by state, transition, file, or implementation step",
            "highest-capability implementation route with effort selected independently",
            "`ultra` is forbidden",
            "`n/a` for `requires-higher-capability`",
            "one indivisible high-capability state-chart node",
        ):
            self.assertIn(phrase, normalized)

        self.assertIn("Only `ready` contracts may be dispatched to Luna", normalized)
        self.assertIn("Do not invent a Luna prompt", normalized)

    def test_component_successors_cannot_diverge_from_the_map(self) -> None:
        skill = " ".join(
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").split()
        )

        self.assertIn("provisional `NEXT` must be `none`", skill)
        self.assertIn("match an existing successor and dependency or reshape trigger", skill)
        self.assertIn("The graph is authoritative", skill)

    def test_dependency_blocked_nodes_remain_unshaped(self) -> None:
        skill = " ".join(
            (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").split()
        )

        for phrase in (
            "Do not apply the shaper to an outcome whose named graph dependencies are incomplete",
            "unshaped `blocked-by-dependency` node",
            "Apply `shape-luna-contract` only to outcomes whose named dependencies are satisfied now",
            "`unshaped` for `blocked-by-dependency` and `reshape-after-evidence`",
            "it owns no mutation authority",
            "`WAVE` is only the earliest candidate wave, not dispatch authority",
            "reapply `shape-luna-contract` against the current fingerprint",
        ):
            self.assertIn(phrase, skill)

        self.assertNotIn("the contract is fully shaped but awaits", skill)

    def test_map_is_not_the_default_orchestrator_path(self) -> None:
        for consumer_name in ("scale-sol-luna-goals", "deliver-sol-luna-goals"):
            consumer = REPOSITORY_ROOT / "skills" / consumer_name / "SKILL.md"
            text = " ".join(consumer.read_text(encoding="utf-8").split())

            self.assertIn("../shape-luna-contract/SKILL.md", text)
            self.assertIn("`map-luna-contracts` is not part of this canonical path", text)
            self.assertIn("user separately asks", text)
            self.assertNotIn("../map-luna-contracts/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
