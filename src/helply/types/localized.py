from typing import List, Optional

from disnake import Permissions

from .abc_ import AppCommandBase, ArgumentBase
from .checks import CommandChecks
from .enums import AppCommandType

__all__ = (
    "LocalizedArgument",
    "LocalizedAppCommand",
    "LocalizedSlashCommand",
    "LocalizedUserCommand",
    "LocalizedMessageCommand",
)


class LocalizedArgument(ArgumentBase):
    """Represents a slash command argument with localized attributes

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
        super().__init__(name=name, description=description, required=required)


class LocalizedAppCommand(AppCommandBase):
    """Represents an AppCommand with localized attributes

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's name
    description: str
        Command's description
    name_localizations: disnake.LocalizationValue
        Contains localizations for the command's name. (*New in version 0.3.0*)
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
    guild_id : Optional[int]
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
        super().__init__(
            id=id,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )


class LocalizedSlashCommand(LocalizedAppCommand):
    """Represents a slash command type AppCommand

    Attributes
    ----------
    args: List[Argument]
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        args: List[LocalizedArgument],
        category: str,
        dm_permission: bool,
        nsfw: bool,
        guild_id: Optional[int] = None,
        default_member_permissions: Optional[Permissions] = None,
    ) -> None:
        super().__init__(
            id=id,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )

        self.args: List[LocalizedArgument] = args


class LocalizedUserCommand(LocalizedAppCommand):
    """Represents a user command type AppCommand"""

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
        super().__init__(
            id=id,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )


class LocalizedMessageCommand(LocalizedAppCommand):
    """Represents a message command type AppCommand"""

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
        super().__init__(
            id=id,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )
