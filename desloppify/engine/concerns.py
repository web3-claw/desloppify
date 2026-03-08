"""Concern generators — mechanical issues → subjective review bridge.

This module remains the stable import surface for external callers and tests.
Implementation details are split into ``desloppify.engine._concerns`` modules to
keep this facade small while preserving backwards compatibility.
"""

from __future__ import annotations

from ._concerns.generators import (
    _cross_file_patterns,
    _file_concerns,
    cleanup_stale_dismissals,
    generate_concerns,
)
from ._concerns.signals import (
    _extract_signals,
    _has_elevated_signals,
    _parse_complexity_signals,
)
from ._concerns.state import _group_by_file, _open_issues
from ._concerns.text import _build_evidence, _build_question, _build_summary, _classify
from ._concerns.types import Concern
from ._concerns.utils import _fingerprint, _is_dismissed

__all__ = ["Concern", "cleanup_stale_dismissals", "generate_concerns"]
