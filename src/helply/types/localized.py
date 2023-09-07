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
    """Represents a slash command argument with localized attributes"""

    def __init__(self, name: str, description: str, required: bool) -> None:
        super().__init__(name=name, description=description, required=required)


class LocalizedAppCommand(AppCommandBase):
    """Represents an AppCommand with localized attributes"""

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
