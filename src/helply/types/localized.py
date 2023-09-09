"""Localized variants of Helply app command types"""
from typing import Any, List, Optional

from disnake import Permissions

from .abc_ import AppCommandBase, ArgumentBase
from .checks import CommandChecks, Cooldown
from .enums import AppCommandType

__all__ = (
    "LocalizedArgument",
    "LocalizedAppCommand",
    "LocalizedSlashCommand",
    "LocalizedUserCommand",
    "LocalizedMessageCommand",
)


class LocalizedArgument(ArgumentBase):
    """Represents a slash command argument with localized attributes.

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
    """Represents an AppCommand with localized attributes.

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's localized name
    description: str
        Command's localized description
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
        The configured cooldown, if available
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.
    """

    __slots__ = ("_name",)

    def __init__(
        self,
        id: int,
        _name: str,
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
        super().__init__(
            id=id,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )

        self._name: str = _name

    @property
    def mention(self) -> str:
        """Return clickable mention if slash, else bolded name."""
        if self.type is AppCommandType.SLASH:
            return f"</{self._name}:{self.id}>"

        return f"**{self._name}**"

    def __eq__(self, other: Any) -> bool:
        """Return True if self == other, else False"""
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id or (
            self._name in (other.name, other._name)
            and self.type == other.type
            and self.category == other.category
            and self.nsfw == other.nsfw
            and self.default_member_permissions == other.default_member_permissions
            and self.cooldown == other.cooldown
        )


class LocalizedSlashCommand(LocalizedAppCommand):
    """Represents a slash command type AppCommand.

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's localized name
    description: str
        Command's localized description
    args: List[LocalizedArgument]
        Command's localized arguments.
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
        The configured cooldown, if available
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as selectable tag.
    """

    __slots__ = ("args",)

    def __init__(
        self,
        id: int,
        _name: str,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        args: List[LocalizedArgument],
        category: str,
        dm_permission: bool,
        nsfw: bool,
        cooldown: Optional[Cooldown],
        guild_id: Optional[int] = None,
        default_member_permissions: Optional[Permissions] = None,
    ) -> None:
        super().__init__(
            id=id,
            _name=_name,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )

        self.args: list[LocalizedArgument] = args


class LocalizedUserCommand(LocalizedAppCommand):
    """Represents a UserCommand with localized attributes.

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's localized name
    description: str
        Command's localized description
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
        The configured cooldown, if available
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command name, bolded.
    """

    def __init__(
        self,
        id: int,
        _name: str,
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
        super().__init__(
            id=id,
            _name=_name,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )


class LocalizedMessageCommand(LocalizedAppCommand):
    """Represents a MessageCommand with localized attributes.

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's localized name
    description: str
        Command's localized description
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
        The configured cooldown, if available
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command name, bolded.
    """

    def __init__(
        self,
        id: int,
        _name: str,
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
        super().__init__(
            id=id,
            _name=_name,
            name=name,
            description=description,
            checks=checks,
            type=type,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )
