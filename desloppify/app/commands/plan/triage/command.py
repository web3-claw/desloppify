"""Handler for `plan triage` command entrypoint."""

from __future__ import annotations

import argparse

from desloppify.app.commands.helpers.state import require_issue_inventory
from .review_coverage import triage_coverage
from .services import default_triage_services
from .workflow import run_triage_workflow

_triage_coverage = triage_coverage

def cmd_plan_triage(args: argparse.Namespace) -> None:
    """Run staged triage workflow: observe -> reflect -> organize -> enrich -> sense-check -> commit."""
    resolved_services = default_triage_services()
    run_triage_workflow(
        args,
        services=resolved_services,
        require_issue_inventory_fn=require_issue_inventory,
    )


__all__ = [
    "_triage_coverage",
    "cmd_plan_triage",
]
