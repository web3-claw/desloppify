"""Compatibility facade for TypeScript pattern consistency detection."""

from __future__ import annotations

from desloppify.languages.typescript.detectors.patterns_analysis import (
    _build_census,
    detect_pattern_anomalies,
    detect_pattern_anomalies_result,
)
from desloppify.languages.typescript.detectors.patterns_catalog import PATTERN_FAMILIES
from desloppify.languages.typescript.detectors.patterns_cli import cmd_patterns

__all__ = [
    "PATTERN_FAMILIES",
    "_build_census",
    "cmd_patterns",
    "detect_pattern_anomalies",
    "detect_pattern_anomalies_result",
]
