"""Nextcord specific application command handler."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Optional, Sequence, Union

from nextcord import (
    BaseApplicationCommand,
    MessageApplicationCommand,
    SlashApplicationCommand,
    SlashApplicationSubcommand,
    UserApplicationCommand,
)
from nextcord.ext import commands

from .. import errors
from ..types import (
    AppCommand,
    AppCommandType,
    Argument,
    CommandChecks,
    Cooldown,
    MessageCommand,
    SlashCommand,
    UserCommand,
)
from ..utils import utils

BotT = Union[commands.Bot, commands.AutoShardedBot]
CooldownT = Union[commands.CooldownMapping, commands.DynamicCooldownMapping]
ApplicationCommands = Union[
    SlashApplicationCommand,
    UserApplicationCommand,
    MessageApplicationCommand,
    SlashApplicationSubcommand,
]


class NextcordCommandHandler:
    """Command handler that interfaces with the Nextcord library."""

    if TYPE_CHECKING:
        from ..__wrappers import Bot

    def __init__(self, bot: BotT, commands_to_ignore: Union[Sequence[str], None] = None) -> None:
        self.bot = bot

        if commands_to_ignore is not None:
            self.commands_to_ignore: set[str] = set(commands_to_ignore)
        else:
            self.commands_to_ignore = set()

        self._app_commands: List[AppCommand] = []

    def _parse_arguments(
        self, command: Union[SlashApplicationCommand, SlashApplicationSubcommand]
    ) -> List[Argument]:
        """Parse and return the `SlashCommand` or `SubCommand` arguments.

        Parameters
        ----------
        command : Union[SlashApplicationCommand, SlashApplicationSubcommand]
            The slash command or a slash command's sub_command.

        Returns
        -------
        List[Argument]
            A sequence of the command or sub_command's arguments.
        """
        args: List[Argument] = []

        for name, option in command.options.items():
            args.append(
                Argument(
                    name=name,
                    description=option.description,
                    required=option.required or False,
                    name_localizations=option.name_localizations,
                    description_localizations=option.description_localizations,
                )
            )

        return args

    def _get_command_desc(
        self,
        command: Union[SlashApplicationCommand, SlashApplicationSubcommand],
    ) -> str:
        """Get the description for a command.

        Parameters
        ----------
        command: Union[SlashApplicationCommand, SlashApplicationSubcommand]
            The slash command or sub command.

        Returns
        -------
        str
            The description of the command.
        """
        return getattr(command, "description", "-")

    def _parse_cooldowns(
        self,
        command: ApplicationCommands,
    ) -> Optional[Cooldown]:
        """Parse the configured cooldown for an ApplicationCommand.

        Parameters
        ----------
        command: Union[SlashApplicationCommand, SlashApplicationSubcommand]
            The slash command or sub command.

        Returns
        -------
        Optional[Cooldown]
            Return the Cooldown if configured, else None
        """
        cooldown_map: Union[CooldownT, None] = getattr(command, "__commands_cooldown__", None)
        cooldown: Union[commands.Cooldown, None] = getattr(cooldown_map, "_cooldown", None)

        if cooldown_map is None or cooldown is None:
            return None

        rate = cooldown.rate
        per = cooldown.per
        type_ = str(cooldown_map._type)  # type: ignore[reportPrivateUsage]
        type_ = type_.replace("BucketType.", "").replace("default", "global").title()

        return Cooldown(rate=rate, per=per, type=type_)

    def _get_sub_commands(
        self,
        command_id: int,
        command: SlashApplicationCommand,
        category: str,
    ) -> List[SlashCommand]:
        """Get and return the `SlashCommand`'s registered `SubCommands` if any.

        Parameters
        ----------
        command_id: int
            ID of the slash command.
        command : SlashApplicationCommand
            The registered slash command or the command's SubCommand.
        category : str
            The category of the commands.


        Returns
        -------
        List[SlashCommand]
            A list of sub-commands, if any.
        """
        sub_commands: List[SlashCommand] = []

        for child in command.children.values():
            if not child.children:
                checks = self._parse_checks(child)
                args = self._parse_arguments(child)
                cooldown = self._parse_cooldowns(child)
                description = self._get_command_desc(child)
                sub_commands.append(
                    SlashCommand(
                        id=command_id,
                        name=child.name,  # type: ignore[reportArgumentType]
                        name_=child.name,  # type: ignore[reportArgumentType]
                        description=description,
                        checks=checks,
                        type=AppCommandType.SLASH,
                        dm_permission=command.dm_permission or False,
                        nsfw=command.nsfw,
                        name_localizations=child.name_localizations,
                        category=category,
                        description_localizations=child.description_localizations,
                        args=args,
                        cooldown=cooldown,
                        guild_ids=command.guild_ids,
                        default_member_permissions=command.default_member_permissions,
                    )
                )
                continue

            for grandchild in child.children.values():
                checks = self._parse_checks(grandchild)
                args = self._parse_arguments(grandchild)
                cooldown = self._parse_cooldowns(grandchild)
                description = self._get_command_desc(grandchild)
                sub_commands.append(
                    SlashCommand(
                        id=command_id,
                        name=grandchild.name,  # type: ignore[reportArgumentType]
                        name_=grandchild.name,  # type: ignore[reportArgumentType]
                        description=description,
                        checks=checks,
                        type=AppCommandType.SLASH,
                        dm_permission=command.dm_permission or False,
                        nsfw=command.nsfw,
                        name_localizations=grandchild.name_localizations,
                        category=category,
                        description_localizations=grandchild.description_localizations,
                        args=args,
                        cooldown=cooldown,
                        guild_ids=command.guild_ids,
                        default_member_permissions=command.default_member_permissions,
                    )
                )

        return sub_commands

    def _extract_closure_values(self, func: Callable[..., Any]) -> List[Any]:
        """Recursively extract closure values from nested functions."""
        closure_values: List[Any] = []
        current_func: Callable[..., Any] = func

        while hasattr(current_func, "__closure__") and current_func.__closure__:
            closure = current_func.__closure__
            for cell in closure:
                cell_content = cell.cell_contents
                closure_values.append(cell_content)
                if callable(cell_content):
                    # If it's another function, dive deeper
                    current_func = cell_content
                    break
            else:
                # If no function was found in the closure, exit the loop
                break

        return closure_values

    def _parse_checks(
        self,
        command: ApplicationCommands,
    ) -> CommandChecks:
        """Parse the role and permissions checks."""
        permissions: List[str] = []
        roles: List[Union[str, int]] = []

        # Access the list of checks associated with the command
        checks: List[Any] = command.checks

        for check in checks:
            # Get the name of the check to determine its type
            name: str = check.__qualname__.split(".")[0]

            # Skip bot-specific checks or checks without a closure
            if "bot" in name or not check.__closure__:
                continue

            # Extract closure values
            closure_values: List[Any] = self._extract_closure_values(check)
            closure_content: Union[dict[str, bool], str, int]

            for closure_content in closure_values:
                if isinstance(closure_content, (int, str)) and "role" in name:
                    roles.append(closure_content)
                elif isinstance(closure_content, dict):
                    permissions.extend(
                        [
                            perm.replace("_", " ").title()
                            for perm, value in closure_content.items()
                            if value
                        ]
                    )

        return CommandChecks(permissions, roles)

    def _get_command_category(self, command: BaseApplicationCommand) -> str:
        """Get the command's category, plugin, or cog name, if available

        Nextcord does not support cog or category names for application commands.
        This will always return "".

        Parameters
        ----------
        command: BaseApplicationCommand

        Returns
        -------
        Optional[str]
            Name of the category, plugin, or cog the command belongs to, or "".

        """
        _ = command  # unused variables, yeah yeah.  I might end up needing this.
        return ""

    def _handle_slash_command(
        self, id_: int, command: SlashApplicationCommand
    ) -> List[SlashCommand]:
        """Handle creation of `SlashCommand` from 'nextcord.SlashApplicationCommand`.

        Parameters
        ----------
        id_: int
            ID of the slash command.
        command : nextcord.SlashApplicationCommand
            Slash Command provided by nextcord

        Return
        ------
        List[SlashCommand]
        """
        checks = self._parse_checks(command)
        cooldown = self._parse_cooldowns(command)
        args = self._parse_arguments(command)
        category = self._get_command_category(command)
        description = self._get_command_desc(command)
        sub_commands = self._get_sub_commands(id_, command, category=category)

        if sub_commands:
            return sub_commands

        return [
            SlashCommand(
                id=id_,
                name=command.name,  # type: ignore[reportArgumentType]
                name_=command.name,  # type: ignore[reportArgumentType]
                description=description,
                checks=checks,
                type=AppCommandType.SLASH,
                dm_permission=command.dm_permission or False,
                nsfw=command.nsfw,
                name_localizations=command.name_localizations,
                description_localizations=command.description_localizations,
                category=category,
                args=args,
                cooldown=cooldown,
                guild_ids=command.guild_ids,
                default_member_permissions=command.default_member_permissions,
            )
        ]

    def _handle_message_command(
        self, id_: int, command: MessageApplicationCommand
    ) -> MessageCommand:
        """Handle creation of `MessageCommand` from 'nextcord.MessageApplicationCommand`.

        Parameters
        ----------
        id_: int
            ID of the command.
        command : nextcord.MessageApplicationCommand
            Message Command provided by nextcord

        Return
        ------
        List[MessageCommand]
        """
        checks = self._parse_checks(command)
        cooldown = self._parse_cooldowns(command)
        desc = utils._parse_docstring(command.callback)
        category = self._get_command_category(command)

        return MessageCommand(
            id=id_,
            name=command.name or "",
            name_=command.name or "",
            description=desc,
            name_localizations=command.name_localizations,
            checks=checks,
            type=AppCommandType.MESSAGE,
            dm_permission=command.dm_permission or False,
            nsfw=command.nsfw,
            cooldown=cooldown,
            guild_ids=command.guild_ids,
            default_member_permissions=command.default_member_permissions,
            category=category,
        )

    def _handle_user_command(self, id_: int, command: UserApplicationCommand) -> UserCommand:
        """Handle creation of `UserCommand` from `nextcord.MessageApplicationCommand`.

        Parameters
        ----------
        command : nextcord.MessageApplicationCommand
            The MessageApplicationCommand provided by Discord's API.

        Return
        ------
        UserCommand
        """
        checks = self._parse_checks(command)
        cooldown = self._parse_cooldowns(command)
        desc = utils._parse_docstring(command.callback)
        category = self._get_command_category(command)

        return UserCommand(
            id=id_,
            name=command.name,
            name_=command.name,
            description=desc,
            name_localizations=command.name_localizations,
            checks=checks,
            type=AppCommandType.USER,
            dm_permission=command.dm_permission or False,
            nsfw=command.nsfw,
            cooldown=cooldown,
            guild_ids=command.guild_ids,
            default_member_permissions=command.default_member_permissions,
            category=category,
        )

    def _walk_app_commands(self) -> List[AppCommand]:
        """Retrieve all global and guild-specific application commands."""
        if self._app_commands:
            return self._app_commands

        for id_, command in self.bot._connection._application_command_ids.items():
            if isinstance(command, SlashApplicationCommand):
                commands = self._handle_slash_command(id_, command)
            elif isinstance(command, MessageApplicationCommand):
                commands = [self._handle_message_command(id_, command)]
            elif isinstance(command, UserApplicationCommand):
                commands = [self._handle_user_command(id_, command)]
            else:
                raise errors.UnsupportedCommandType(command)

            self._app_commands.extend(commands)

        return self._app_commands
