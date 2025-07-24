from os import path as os_path
from sys import path as sys_path

sys_path.append(os_path.dirname(os_path.abspath(__file__)))

# pylint: disable=C0413
from checker import CheckIP, CheckDomain

__all__ = (
    "CheckIP",
    "CheckDomain",
)
