"""
Package containing all pip commands
"""
from __future__ import absolute_import

from collections import OrderedDict

from pip._internal.commands.check import CheckCommand
from pip._internal.commands.completion import CompletionCommand
from pip._internal.commands.configuration import ConfigurationCommand
from pip._internal.commands.download import DownloadCommand
from pip._internal.commands.freeze import FreezeCommand
from pip._internal.commands.hash import HashCommand
from pip._internal.commands.help import HelpCommand
from pip._internal.commands.install import InstallCommand
from pip._internal.commands.list_ import ListCommand
from pip._internal.commands.search import SearchCommand
from pip._internal.commands.show import ShowCommand
from pip._internal.commands.plugins import get_plugin_commands, PluginCommand
from pip._internal.commands.uninstall import UninstallCommand
from pip._internal.commands.wheel import WheelCommand
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.cli.base_command import Command

if MYPY_CHECK_RUNNING:
    from typing import Dict, Type, Union  # noqa: F401

commands_dict = OrderedDict(
    (c.name, c)
    for c in [
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
    ]
)  # type:Dict[str, Union[Type[Command], PluginCommand]]

plugin_commands_dict = OrderedDict(
    (c.name, c) for c in get_plugin_commands()
)  # type:Dict[str, PluginCommand]


def get_summaries():
    return [(name, cmd_cls.summary) for name, cmd_cls in commands_dict.items()]


def get_summaries_for_plugins():
    return list(plugin_commands_dict.keys())


def get_similar_commands(name):
    """Command name auto-correct."""
    from difflib import get_close_matches

    name = name.lower()

    close_commands = get_close_matches(
        name, {**commands_dict.keys(), **plugin_commands_dict.keys()}
    )

    if close_commands:
        return close_commands[0]
    else:
        return False
