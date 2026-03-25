"""Architecture critique engine -- evaluate agent specs against best practices."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CritiqueResult:
    """Result of evaluating an agent spec."""

    warnings: list[str] = field(default_factory=list)
    score: dict[str, int] = field(default_factory=dict)
    # score keys: safety, completeness, maintainability
    # each 0-100

    @property
    def total_score(self) -> int:
        """Weighted average: safety 50%, completeness 30%, maint 20%."""
        s = self.score.get("safety", 0)
        c = self.score.get("completeness", 0)
        m = self.score.get("maintainability", 0)
        return int(s * 0.5 + c * 0.3 + m * 0.2)

    @property
    def grade(self) -> str:
        """Letter grade based on total score."""
        t = self.total_score
        if t >= 90:
            return "A"
        if t >= 80:
            return "B"
        if t >= 70:
            return "C"
        if t >= 60:
            return "D"
        return "F"


def critique(spec: dict[str, object]) -> CritiqueResult:
    """Evaluate an agent spec and return warnings + scores.

    Checks:
    1. Safety: Are DENY policies defined? Are critical actions denied?
    2. Completeness: Does spec have skills, persona, description?
    3. Maintainability: Is complexity reasonable?
    """
    result = CritiqueResult()

    # --- Safety checks ---
    safety_score = 100
    policies = spec.get("policies", {})
    if not isinstance(policies, dict):
        policies = {}

    deny_list = policies.get("deny", [])
    if not isinstance(deny_list, list):
        deny_list = []

    if not deny_list:
        result.warnings.append(
            "SAFETY: No DENY policies defined. Consider denying "
            "dangerous actions "
            "(delete_file, send_email, deploy, payment)."
        )
        safety_score -= 40

    critical_denies = {
        "delete_file",
        "send_email",
        "deploy",
        "payment",
    }
    missing_critical = critical_denies - {
        str(d) for d in deny_list
    }
    if missing_critical and deny_list:
        result.warnings.append(
            "SAFETY: Missing recommended DENY actions: "
            f"{', '.join(sorted(missing_critical))}."
        )
        safety_score -= 5 * len(missing_critical)

    ask_list = policies.get("ask", [])
    if not isinstance(ask_list, list):
        ask_list = []

    if not ask_list and not deny_list:
        result.warnings.append(
            "SAFETY: No ASK policies defined either. "
            "The agent has unrestricted permissions."
        )
        safety_score -= 20

    # --- Completeness checks ---
    completeness_score = 100

    if not spec.get("description"):
        result.warnings.append(
            "COMPLETENESS: No description provided."
        )
        completeness_score -= 20

    skills = spec.get("skills", [])
    if not isinstance(skills, list):
        skills = []

    if not skills:
        result.warnings.append(
            "COMPLETENESS: No skills defined. "
            "The agent may lack specific capabilities."
        )
        completeness_score -= 15

    persona = spec.get("persona", {})
    if not isinstance(persona, dict) or not persona:
        result.warnings.append(
            "COMPLETENESS: No persona defined. "
            "Default tone will be used."
        )
        completeness_score -= 10

    if not spec.get("name"):
        result.warnings.append(
            "COMPLETENESS: No agent name provided."
        )
        completeness_score -= 20

    # --- Maintainability checks ---
    maintainability_score = 100

    if len(skills) > 5:
        result.warnings.append(
            f"MAINTAINABILITY: {len(skills)} skills defined. "
            "Consider reducing to <=5 to keep the agent focused."
        )
        maintainability_score -= 10 * (len(skills) - 5)

    agents = spec.get("agents", [])
    if isinstance(agents, list) and len(agents) > 4:
        result.warnings.append(
            f"MAINTAINABILITY: {len(agents)} agents in "
            "multi-agent setup. "
            "Consider simplifying to <=4 agents."
        )
        maintainability_score -= 15

    # Persona + policy conflict check
    if persona and isinstance(persona, dict):
        tone = str(persona.get("tone", "")).lower()
        if (
            tone in ("aggressive", "confrontational")
            and len(deny_list) > 5
        ):
            result.warnings.append(
                "MAINTAINABILITY: Aggressive persona combined "
                "with many DENY rules may create conflicting "
                "agent behavior."
            )
            maintainability_score -= 15

    # Clamp scores
    result.score = {
        "safety": max(0, min(100, safety_score)),
        "completeness": max(0, min(100, completeness_score)),
        "maintainability": max(
            0, min(100, maintainability_score)
        ),
    }

    return result
