"""Top-level batch building APIs for holistic review preparation."""

from __future__ import annotations

from pathlib import Path

from .prepare_batches_collectors import _DIMENSION_FILE_MAPPING, _FILE_COLLECTORS
from .prepare_batches_core import (
    _collect_files_from_batches,
    _ensure_holistic_context,
    _normalize_file_path,
)


def build_investigation_batches(
    holistic_ctx,
    lang: object,
    *,
    repo_root: Path | None = None,
    max_files_per_batch: int | None = None,
) -> list[dict]:
    """Build one batch per dimension from holistic context."""
    ctx = _ensure_holistic_context(holistic_ctx)
    del lang
    del repo_root

    file_cache: dict[str, list[str]] = {}
    batches: list[dict] = []

    for dimension, collector_key in _DIMENSION_FILE_MAPPING.items():
        if collector_key not in file_cache:
            collector = _FILE_COLLECTORS[collector_key]
            file_cache[collector_key] = collector(
                ctx,
                max_files=max_files_per_batch,
            )

        files = file_cache[collector_key]
        if not files:
            continue

        batches.append(
            {
                "name": dimension,
                "dimensions": [dimension],
                "files_to_read": files,
                "why": f"seed files for {dimension} review",
            }
        )

    return batches


def filter_batches_to_dimensions(
    batches: list[dict],
    dimensions: list[str],
    *,
    fallback_max_files: int | None = 80,
) -> list[dict]:
    """Keep only batches whose dimension is in the active set."""
    selected = [dimension for dimension in dimensions if isinstance(dimension, str) and dimension]
    if not selected:
        return []
    selected_set = set(selected)
    filtered: list[dict] = []
    covered: set[str] = set()
    for batch in batches:
        batch_dims = [dim for dim in batch.get("dimensions", []) if dim in selected_set]
        if not batch_dims:
            continue
        filtered.append({**batch, "dimensions": batch_dims})
        covered.update(batch_dims)

    missing = [dim for dim in selected if dim not in covered]
    if not missing:
        return filtered

    max_files = fallback_max_files if isinstance(fallback_max_files, int) else None
    if isinstance(max_files, int) and max_files <= 0:
        max_files = None
    fallback_files = _collect_files_from_batches(
        filtered or batches,
        max_files=max_files,
    )
    if not fallback_files:
        return filtered

    for dim in missing:
        filtered.append(
            {
                "name": dim,
                "dimensions": [dim],
                "files_to_read": fallback_files,
                "why": f"no direct batch mapping for {dim}; using representative files",
            }
        )
    return filtered


def batch_concerns(
    concerns: list,
    *,
    max_files: int | None = None,
    active_dimensions: list[str] | None = None,
) -> dict | None:
    """Build investigation batch from mechanical concern signals."""
    del active_dimensions
    if not concerns:
        return None

    types = sorted({concern.type for concern in concerns if concern.type})
    why_parts = ["mechanical detectors identified structural patterns needing judgment"]
    if types:
        why_parts.append(f"concern types: {', '.join(types)}")

    files: list[str] = []
    seen: set[str] = set()
    concern_signals: list[dict[str, object]] = []
    for concern in concerns:
        candidate = _normalize_file_path(getattr(concern, "file", ""))
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        files.append(candidate)

        evidence_raw = getattr(concern, "evidence", ())
        evidence = [
            str(entry).strip()
            for entry in evidence_raw
            if isinstance(entry, str) and entry.strip()
        ][:4]
        summary = str(getattr(concern, "summary", "")).strip()
        question = str(getattr(concern, "question", "")).strip()
        concern_type = str(getattr(concern, "type", "")).strip()
        concern_signals.append(
            {
                "type": concern_type or "design_concern",
                "file": candidate,
                "summary": summary or "Mechanical concern requires subjective judgment",
                "question": question or "Is this pattern intentional or debt?",
                "evidence": evidence,
            }
        )

    total_candidate_files = len(files)
    if (
        max_files is not None
        and isinstance(max_files, int)
        and max_files > 0
        and total_candidate_files > max_files
    ):
        files = files[:max_files]
        why_parts.append(
            f"truncated to {max_files} files from {total_candidate_files} candidates"
        )

    return {
        "name": "design_coherence",
        "dimensions": ["design_coherence"],
        "files_to_read": files,
        "why": "; ".join(why_parts),
        "total_candidate_files": total_candidate_files,
        "concern_signals": concern_signals[:12],
        "concern_signal_count": len(concern_signals),
    }


__all__ = ["batch_concerns", "build_investigation_batches", "filter_batches_to_dimensions"]
