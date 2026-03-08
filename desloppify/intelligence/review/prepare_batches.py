"""Holistic investigation batch builders for review preparation.

Public API compatibility facade over split helper modules.
"""

from __future__ import annotations

from .prepare_batches_builders import (
    batch_concerns,
    build_investigation_batches,
    filter_batches_to_dimensions,
)
from .prepare_batches_collectors import _DIMENSION_FILE_MAPPING, _FILE_COLLECTORS
from .prepare_batches_core import (
    _collect_files_from_batches,
    _collect_unique_files,
    _ensure_holistic_context,
    _normalize_file_path,
    _representative_files_for_directory,
)

__all__ = ["batch_concerns", "build_investigation_batches", "filter_batches_to_dimensions"]
