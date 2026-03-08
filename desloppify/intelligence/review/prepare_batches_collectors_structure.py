"""Collector helpers for org/state/auth/migration dimensions."""

from __future__ import annotations

from desloppify.intelligence.review._context.models import HolisticContext

from .prepare_batches_core import _collect_unique_files, _representative_files_for_directory


def _authorization_files(
    ctx: HolisticContext,
    *,
    max_files: int | None = None,
) -> list[str]:
    """Files relevant to authorization dimension."""
    auth_ctx = ctx.authorization
    auth_files: list[dict] = []
    for rpath, info in auth_ctx.get("route_auth_coverage", {}).items():
        if info.get("without_auth", 0) > 0:
            auth_files.append({"file": rpath})
    for rpath in auth_ctx.get("service_role_usage", []):
        auth_files.append({"file": rpath})
    rls_coverage = auth_ctx.get("rls_coverage", {})
    rls_files = rls_coverage.get("files", {})
    if isinstance(rls_files, dict):
        for file_paths in rls_files.values():
            if isinstance(file_paths, list):
                for filepath in file_paths:
                    auth_files.append({"file": filepath})
    return _collect_unique_files([auth_files], max_files=max_files)


def _ai_debt_files(
    ctx: HolisticContext,
    *,
    max_files: int | None = None,
) -> list[str]:
    """Files relevant to AI debt/migration dimensions."""
    ai_debt = ctx.ai_debt_signals
    migration = ctx.migration_signals
    debt_files: list[dict] = []
    for rpath in ai_debt.get("file_signals", {}):
        debt_files.append({"file": rpath})
    dep_files = migration.get("deprecated_markers", {}).get("files")
    if isinstance(dep_files, dict):
        for entry in dep_files:
            debt_files.append({"file": entry})
    for entry in migration.get("migration_todos", []):
        debt_files.append({"file": entry.get("file", "")})
    return _collect_unique_files([debt_files], max_files=max_files)


def _package_org_files(
    ctx: HolisticContext,
    *,
    max_files: int | None = None,
) -> list[str]:
    """Files relevant to package organization dimensions."""
    structure = ctx.structure
    struct_files: list[dict] = []
    for entry in structure.get("flat_dir_issues", []):
        if isinstance(entry, dict):
            directory = entry.get("directory", "")
            for filepath in _representative_files_for_directory(ctx, directory):
                struct_files.append({"file": filepath})
    for root_file in structure.get("root_files", []):
        if root_file.get("role") == "peripheral":
            struct_files.append({"file": root_file["file"]})
    dir_profiles = structure.get("directory_profiles", {})
    largest_dirs = sorted(
        dir_profiles.items(),
        key=lambda item: -item[1].get("file_count", 0),
    )[:3]
    for dir_key, profile in largest_dirs:
        for fname in profile.get("files", [])[:3]:
            dir_path = dir_key.rstrip("/")
            rpath = f"{dir_path}/{fname}" if dir_path != "." else fname
            struct_files.append({"file": rpath})
    coupling_matrix = structure.get("coupling_matrix", {})
    seen_edges: set[str] = set()
    for edge in coupling_matrix:
        if " → " not in edge:
            continue
        left, right = edge.split(" → ", 1)
        reverse = f"{right} → {left}"
        if reverse in coupling_matrix and edge not in seen_edges:
            seen_edges.add(edge)
            seen_edges.add(reverse)
            for directory in (left, right):
                for fname in dir_profiles.get(directory, {}).get("files", [])[:2]:
                    dir_path = directory.rstrip("/")
                    rpath = f"{dir_path}/{fname}" if dir_path != "." else fname
                    struct_files.append({"file": rpath})
    return _collect_unique_files([struct_files], max_files=max_files)


def _state_design_files(
    ctx: HolisticContext,
    *,
    max_files: int | None = None,
) -> list[str]:
    """Files relevant to state/design integrity dimensions."""
    evidence = ctx.scan_evidence
    mutable_files = [
        item for item in evidence.get("mutable_globals", []) if isinstance(item, dict)
    ]
    complexity_files = [
        item
        for item in evidence.get("complexity_hotspots", [])[:10]
        if isinstance(item, dict)
    ]
    error_files = [
        item for item in evidence.get("error_hotspots", [])[:10] if isinstance(item, dict)
    ]
    density_files = [
        {"file": item["file"]}
        for item in evidence.get("signal_density", [])[:10]
        if isinstance(item, dict) and item.get("file")
    ]
    return _collect_unique_files(
        [mutable_files, complexity_files, error_files, density_files],
        max_files=max_files,
    )


__all__ = [
    "_ai_debt_files",
    "_authorization_files",
    "_package_org_files",
    "_state_design_files",
]
