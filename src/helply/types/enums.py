"""Helply AppCommand types"""
import enum

__all__ = ("AppCommandType",)


class AppCommandType(str, enum.Enum):
    """Represents a command type.

    Attributes
    ----------
    SLASH
        "slash"
    MESSAGE
        "message"
    USER
        "user"

    """

    SLASH = "slash"
    MESSAGE = "message"
    USER = "user"
