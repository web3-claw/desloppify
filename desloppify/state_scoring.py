"""State scoring facade."""

from __future__ import annotations

from typing import NamedTuple

from desloppify.engine._state.schema import StateModel
from desloppify.engine._state.schema_scores import (
    get_objective_score,
    get_overall_score,
    get_strict_score,
    get_verified_strict_score,
)
from desloppify.engine._state.scoring import suppression_metrics


class ScoreSnapshot(NamedTuple):
    """All four canonical scores from a single state dict."""

    overall: float | None
    objective: float | None
    strict: float | None
    verified: float | None


def _score_reader_functions():
    return (
        get_overall_score,
        get_objective_score,
        get_strict_score,
        get_verified_strict_score,
    )


def score_snapshot(state: StateModel) -> ScoreSnapshot:
    """Load all four canonical scores from *state* in one call."""
    overall_fn, objective_fn, strict_fn, verified_fn = _score_reader_functions()
    return ScoreSnapshot(
        overall=overall_fn(state),
        objective=objective_fn(state),
        strict=strict_fn(state),
        verified=verified_fn(state),
    )


__all__ = [
    "ScoreSnapshot",
    "get_objective_score",
    "get_overall_score",
    "get_strict_score",
    "get_verified_strict_score",
    "score_snapshot",
    "suppression_metrics",
]
