# -*- coding: utf-8 -*-

"""Version information."""

import os
from subprocess import CalledProcessError, check_output  # noqa: S404
from typing import Optional

__all__ = [
    'VERSION',
    'get_version',
    'get_git_hash',
]

VERSION = '0.0.5-dev'


def get_git_hash() -> Optional[str]:
    """Get the git hash.

    :return:
        The git hash, equals 'UNHASHED' if encountered CalledProcessError, signifying that the
        code is not installed in development mode.
    """
    with open(os.devnull, 'w') as devnull:
        try:
            ret = check_output(  # noqa: S603,S607
                ['git', 'rev-parse', 'HEAD'],
                cwd=os.path.dirname(__file__),
                stderr=devnull,
            )
        except CalledProcessError:
            return
        else:
            return ret.strip().decode('utf-8')[:8]


def get_version(with_git_hash: bool = False) -> str:
    """Get the version string, including a git hash.

    :param with_git_hash:
        If set to True, the git hash will be appended to the version.
    :return: The version as well as the git hash, if the parameter with_git_hash was set to true.
    """
    return f'{VERSION}-{get_git_hash()}' if with_git_hash else VERSION


if __name__ == '__main__':
    print(get_version(with_git_hash=True))