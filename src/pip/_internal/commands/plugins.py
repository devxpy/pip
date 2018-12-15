from __future__ import absolute_import

import glob
import json
import logging
import os
import sys
from functools import lru_cache
from typing import TypeVar, List

logger = logging.getLogger(__name__)

PluginCommand = TypeVar("PluginCommand")

PIP_PLUGIN_SCRIPT_PREFIX = "pip-plugin-"


def search_plugin_scripts() -> List[str]:
    glob_pattern = PIP_PLUGIN_SCRIPT_PREFIX + "*"
    user_path_dirs = set(os.environ["PATH"].split(os.pathsep))
    return [
        maybe_exec
        for dirpath in user_path_dirs
        for maybe_exec in glob.glob(os.path.join(dirpath, glob_pattern))
        if os.access(maybe_exec, os.X_OK)
    ]


def make_plugin_command(script: str) -> PluginCommand:
    class PluginCommand:
        """
        Represents a third-party pip command.
        """

        name = os.path.basename(script).split(".")[0][len(PIP_PLUGIN_SCRIPT_PREFIX):]
        summary = "---"

        # for compat with `Command`
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def main(args):
            os.execv(
                script,
                [
                    script,
                    json.dumps(
                        {
                            "sys.executable": sys.executable,
                            "sys.argv": sys.argv,
                            "os.environ": dict(os.environ),
                            "args": args,
                        }
                    ),
                ],
            )

    return PluginCommand


@lru_cache(maxsize=None)  # hint: it is expensive to search for plugins
def get_plugin_commands() -> List[PluginCommand]:
    return [make_plugin_command(i) for i in search_plugin_scripts()]
