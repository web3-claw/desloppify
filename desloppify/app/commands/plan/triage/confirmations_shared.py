"""Shared helpers for triage stage confirmation flows."""

from __future__ import annotations

from collections.abc import Callable

from desloppify.base.output.terminal import colorize
from desloppify.state import utc_now

from .helpers import purge_triage_stage

_STAGE_LABELS = {
    "observe": "Observe",
    "reflect": "Reflect",
    "organize": "Organize",
    "enrich": "Enrich",
    "sense-check": "Sense-check",
}


def ensure_stage_is_confirmable(stages: dict, *, stage: str) -> bool:
    """Validate stage presence/confirmation status before confirm flow runs."""
    if stage not in stages:
        print(colorize(f"  Cannot confirm: {stage} stage not recorded.", "red"))
        print(colorize(f'  Run: desloppify plan triage --stage {stage} --report "..."', "dim"))
        return False
    if stages[stage].get("confirmed_at"):
        label = _STAGE_LABELS.get(stage, stage.title())
        print(colorize(f"  {label} stage already confirmed.", "green"))
        return False
    return True


def finalize_stage_confirmation(
    *,
    plan: dict,
    stages: dict,
    stage: str,
    attestation: str | None,
    min_attestation_len: int,
    command_hint: str,
    validation_stage: str,
    validate_attestation_fn: Callable[..., str | None],
    validation_kwargs: dict[str, object] | None,
    log_action: str,
    log_detail: dict[str, object] | None,
    services,
    not_satisfied_hint: str | None = None,
) -> bool:
    """Apply shared attestation validation + state mutation + log/save flow."""
    attestation_text = (attestation or "").strip()
    if len(attestation_text) < min_attestation_len:
        if attestation_text:
            print(
                colorize(
                    f"\n  Attestation too short ({len(attestation_text)} chars, min {min_attestation_len}).",
                    "red",
                )
            )
        print(colorize("\n  If satisfied, confirm:", "dim"))
        print(colorize(f"    {command_hint}", "dim"))
        if not_satisfied_hint:
            print(colorize(f"  {not_satisfied_hint}", "dim"))
        return False

    err = validate_attestation_fn(
        attestation_text,
        validation_stage,
        **(validation_kwargs or {}),
    )
    if err:
        print(colorize(f"\n  {err}", "red"))
        return False

    stages[stage]["confirmed_at"] = utc_now()
    stages[stage]["confirmed_text"] = attestation_text
    purge_triage_stage(plan, stage)

    detail = {"attestation": attestation_text}
    if log_detail:
        detail.update(log_detail)
    services.append_log_entry(
        plan,
        log_action,
        actor="user",
        detail=detail,
    )
    services.save_plan(plan)
    label = _STAGE_LABELS.get(stage, stage.title())
    print(colorize(f'  ✓ {label} confirmed: "{attestation_text}"', "green"))
    return True


__all__ = ["ensure_stage_is_confirmable", "finalize_stage_confirmation"]
