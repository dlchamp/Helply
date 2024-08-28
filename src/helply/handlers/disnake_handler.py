"""Disnake specific application command handler."""
from typing import List, Optional, Sequence, Union

import disnake
import disnake.app_commands
from disnake.ext import commands

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

Bot = Union[
    commands.Bot,
    commands.InteractionBot,
    commands.AutoShardedBot,
    commands.AutoShardedInteractionBot,
]

APIApplicationCommand = Union[
    disnake.APIMessageCommand, disnake.APISlashCommand, disnake.APIUserCommand
]


class DisnakeCommandHandler:
    """Command handler that interfaces with the disnake library."""

    def __init__(self, bot: Bot, commands_to_ignore: Union[Sequence[str], None] = None) -> None:
        self.bot = bot

        if commands_to_ignore is not None:
            self.commands_to_ignore: set[str] = set(commands_to_ignore)
        else:
            self.commands_to_ignore = set()

        self._app_commands: List[AppCommand] = []

    def _get_command_args(
        self, command: Union[disnake.APISlashCommand, disnake.Option]
    ) -> List[Argument]:
        """Parse the slash command's arguments."""
        args: List[Argument] = []
        for option in command.options:
            if option.type in (
                disnake.OptionType.sub_command,
                disnake.OptionType.sub_command_group,
            ):
                continue

            args.append(
                Argument(
                    name=option.name,
                    name_localizations=option.name_localizations,
                    description=option.description,
                    description_localizations=option.description_localizations,
                    required=option.required,
                )
            )

        return args

    def _get_command_desc(
        self,
        command: commands.InvokableApplicationCommand,
    ) -> str:
        """Get the app command's description."""
        extras = command.extras.get("help")
        description = getattr(command, "description", "-")

        return extras or description

    def _parse_cooldowns(
        self,
        command: Union[commands.InvokableApplicationCommand, commands.SubCommand],
    ) -> Optional[Cooldown]:
        """Parse the app command's cooldowns."""
        cooldown = command._buckets._cooldown  # type: ignore
        if cooldown is None:
            return None

        rate = cooldown.rate
        per = cooldown.per
        type_ = str(command._buckets._type)  # type: ignore

        type_ = type_.replace("BucketType.", "").replace("default", "global").title()

        return Cooldown(rate=rate, per=per, type=type_)

    def _get_sub_commands(
        self,
        command: Union[disnake.APISlashCommand, disnake.Option],
        checks: CommandChecks,
        category: str,
        parent_command: Optional[disnake.APISlashCommand] = None,
    ) -> List[SlashCommand]:
        """Recursively get the sub commands of the slash command and any sub command groups."""
        sub_commands: List[SlashCommand] = []

        # ensure we always have access to the original parent command.
        if parent_command is None and isinstance(command, disnake.APISlashCommand):
            original_command = command
        elif parent_command:
            original_command = parent_command
        else:
            msg = (
                "Invalid input. Either command must be an instance of `disnake.APISlashCommand"
                "or parent_command must be provided."
            )
            raise ValueError(msg)

        for option in command.options:
            name = (
                f"{original_command.name} {command.name} {option.name}"
                if parent_command
                else f"{original_command.name} {option.name}"
            )
            if option.type == disnake.OptionType.sub_command_group:
                sub_commands.extend(
                    self._get_sub_commands(option, checks, category, original_command)
                )

            elif option.type == disnake.OptionType.sub_command:
                args = self._get_command_args(option)
                command_id = original_command.id
                dm_permissions = original_command.dm_permission
                nsfw = original_command.nsfw

                invokable = self.bot.get_slash_command(name)
                if not invokable:
                    return []
                desc = self._get_command_desc(invokable)
                cooldown = self._parse_cooldowns(invokable)
                sub_commands.append(
                    SlashCommand(
                        id=command_id,
                        name=name,
                        name_=name,
                        description=desc,
                        name_localizations=original_command.name_localizations,
                        description_localizations=original_command.description_localizations,
                        args=args,
                        checks=checks,
                        type=AppCommandType.SLASH,
                        dm_permission=dm_permissions,
                        nsfw=nsfw,
                        cooldown=cooldown,
                        category=category,
                        extras=invokable.extras,
                    )
                )

        return sub_commands

    def _parse_checks(
        self,
        command: commands.InvokableApplicationCommand,
    ) -> CommandChecks:
        """Parse any role or permission checks registered to the command."""
        permissions: List[str] = []
        roles: List[Union[str, int]] = []

        # command.checks provides a list of check predicates
        # associated with the command
        checks = command.checks

        # iterate those checks and analyze them to access
        # check names (ie. "has_any_role")
        for check in checks:
            name = check.__qualname__.split(".")[0]
            if "bot" in name or not check.__closure__:
                continue

            # for each check that does not include "bot" (ie. "bot_has_permissions")
            # the arguments will be parsed and used to populate `CommandChecks`
            closure = check.__closure__[0]

            args = (
                closure.cell_contents
                if len(closure.cell_contents) > 1
                else (closure.cell_contents,)
            )

            # checks pertaining to roles will populate CommandChecks.roles
            if "role" in name:
                roles.extend(args)

            # remaining checks should be permissions based and are formatted
            # then added to CommandChecks.permissions
            else:
                permissions.extend(
                    [p.replace("_", " ").title() for p, v in closure.cell_contents.items() if v]
                )

        return CommandChecks(permissions, roles)

    def _handle_slash_command(self, command: disnake.APISlashCommand) -> List[SlashCommand]:
        """Create a `SlashCommand` from the app command provided by disnake."""
        invokable = self.bot.get_slash_command(command.name)
        if invokable is None:
            return []

        checks = self._parse_checks(invokable)
        cooldown = self._parse_cooldowns(invokable)
        desc = self._get_command_desc(invokable)
        category = self._get_command_category(invokable)
        args = self._get_command_args(command)
        sub_commands = self._get_sub_commands(command, checks, category)

        if sub_commands:
            return sub_commands

        return [
            SlashCommand(
                id=command.id,
                name=command.name,
                name_=command.name,
                description=desc,
                name_localizations=command.name_localizations,
                description_localizations=command.description_localizations,
                args=args,
                checks=checks,
                type=AppCommandType.SLASH,
                dm_permission=command.dm_permission,
                nsfw=command.nsfw,
                cooldown=cooldown,
                guild_ids={command.guild_id} if command.guild_id else None,
                default_member_permissions=invokable.default_member_permissions,
                category=category,
                extras=invokable.extras,
            )
        ]

    def _handle_message_command(
        self, command: disnake.APIMessageCommand
    ) -> Optional[MessageCommand]:
        """Create `MessageCommand`s from the commands provided by disanke."""
        invokable = self.bot.get_message_command(command.name)
        if invokable is None:
            return invokable

        checks = self._parse_checks(invokable)
        cooldown = self._parse_cooldowns(invokable)
        desc = invokable.extras.get("help", "-")
        category = self._get_command_category(invokable)

        return MessageCommand(
            id=command.id,
            name=command.name,
            name_=command.name,
            description=desc,
            name_localizations=command.name_localizations,
            checks=checks,
            type=AppCommandType.MESSAGE,
            dm_permission=command.dm_permission,
            nsfw=command.nsfw,
            cooldown=cooldown,
            guild_ids={command.guild_id} if command.guild_id else None,
            default_member_permissions=invokable.default_member_permissions,
            category=category,
            extras=invokable.extras,
        )

    def _handle_user_command(self, command: disnake.APIUserCommand) -> Optional[UserCommand]:
        """Create `UserCommand`s from the command provided by disanke."""
        invokable = self.bot.get_user_command(command.name)

        if invokable is None:
            return invokable

        checks = self._parse_checks(invokable)
        cooldown = self._parse_cooldowns(invokable)
        desc = invokable.extras.get("help", "-")
        category = self._get_command_category(invokable)

        return UserCommand(
            id=command.id,
            name=command.name,
            name_=command.name,
            description=desc,
            name_localizations=command.name_localizations,
            checks=checks,
            type=AppCommandType.USER,
            dm_permission=command.dm_permission,
            nsfw=command.nsfw,
            cooldown=cooldown,
            guild_ids={command.guild_id} if command.guild_id else None,
            default_member_permissions=invokable.default_member_permissions,
            category=category,
            extras=invokable.extras,
        )

    def _get_command_category(self, command: commands.InvokableApplicationCommand) -> str:
        """Get the command's category or cog that it is associated with."""
        return (
            command.extras.get("category") or command.extras.get("plugin") or command.cog_name or ""
        )

    def _walk_app_commands(self) -> List[AppCommand]:
        """Retrieve all global and guild-specific application commands."""
        if self._app_commands:
            return self._app_commands

        all_commands = self.bot.global_application_commands
        for guild in self.bot.guilds:
            all_commands.extend(self.bot.get_guild_application_commands(guild.id))

        for command in all_commands:
            if self.commands_to_ignore and command.name in self.commands_to_ignore:
                continue

            if isinstance(command, disnake.APISlashCommand):
                self._app_commands.extend(self._handle_slash_command(command))

            elif isinstance(command, disnake.MessageCommand):
                msg_command = self._handle_message_command(command)

                if msg_command:
                    self._app_commands.append(msg_command)

            else:
                user_command = self._handle_user_command(command)

                if user_command:
                    self._app_commands.append(user_command)

        return self._app_commands
