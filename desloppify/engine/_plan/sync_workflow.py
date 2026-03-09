"""Workflow gate sync — inject workflow action items when preconditions are met."""

from __future__ import annotations

from desloppify.engine._plan import stale_policy as stale_policy_mod
from desloppify.engine._plan._sync_context import has_objective_backlog
from desloppify.engine._plan.constants import (
    SUBJECTIVE_PREFIX,
    TRIAGE_IDS,
    WORKFLOW_COMMUNICATE_SCORE_ID,
    WORKFLOW_CREATE_PLAN_ID,
    WORKFLOW_IMPORT_SCORES_ID,
    WORKFLOW_SCORE_CHECKPOINT_ID,
    QueueSyncResult,
)
from desloppify.engine._plan.schema import PlanModel, ensure_plan_defaults
from desloppify.engine._plan.subjective_policy import SubjectiveVisibility
from desloppify.engine._state.schema import StateModel


def _no_unscored(
    state: StateModel,
    policy: SubjectiveVisibility | None,
) -> bool:
    """Return True when no unscored (placeholder) subjective dimensions remain."""
    if policy is not None:
        return not policy.unscored_ids
    return not stale_policy_mod.current_unscored_ids(
        state, subjective_prefix=SUBJECTIVE_PREFIX,
    )


def _inject(plan: PlanModel, item_id: str) -> QueueSyncResult:
    """Append *item_id* and clear stale skip entries for that workflow item."""
    order = plan["queue_order"]
    order.append(item_id)
    skipped = plan.get("skipped", {})
    if isinstance(skipped, dict):
        skipped.pop(item_id, None)
    return QueueSyncResult(injected=[item_id])


_EMPTY = QueueSyncResult


def sync_score_checkpoint_needed(
    plan: PlanModel,
    state: StateModel,
    *,
    policy: SubjectiveVisibility | None = None,
) -> QueueSyncResult:
    """Inject ``workflow::score-checkpoint`` when all initial reviews complete.

    Injects when:
    - No unscored (placeholder) subjective dimensions remain
    - ``workflow::score-checkpoint`` is not already in the queue

    Appended to back of queue.  Never reorders existing items.
    """
    ensure_plan_defaults(plan)
    order: list[str] = plan["queue_order"]

    if WORKFLOW_SCORE_CHECKPOINT_ID in order:
        return _EMPTY()
    if not _no_unscored(state, policy):
        return _EMPTY()
    return _inject(plan, WORKFLOW_SCORE_CHECKPOINT_ID)


def sync_create_plan_needed(
    plan: PlanModel,
    state: StateModel,
    *,
    policy: SubjectiveVisibility | None = None,
) -> QueueSyncResult:
    """Inject ``workflow::create-plan`` when reviews complete + objective backlog exists.

    Only injects when:
    - No unscored (placeholder) subjective dimensions remain
    - At least one objective issue exists
    - ``workflow::create-plan`` is not already in the queue
    - No triage stages are pending

    Appended to back of queue.  Never reorders existing items.
    """
    ensure_plan_defaults(plan)
    order: list[str] = plan["queue_order"]

    if WORKFLOW_CREATE_PLAN_ID in order:
        return _EMPTY()
    if any(sid in order for sid in TRIAGE_IDS):
        return _EMPTY()
    if not _no_unscored(state, policy):
        return _EMPTY()

    if not has_objective_backlog(state, policy):
        return _EMPTY()

    return _inject(plan, WORKFLOW_CREATE_PLAN_ID)


def sync_import_scores_needed(
    plan: PlanModel,
    state: StateModel,
    *,
    assessment_mode: str | None = None,
) -> QueueSyncResult:
    """Inject ``workflow::import-scores`` after issues-only import.

    Only injects when:
    - Assessment mode was ``issues_only`` (scores were skipped)
    - ``workflow::import-scores`` is not already in the queue

    Appended to back of queue.  Never reorders existing items.
    """
    ensure_plan_defaults(plan)
    order: list[str] = plan["queue_order"]

    if WORKFLOW_IMPORT_SCORES_ID in order:
        return _EMPTY()
    if assessment_mode != "issues_only":
        return _EMPTY()
    return _inject(plan, WORKFLOW_IMPORT_SCORES_ID)


def sync_communicate_score_needed(
    plan: PlanModel,
    state: StateModel,
    *,
    policy: SubjectiveVisibility | None = None,
    scores_just_imported: bool = False,
) -> QueueSyncResult:
    """Inject ``workflow::communicate-score`` when scores should be shown.

    Injects when either:
    - All initial subjective reviews are complete (no unscored dimensions), OR
    - Scores were just imported (trusted/attested/override)

    And ``workflow::communicate-score`` is not already in the queue.
    Appended to back of queue.  Never reorders existing items.
    """
    ensure_plan_defaults(plan)
    order: list[str] = plan["queue_order"]

    if WORKFLOW_COMMUNICATE_SCORE_ID in order or WORKFLOW_SCORE_CHECKPOINT_ID in order:
        return _EMPTY()
    if not scores_just_imported and not _no_unscored(state, policy):
        return _EMPTY()
    return _inject(plan, WORKFLOW_COMMUNICATE_SCORE_ID)


__all__ = [
    "sync_communicate_score_needed",
    "sync_create_plan_needed",
    "sync_import_scores_needed",
    "sync_score_checkpoint_needed",
]
