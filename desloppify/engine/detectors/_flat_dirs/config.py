"""Configuration model and defaults for flat-directory detection."""

from __future__ import annotations

from dataclasses import dataclass

THIN_WRAPPER_NAMES = frozenset(
    {
        "components",
        "hooks",
        "utils",
        "services",
        "state",
        "contexts",
        "contracts",
        "types",
        "models",
        "adapters",
        "helpers",
        "core",
        "common",
    }
)
DEFAULT_THIN_WRAPPER_NAMES = (
    "components",
    "hooks",
    "utils",
    "services",
    "state",
    "contexts",
    "contracts",
    "types",
    "models",
    "adapters",
    "helpers",
    "core",
    "common",
)


@dataclass(frozen=True)
class FlatDirDetectionConfig:
    """Thresholds and heuristics for flat directory detection."""

    threshold: int = 20
    child_dir_threshold: int = 10
    child_dir_weight: int = 3
    combined_threshold: int = 30
    sparse_parent_child_threshold: int = 8
    sparse_child_file_threshold: int = 1
    sparse_child_count_threshold: int = 6
    sparse_child_ratio_threshold: float = 0.7
    thin_wrapper_parent_sibling_threshold: int = 10
    thin_wrapper_max_file_count: int = 1
    thin_wrapper_max_child_dir_count: int = 1
    thin_wrapper_names: tuple[str, ...] = DEFAULT_THIN_WRAPPER_NAMES


def resolve_detection_settings(
    *,
    threshold: int,
    config: FlatDirDetectionConfig | None,
    child_dir_threshold: int,
    child_dir_weight: int,
    combined_threshold: int,
    sparse_parent_child_threshold: int,
    sparse_child_file_threshold: int,
    sparse_child_count_threshold: int,
    sparse_child_ratio_threshold: float,
    thin_wrapper_parent_sibling_threshold: int,
    thin_wrapper_max_file_count: int,
    thin_wrapper_max_child_dir_count: int,
    thin_wrapper_names: tuple[str, ...],
) -> FlatDirDetectionConfig:
    """Return explicit settings, preferring an already-built config object."""
    if config is not None:
        return config
    return FlatDirDetectionConfig(
        threshold=threshold,
        child_dir_threshold=child_dir_threshold,
        child_dir_weight=child_dir_weight,
        combined_threshold=combined_threshold,
        sparse_parent_child_threshold=sparse_parent_child_threshold,
        sparse_child_file_threshold=sparse_child_file_threshold,
        sparse_child_count_threshold=sparse_child_count_threshold,
        sparse_child_ratio_threshold=sparse_child_ratio_threshold,
        thin_wrapper_parent_sibling_threshold=thin_wrapper_parent_sibling_threshold,
        thin_wrapper_max_file_count=thin_wrapper_max_file_count,
        thin_wrapper_max_child_dir_count=thin_wrapper_max_child_dir_count,
        thin_wrapper_names=thin_wrapper_names,
    )


__all__ = [
    "DEFAULT_THIN_WRAPPER_NAMES",
    "FlatDirDetectionConfig",
    "THIN_WRAPPER_NAMES",
    "resolve_detection_settings",
]
