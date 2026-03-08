"""Flat directory detection facade.

The implementation is split across ``desloppify.engine.detectors._flat_dirs``
modules to keep this public module small while preserving the existing import
surface.
"""

from __future__ import annotations

from ._flat_dirs.config import (
    DEFAULT_THIN_WRAPPER_NAMES,
    THIN_WRAPPER_NAMES,
    FlatDirDetectionConfig,
    resolve_detection_settings,
)
from ._flat_dirs.detect import detect_flat_dirs
from ._flat_dirs.entries import (
    format_flat_dir_summary,
    fragmentation_entry,
    is_overloaded,
    sort_entries,
    thin_wrapper_entry,
)
from ._flat_dirs.stats import all_tracked_dirs, build_dir_stats

_DEFAULT_THIN_WRAPPER_NAMES = DEFAULT_THIN_WRAPPER_NAMES
_resolve_detection_settings = resolve_detection_settings
_build_dir_stats = build_dir_stats
_all_tracked_dirs = all_tracked_dirs
_is_overloaded = is_overloaded
_fragmentation_entry = fragmentation_entry
_thin_wrapper_entry = thin_wrapper_entry
_sort_entries = sort_entries

__all__ = [
    "FlatDirDetectionConfig",
    "THIN_WRAPPER_NAMES",
    "detect_flat_dirs",
    "format_flat_dir_summary",
]
