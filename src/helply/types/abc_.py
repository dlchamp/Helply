from abc import ABC
from typing import Optional

from disnake import Permissions

from .checks import CommandChecks
from .enums import AppCommandType

__all__ = (
    "ArgumentBase",
    "AppCommandBase",
)


class ArgumentBase(ABC):
    """Base class for slash command arguments

    Attributes
    ----------
    name: str
        Argument's non-localized name
    description: str
        Argument's non-localized description
    required: bool
        Whether or not the argument is required
    """

    def __init__(self, name: str, description: str, required: bool) -> None:
        self.name = name
        self.description = description
        self.required = required


class AppCommandBase(ABC):
    """Base class for all AppCommand and LocalizedAppCommand

    AppCommands are classes that include various attributes from both
    `.ApplicationCommand` and `.InvokableApplicationCommand`

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's non-localized name
    description: str
        Command's non-localized description
    name_localizations: disnake.LocalizationValue
        Contains localizations for the command's name. (*New in version 0.3.0*)
    description_localizations: Optional[disnake.LocalizationValue]
        Contains localizations for the command's description. (*New in version 0.3.0*)
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
    guild_id : int, optional
        The ID of the guild where the command is available.
    default_member_permissions : Permissions, optional
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else returns bolded name.
    """

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
        guild_id: Optional[int] = None,
        default_member_permissions: Optional[Permissions] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.checks = checks
        self.type = type
        self.category = category
        self.dm_permission = dm_permission
        self.nsfw = nsfw
        self.guild_id = guild_id
        self.default_member_permissions = default_member_permissions

    @property
    def mention(self) -> str:
        if self.type is AppCommandType.slash:
            return f"</{self.name}:{self.id}>"
        return f"**{self.name}**"