"""Compatibility re-exports for triage helper APIs.

Active command code imports the bounded modules directly. This facade remains
for older imports and focused tests while the package migrates.
"""

from __future__ import annotations

from .completion_flow import apply_completion, count_log_activity_since
from .observe_batches import (
    group_issues_into_observe_batches,
    observe_dimension_breakdown,
)
from .review_coverage import (
    active_triage_issue_ids,
    clear_active_triage_issue_tracking,
    cluster_issue_ids,
    ensure_active_triage_issue_ids,
    find_cluster_for,
    has_open_review_issues,
    live_active_triage_issue_ids,
    manual_clusters_with_issues,
    open_review_ids_from_state,
    plan_review_ids,
    sync_undispositioned_triage_meta,
    triage_coverage,
    undispositioned_triage_issue_ids,
)
from .stage_queue import (
    cascade_clear_later_confirmations,
    has_triage_in_queue,
    inject_triage_stages,
    print_cascade_clear_feedback,
    purge_triage_stage,
)

__all__ = [
    "active_triage_issue_ids",
    "apply_completion",
    "cascade_clear_later_confirmations",
    "clear_active_triage_issue_tracking",
    "cluster_issue_ids",
    "count_log_activity_since",
    "ensure_active_triage_issue_ids",
    "find_cluster_for",
    "group_issues_into_observe_batches",
    "has_open_review_issues",
    "has_triage_in_queue",
    "inject_triage_stages",
    "live_active_triage_issue_ids",
    "manual_clusters_with_issues",
    "observe_dimension_breakdown",
    "open_review_ids_from_state",
    "plan_review_ids",
    "print_cascade_clear_feedback",
    "purge_triage_stage",
    "sync_undispositioned_triage_meta",
    "triage_coverage",
    "undispositioned_triage_issue_ids",
]
