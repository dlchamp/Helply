"""Base classes for the types used within Helply."""

from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Optional

from disnake import Permissions

from .checks import CommandChecks, Cooldown
from .enums import AppCommandType

__all__ = (
    "ArgumentBase",
    "AppCommandBase",
)


class ArgumentBase(ABC):
    """Base class for Argument.

    Attributes
    ----------
    name: str
        Argument's name
    description: str
        Argument's description
    required: bool
        Whether or not the argument is required
    """

    __slots__ = (
        "name",
        "description",
        "required",
    )

    def __init__(self, name: str, description: str, required: bool) -> None:
        self.name = name
        self.description = description
        self.required = required


class AppCommandBase(ABC):
    """Base class for AppCommand and LocalizedAppCommand.

    AppCommands are classes that include various attributes from both
    `.ApplicationCommand` and `.InvokableApplicationCommand`

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's name
    description: str
        Command's description
    checks : CommandChecks
        The command's permission and role requirements.
    type: AppCommandType
        Type of command
    category: str
        Name of cog or category the command belongs to
    dm_permission : bool
        Whether the command is available in DMs or not.
    nsfw : bool
        Whether the command is NSFW (Not Safe For Work).
    cooldown: Optional[Cooldown]
        The configured cooldown, if available (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Permissions, optional
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.
    """

    __slots__ = (
        "id",
        "name",
        "description",
        "checks",
        "type",
        "category",
        "dm_permission",
        "nsfw",
        "cooldown",
        "guild_id",
        "default_member_permissions",
    )

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        category: str,
        dm_permission: bool,
        nsfw: bool,
        cooldown: Optional[Cooldown],
        guild_id: Optional[int] = None,
        default_member_permissions: Optional[Permissions] = None,
    ) -> None:
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.checks: CommandChecks = checks
        self.type: AppCommandType = type
        self.category: str = category
        self.dm_permission: bool = dm_permission
        self.nsfw: bool = nsfw
        self.cooldown: Optional[Cooldown] = cooldown
        self.guild_id: Optional[int] = guild_id
        self.default_member_permissions: Optional[Permissions] = default_member_permissions

    @abstractproperty
    def mention(self) -> str:
        """Return clickable mention if slash, else bolded name."""
        ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        """Return True if self == other, else False"""
        ...
