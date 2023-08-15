"""src/user/constants.py"""

from enum import Enum


class Role(Enum):
    """Class used for Users role definition."""

    USER = "USER"
    MANAGER = "MANAGER"
    ADMIN = "ADMIN"
