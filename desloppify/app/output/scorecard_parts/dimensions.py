"""App-facing compatibility re-exports for scorecard dimension policy."""

from __future__ import annotations

from desloppify.engine.planning.scorecard_dimensions import (
    SCORECARD_MAX_DIMENSIONS,
    collapse_elegance_dimensions,
    limit_scorecard_dimensions,
    prepare_scorecard_dimensions,
    resolve_scorecard_lang,
)

__all__ = [
    "SCORECARD_MAX_DIMENSIONS",
    "collapse_elegance_dimensions",
    "prepare_scorecard_dimensions",
    "limit_scorecard_dimensions",
    "resolve_scorecard_lang",
]
