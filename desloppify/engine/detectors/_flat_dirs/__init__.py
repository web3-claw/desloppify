"""Internal helpers for the flat-directory detector."""

from .config import FlatDirDetectionConfig
from .detect import detect_flat_dirs
from .entries import format_flat_dir_summary

__all__ = ["FlatDirDetectionConfig", "detect_flat_dirs", "format_flat_dir_summary"]
