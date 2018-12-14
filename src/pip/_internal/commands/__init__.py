"""
Package containing all pip commands
"""
from __future__ import absolute_import

from pip._internal.commands.check import CheckCommand
from pip._internal.commands.completion import CompletionCommand
from pip._internal.commands.configuration import ConfigurationCommand
from pip._internal.commands.download import DownloadCommand
from pip._internal.commands.freeze import FreezeCommand
from pip._internal.commands.hash import HashCommand
from pip._internal.commands.help import HelpCommand
from pip._internal.commands.install import InstallCommand
from pip._internal.commands.list import ListCommand
from pip._internal.commands.search import SearchCommand
from pip._internal.commands.show import ShowCommand
from pip._internal.commands.third_party import get_3rd_party_commands, ThirdPartyCommand
from pip._internal.commands.uninstall import UninstallCommand
from pip._internal.commands.wheel import WheelCommand
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.cli.base_command import Command

if MYPY_CHECK_RUNNING:
    from typing import List, Type, Union  # noqa: F401

commands_order = [
    InstallCommand,
    DownloadCommand,
    UninstallCommand,
    FreezeCommand,
    ListCommand,
    ShowCommand,
    CheckCommand,
    ConfigurationCommand,
    SearchCommand,
    WheelCommand,
    HashCommand,
    CompletionCommand,
    HelpCommand,
]  # type: List[Union[Type[Command], ThirdPartyCommand]]
commands_order += get_3rd_party_commands()
commands_dict = {c.name: c for c in commands_order}


def _get_sorted_commands(ordered):
    if ordered:
        cmditems = _sort_commands(commands_dict, commands_order)
    else:
        cmditems = commands_dict.items()

    return iter(cmditems)


def get_summaries(ordered=True):
    """Yields sorted (command name, command summary) tuples."""

    return (
        (name, cmd_cls.summary)
        for name, cmd_cls in _get_sorted_commands(ordered)
        if issubclass(cmd_cls, Command)
    )


def get_summaries_3rd_party(ordered=True):
    return [
        name
        for name, cmd_cls in _get_sorted_commands(ordered)
        if not issubclass(cmd_cls, Command)
    ]


def get_similar_commands(name):
    """Command name auto-correct."""
    from difflib import get_close_matches

    name = name.lower()

    close_commands = get_close_matches(name, commands_dict.keys())

    if close_commands:
        return close_commands[0]
    else:
        return False


def _sort_commands(cmddict, order):
    def keyfn(key):
        try:
            return order.index(key[1])
        except ValueError:
            # unordered items should come last
            return 0xFF

    return sorted(cmddict.items(), key=keyfn)
