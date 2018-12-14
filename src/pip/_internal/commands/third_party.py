from __future__ import absolute_import

import glob
import json
import logging
import os
import sys
from typing import TypeVar, List

logger = logging.getLogger(__name__)

THIRD_PARTY_CMD_PREFIX = "pip-"


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
        name = os.path.basename(script).split(".")[0][len(THIRD_PARTY_CMD_PREFIX):]
        summary = "xyz"

        # for compat with `Command`
        def __init__(self, *args, **kwargs):
            pass

        @staticmethod
        def main(args):
            os.execv(
                script,
                [
                    sys.argv[0],
                    json.dumps(
                        {
                            "sys.executable": sys.executable,
                            "args": args,
                            "sys.argv": sys.argv,
                        }
                    ),
                ],
            )

    return ThirdPartyCommand


def get_3rd_party_commands() -> List[ThirdPartyCommand]:
    return [make_3rd_party_command(i) for i in search_3rd_party_scripts()]
