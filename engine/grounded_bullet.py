"""A deliberately narrow, fail-closed Fact Ledger and bullet renderer.

This is the first Phase 2B baseline. A model may select fact IDs, but it may not
submit free-form prose through this validator. The renderer owns every word of
the final bullet apart from values already present in the ledger.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FactSource = Literal["resume", "user_stated", "repo_derived", "placeholder"]


@dataclass(frozen=True)
class Fact:
    id: str
    claim_id: str
    key: str
    value: str | int | float | None
    source: FactSource
    evidence: str | None = None


@dataclass(frozen=True)
class BulletPlan:
    claim_id: str
    action_fact_id: str
    object_fact_id: str
    technology_fact_id: str | None = None
    outcome_fact_id: str | None = None


class LedgerError(ValueError):
    """A plan or ledger cannot support the requested output."""


class FactLedger:
    def __init__(self, facts: list[Fact] | tuple[Fact, ...]):
        self._facts: dict[str, Fact] = {}
        for fact in facts:
            if not fact.id or not fact.claim_id or not fact.key:
                raise LedgerError("fact id, claim id and key are required")
            if fact.id in self._facts:
                raise LedgerError(f"duplicate fact id: {fact.id}")
            if fact.source not in ("resume", "user_stated", "repo_derived", "placeholder"):
                raise LedgerError("unsupported fact source")
            if fact.source == "placeholder":
                if fact.value is not None:
                    raise LedgerError("placeholder fact must not have a value")
            elif fact.value is None or not str(fact.value).strip():
                raise LedgerError("non-placeholder fact needs a value")
            if fact.source != "placeholder" and not fact.evidence:
                raise LedgerError("non-placeholder facts need an evidence reference")
            self._facts[fact.id] = fact

    def require(self, fact_id: str, claim_id: str, key: str) -> Fact:
        fact = self._facts.get(fact_id)
        if fact is None:
            raise LedgerError(f"unknown fact id: {fact_id}")
        if fact.claim_id != claim_id:
            raise LedgerError("fact belongs to another claim")
        if fact.key != key:
            raise LedgerError(f"expected {key} fact, got {fact.key}")
        if fact.source == "placeholder":
            raise LedgerError("missing evidence: placeholder cannot be exported")
        return fact


def _safe_value(fact: Fact) -> str:
    value = str(fact.value).strip()
    if not value or "\n" in value or "\r" in value or len(value) > 160:
        raise LedgerError("fact value must be a short, single-line phrase")
    return value


def render_bullet(ledger: FactLedger, plan: BulletPlan) -> str:
    """Render only ledger-backed slots, using a fixed sentence structure."""
    if not plan.claim_id:
        raise LedgerError("claim id is required")
    action = _safe_value(ledger.require(plan.action_fact_id, plan.claim_id, "action"))
    obj = _safe_value(ledger.require(plan.object_fact_id, plan.claim_id, "object"))
    # Keep the action slot to a single verb. Richer phrasing needs a later,
    # separately tested validator rather than unconstrained model prose.
    if not action.isalpha() or " " in action:
        raise LedgerError("action must be a single alphabetic verb")
    bullet = f"{action[0].upper()}{action[1:]} {obj}"
    if plan.technology_fact_id is not None:
        tech = _safe_value(ledger.require(plan.technology_fact_id, plan.claim_id, "technology"))
        bullet += f" using {tech}"
    if plan.outcome_fact_id is not None:
        outcome = _safe_value(ledger.require(plan.outcome_fact_id, plan.claim_id, "outcome"))
        bullet += f"; {outcome}"
    return bullet + "."


def validate_bullet(text: str, ledger: FactLedger, plan: BulletPlan) -> bool:
    """Accept only the exact deterministic rendering of a vetted fact plan."""
    return text == render_bullet(ledger, plan)
