from __future__ import absolute_import

import glob
import json
import logging
import os
import subprocess
import sys
from typing import Generator, TypeVar, List

import pkg_resources

logger = logging.getLogger(__name__)

THIRD_PARTY_CMD_PREFIX = "pip-"


def get_all_console_scripts(package_name):
    entrypoints = (
        ep
        for ep in pkg_resources.iter_entry_points("console_scripts")
        if ep.module_name.startswith(package_name)
    )
    return entrypoints


def search_3rd_party_scripts() -> List[str]:
    glob_pattern = THIRD_PARTY_CMD_PREFIX + "*"
    user_path_dirs = set(os.environ["PATH"].split(os.pathsep))
    return [
        maybe_exec
        for dirpath in user_path_dirs
        for maybe_exec in glob.glob(os.path.join(dirpath, glob_pattern))
        if os.access(maybe_exec, os.X_OK)
    ]


ThirdPartyCommand = TypeVar("ThirdPartyCommand")


def make_3rd_party_command(script: str) -> ThirdPartyCommand:
    class ThirdPartyCommand:
        """
        Represents a third-party pip command.
        """

        name = os.path.basename(script).split(".")[0][len(THIRD_PARTY_CMD_PREFIX) :]
        summary = "xyz"

        # for compat with Command.
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def main(args):
            pip_help = dict(json.loads(subprocess.check_output([script, "--pip-help"])))

            modenv = os.environ.copy()
            modenv["PYTHONPATH"] = os.pathsep.join(
                (modenv.get("PYTHONPATH", ""), pip_help["pkgpath"])
            )

            subprocess.run([sys.executable, pip_help["__file__"]] + args, env=modenv)

    return ThirdPartyCommand


def get_3rd_party_commands() -> List[ThirdPartyCommand]:
    return [make_3rd_party_command(i) for i in search_3rd_party_scripts()]
