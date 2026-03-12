"""Direct tests for lazy package-root command entrypoints."""

from __future__ import annotations

import argparse
import importlib

import pytest

COMMAND_PACKAGES = (
    (
        "desloppify.app.commands.autofix",
        "desloppify.app.commands.autofix.cmd",
        "cmd_autofix",
    ),
    (
        "desloppify.app.commands.backlog",
        "desloppify.app.commands.backlog.cmd",
        "cmd_backlog",
    ),
    (
        "desloppify.app.commands.move",
        "desloppify.app.commands.move.cmd",
        "cmd_move",
    ),
    (
        "desloppify.app.commands.next",
        "desloppify.app.commands.next.cmd",
        "cmd_next",
    ),
    (
        "desloppify.app.commands.scan",
        "desloppify.app.commands.scan.cmd",
        "cmd_scan",
    ),
    (
        "desloppify.app.commands.show",
        "desloppify.app.commands.show.cmd",
        "cmd_show",
    ),
)


@pytest.mark.parametrize(("package_name", "command_module_name", "entrypoint_name"), COMMAND_PACKAGES)
def test_package_root_entrypoints_delegate_to_command_modules(
    monkeypatch,
    package_name: str,
    command_module_name: str,
    entrypoint_name: str,
) -> None:
    package_mod = importlib.import_module(package_name)
    command_mod = importlib.import_module(command_module_name)
    args = argparse.Namespace(path=".")
    calls: list[argparse.Namespace] = []

    monkeypatch.setattr(command_mod, entrypoint_name, lambda value: calls.append(value))

    entrypoint = getattr(package_mod, entrypoint_name)

    assert entrypoint_name in package_mod.__all__
    assert callable(entrypoint)
    assert entrypoint.__module__ == package_name
    assert "stable package-root entrypoint" in (package_mod.__doc__ or "")

    entrypoint(args)

    assert calls == [args]
