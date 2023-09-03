import enum

from .commands import MessageCommand, SlashCommand, UserCommand

__all__ = ("AppCommandType",)


class AppCommandType(enum.Enum):
    """Enum for AppCommandType

    Attributes
    ----------
    slash: SlashCommand
    message: MessageCommand
    user UserCommand
    """

    slash = SlashCommand
    message = MessageCommand
    user = UserCommand
