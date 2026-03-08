"""Direct coverage tests for epic triage parsing helpers."""

from __future__ import annotations

import desloppify.engine._plan.epic_triage_parsing as parsing_mod


def test_extract_issue_citations_matches_full_ids_and_suffixes() -> None:
    valid_ids = {
        "review::abcdef12",
        "concerns::1234abcd",
        "review::feedface",
    }
    text = (
        "Keep review::abcdef12. Also reconsider 1234abcd and feedface "
        "while ignoring deadbeef."
    )

    cited = parsing_mod.extract_issue_citations(text, valid_ids)

    assert cited == {
        "review::abcdef12",
        "concerns::1234abcd",
        "review::feedface",
    }


def test_extract_issue_citations_ignores_unknown_matches() -> None:
    valid_ids = {"review::abcdef12"}

    cited = parsing_mod.extract_issue_citations(
        "noise review::badc0de0 and 00112233",
        valid_ids,
    )

    assert cited == set()


def test_parse_triage_result_filters_ids_and_normalizes_direction() -> None:
    valid_ids = {"review::abcdef12", "review::1234abcd"}
    raw = {
        "strategy_summary": "focus on root cause",
        "epics": [
            {
                "name": "cleanup",
                "thesis": "simplify orchestration",
                "direction": "not-a-direction",
                "root_cause": "mixed responsibilities",
                "issue_ids": ["review::abcdef12", "review::unknown"],
                "dismissed": ["review::1234abcd", "review::other"],
                "agent_safe": 1,
                "dependency_order": "3",
                "action_steps": ["step 1", 2, "step 3"],
                "status": "pending",
            }
        ],
        "dismissed_issues": [
            {"issue_id": "review::abcdef12", "reason": "duplicate"},
            {"issue_id": "review::unknown", "reason": "skip"},
        ],
        "contradiction_notes": [
            {"kept": "review::abcdef12", "dismissed": "review::1234abcd", "reason": "same fix"}
        ],
        "priority_rationale": "unblock dependent work",
    }

    result = parsing_mod.parse_triage_result(raw, valid_ids)

    assert result.strategy_summary == "focus on root cause"
    assert result.priority_rationale == "unblock dependent work"
    assert len(result.epics) == 1

    epic = result.epics[0]
    assert epic["name"] == "cleanup"
    assert epic["direction"] == "simplify"
    assert epic["issue_ids"] == ["review::abcdef12"]
    assert epic["dismissed"] == ["review::1234abcd"]
    assert epic["agent_safe"] is True
    assert epic["dependency_order"] == 3
    assert epic["action_steps"] == ["step 1", "step 3"]

    assert [d.issue_id for d in result.dismissed_issues] == ["review::abcdef12"]
    assert len(result.contradiction_notes) == 1
    assert result.contradiction_notes[0].kept == "review::abcdef12"


def test_parse_triage_result_drops_invalid_epics_and_non_dict_items() -> None:
    raw = {
        "epics": [None, "bad", {"name": " "}],
        "dismissed_issues": [None, {"issue_id": "review::x", "reason": "n/a"}],
        "contradiction_notes": ["bad", {"kept": 1, "dismissed": 2, "reason": 3}],
    }

    result = parsing_mod.parse_triage_result(raw, valid_ids={"review::y"})

    assert result.epics == []
    assert result.dismissed_issues == []
    assert len(result.contradiction_notes) == 1
    note = result.contradiction_notes[0]
    assert note.kept == "1"
    assert note.dismissed == "2"
    assert note.reason == "3"
