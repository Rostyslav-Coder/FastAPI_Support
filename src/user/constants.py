"""src/user/constants.py"""

from enum import IntEnum


class Role(IntEnum):
    """Class used for Users role definition."""

    USER = 1
    MANAGER = 2
    ADMIN = 3
