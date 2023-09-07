from typing import Dict, List, Optional, Sequence, Union

import disnake
import disnake.app_commands
from disnake.ext import commands

from .types import (
    AppCommand,
    AppCommandType,
    Argument,
    CommandChecks,
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


class Helply:
    """Represents an application command helper.

    Parameters
    ----------
    bot : Union[commands.Bot, commands.InteractionBot]
        The bot for which this help class will be associated with.
    commands_to_ignore: Iterable[str]
        Provide a list of command names to ignore when walking all app commands.
    """

    def __init__(self, bot: Bot, commands_to_ignore: Optional[Sequence[str]] = None) -> None:
        self.bot = bot

        if commands_to_ignore is not None:
            self.commands_to_ignore: set[str] = set(commands_to_ignore)
        else:
            self.commands_to_ignore = set()

        self._app_commands: Dict[int, AppCommand] = {}

    def _get_command_args(
        self, command: Union[disnake.APISlashCommand, disnake.Option]
    ) -> List[Argument]:
        """Parse and return the `SlashCommand` or `SubCommand` arguments.

        Parameters
        ----------
        command : Union[disnake.APISlashCommand, disnake.Option]
            The slash command or a slash command's sub_command.

        Returns
        -------
        List[Argument]
            A sequence of the command or sub_command's arguments.
        """
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

    def _get_command_desc(self, name: str) -> str:
        """Get the description for a command.

        Parameters
        ----------
        name : str
            The name of the command.

        Returns
        -------
        str
            The description of the command.
        """
        desc = "-"
        command = self.bot.get_slash_command(name)

        if command and isinstance(command, (commands.InvokableSlashCommand, commands.SubCommand)):
            desc = command.extras.get("help", "") or command.description

        return desc

    def _get_sub_commands(
        self,
        command: Union[disnake.APISlashCommand, disnake.Option],
        checks: CommandChecks,
        category: str,
        parent_command: Optional[disnake.APISlashCommand] = None,
    ) -> List[SlashCommand]:
        """Get and return the `APISlashCommand`'s registered `SubCommands` if any.

        Parameters
        ----------
        command : Union[disnake.APISlashCommand, disnake.Option]
            The registered slash command or the command's SubCommand.
        checks : CommandChecks
            The permission and role checks assigned to the parent command.
        parent_name : Optional[str]
            Parent command's name. Only used if sub_group is used and this function is called
            recursively.

        Returns
        -------
        List[SlashCommand]
            A list of sub-commands, if any.
        """
        sub_commands: List[SlashCommand] = []

        for option in command.options:
            name = (
                f"{parent_command.name} {command.name} {option.name}"
                if parent_command
                else f"{command.name} {option.name}"
            )
            if option.type == disnake.OptionType.sub_command:
                args = self._get_command_args(option)

                if parent_command:
                    command_id = parent_command.id
                    dm_permissions = parent_command.dm_permission
                    nsfw = parent_command.nsfw

                elif isinstance(command, disnake.APISlashCommand):
                    command_id = command.id
                    dm_permissions = command.dm_permission
                    nsfw = command.nsfw

                else:
                    # should realistically never be reached
                    raise TypeError(
                        "Command must be an instance of `disnake.APISlashCommand` "
                        "if parent_command is `None`"
                    ) from None

                desc = self._get_command_desc(name)
                sub_commands.append(
                    SlashCommand(
                        id=command_id,
                        name=name,
                        description=desc,
                        name_localizations=command.name_localizations,
                        description_localizations=command.description_localizations,
                        args=args,
                        checks=checks,
                        type=AppCommandType.slash,
                        dm_permission=dm_permissions,
                        nsfw=nsfw,
                        category=category,
                    )
                )
            elif option.type == disnake.OptionType.sub_command_group:
                sub_commands.extend(
                    self._get_sub_commands(option, checks, category, parent_command)
                )

        return sub_commands

    def _parse_checks(
        self,
        command: commands.InvokableApplicationCommand,
    ) -> CommandChecks:
        """Parse the checks associated with a command and extract registered permissions and roles.

        Parameters
        ----------
        command : commands.InvokableApplicationCommand
            The command object to parse checks from.

        Returns
        -------
        CommandChecks
            A NamedTuple containing a list of permissions and/or role names or IDs
            required to invoke the command.
        """

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
        """Handle creation of `SlashCommand` from `disnake.APISlashCommand`.

        Parameters
        ----------
        command : disnake.APISlashCommand
            The APISlashCommand provided by Discord's API.

        Return
        ------
        List[SlashCommand]
            The constructed `SlashCommand`.
        """
        invokable = self.bot.get_slash_command(command.name)
        if invokable is None:
            return []

        checks = self._parse_checks(invokable)
        desc = self._get_command_desc(invokable.qualified_name)
        category = self._get_command_category(invokable)
        args = self._get_command_args(command)
        sub_commands = self._get_sub_commands(command, checks, category)

        if sub_commands:
            return sub_commands

        return [
            SlashCommand(
                id=command.id,
                name=command.name,
                description=desc,
                name_localizations=command.name_localizations,
                description_localizations=command.description_localizations,
                args=args,
                checks=checks,
                type=AppCommandType.slash,
                dm_permission=command.dm_permission,
                nsfw=command.nsfw,
                guild_id=command.guild_id,
                default_member_permissions=invokable.default_member_permissions,
                category=category,
            )
        ]

    def _handle_message_command(
        self, command: disnake.APIMessageCommand
    ) -> Optional[MessageCommand]:
        """Handle creation of `MessageCommand` from `disnake.APIMessageCommand`.

        Parameters
        ----------
        command : disnake.APIUserCommand
            The APIMessageCommand provided by Discord's API.

        Return
        ------
        Optional[MessageCommand]
            The constructed `MessageCommand`.
        """
        invokable = self.bot.get_message_command(command.name)
        if invokable is None:
            return

        checks = self._parse_checks(invokable)
        desc = invokable.extras.get("help", "-")
        category = self._get_command_category(invokable)

        return MessageCommand(
            id=command.id,
            name=command.name,
            description=desc,
            name_localizations=command.name_localizations,
            checks=checks,
            type=AppCommandType.message,
            dm_permission=command.dm_permission,
            nsfw=command.nsfw,
            guild_id=command.guild_id,
            default_member_permissions=invokable.default_member_permissions,
            category=category,
        )

    def _handle_user_command(self, command: disnake.APIUserCommand) -> Optional[UserCommand]:
        """Handle creation of `UserCommand` from `disnake.APIUserCommand`.

        Parameters
        ----------
        command : disnake.APIUserCommand
            The APIUserCommand provided by Discord's API.

        Return
        ------
        Optional[UserCommand]
            The constructed `UserCommand`.
        """
        invokable = self.bot.get_user_command(command.name)

        if invokable is None:
            return

        checks = self._parse_checks(invokable)
        desc = invokable.extras.get("help", "-")
        category = self._get_command_category(invokable)

        return UserCommand(
            id=command.id,
            name=command.name,
            description=desc,
            name_localizations=command.name_localizations,
            checks=checks,
            type=AppCommandType.user,
            dm_permission=command.dm_permission,
            nsfw=command.nsfw,
            guild_id=command.guild_id,
            default_member_permissions=invokable.default_member_permissions,
            category=category,
        )

    def _get_command_category(self, invokable: commands.InvokableApplicationCommand) -> str:
        """Get the command's cog or category name, if available

        `cog_name` would be derived from `disnake.ext.commands.Cog`, whereas
        `category` would come from using [disnake-ext-plugins](https://github.com/DisnakeCommunity/disnake-ext-plugins)

        Parameters
        ----------
        invokable: commands.InvokableApplicationCommand

        Returns
        -------
        str
            `Cog's` name or str value set in `.extras['category']` or 'None'

        """
        name = invokable.cog_name or invokable.extras.get("category")
        if not name:
            name = "None"

        return name

    def _walk_app_commands(self) -> None:
        """Retrieve all global and guild-specific application commands."""
        all_commands = self.bot.global_application_commands
        for guild in self.bot.guilds:
            all_commands.extend(self.bot.get_guild_application_commands(guild.id))

        for command in all_commands:
            if self.commands_to_ignore and command.name in self.commands_to_ignore:
                continue

            if isinstance(command, disnake.APISlashCommand):
                self._app_commands.update({c.id: c for c in self._handle_slash_command(command)})

            elif isinstance(command, disnake.MessageCommand):
                msg_command = self._handle_message_command(command)

                if msg_command:
                    self._app_commands[msg_command.id] = msg_command

            else:
                user_command = self._handle_user_command(command)

                if user_command:
                    self._app_commands[user_command.id] = user_command

    def get_all_commands(
        self,
        guild_id: Optional[int] = None,
        *,
        permissions: Optional[disnake.Permissions] = None,
        include_nsfw: bool = True,
        dm_only: bool = False,
    ) -> List[AppCommand]:
        """Retrieve a filtered list of AppCommand based on specified criteria.

        By default, this method should return all registered commands. Specify filters
        to narrow down the output results.

        Parameters
        ----------
        guild_id : Optional[int]
            Filter commands registered to the specified guild_id.  If not specified,
            all commands may be returned.
        permissions: Optional[disnake.Permissions]
            Filter commands that do not exceed permissions. If not specified,
            commands will not be filtered by permissions.
            !!! Note
                Should not be used with `dm_only`
        include_nsfw : bool
            Whether or not to include categories NSFW commands.
        dm_only: bool
            Whether or not to include only commands with direct message enabled.
            !!! Note
                Should not specify `guild_id` or `permissions` if setting this to True

        Returns
        -------
        List[AppCommand]
            Resulting list of AppCommands after filters have been applied.
        """

        if not self._app_commands:
            self._walk_app_commands()

        commands: List[AppCommand] = []

        for command in self._app_commands.values():
            if guild_id and command.guild_id and command.guild_id != guild_id:
                continue

            if dm_only and not command.dm_permission:
                continue

            if not permissions and command.default_member_permissions:
                continue

            if (
                permissions
                and command.default_member_permissions
                and not permissions >= command.default_member_permissions
            ):
                continue

            if not include_nsfw and command.nsfw:
                continue

            commands.append(command)

        return commands

    def get_command_named(
        self, name: str, cmd_type: Optional[AppCommandType] = None
    ) -> Optional[AppCommand]:
        """Get a command by its non-localized name

        Parameters
        ----------
        name : str
            Name of the ApplicationCommand.
        cmd_type: Optional[AppCommandType]
            Specify the type of command to be returned. If not specified, the first matching
            command will be returned regardless of its type.


        Returns
        -------
        Optional[AppCommand]
            The command that matches the provided name, if found.
        """
        for command in self._app_commands.values():
            if command.name == name and (cmd_type is None or command.type is cmd_type):
                return command

    def get_command(self, id: int) -> Optional[AppCommand]:
        """Get a command by its ID

        Parameters
        ----------
        id: int
            ID of the AppCommand

        Returns
        --------
        Optional[AppCommand]
            The retrieved AppCommand or None of not found.
        """
        return self._app_commands.get(id)

    def get_commands_by_category(
        self,
        category: str,
        *,
        guild_id: Optional[int] = None,
        permissions: Optional[disnake.Permissions] = None,
        include_nsfw: bool = True,
        dm_only: bool = False,
    ) -> List[AppCommand]:
        """Retrieve a filtered list of AppCommand based on specified criteria within a category.

        By default, this method should return all registered commands within a category.
        Specify filters to narrow down the output results.

        Parameters
        ----------
        category: str
            Category for which commands are in.
        guild_id : Optional[int]
            Filter commands registered to the specified guild_id.  If not specified,
            all commands may be returned.
        permissions: Optional[disnake.Permissions]
            Filter commands that do not exceed permissions. If not specified,
            commands will not be filtered by permissions.
            !!! Note
                Should not be used with `dm_only`
        include_nsfw : bool
            Whether or not to include categories NSFW commands.
        dm_only: bool
            Whether or not to include only commands with direct message enabled.
            !!! Note
                Should not specify `guild_id` or `permissions` if setting this to True

        Returns
        --------
        List[AppCommand]
            A list of commands within the specified group name.

        """
        commands = self.get_all_commands(
            guild_id,
            permissions=permissions,
            include_nsfw=include_nsfw,
            dm_only=dm_only,
        )
        return [command for command in commands if command.category == category]

    def get_categories(
        self,
        guild_id: Optional[int] = None,
        *,
        permissions: Optional[disnake.Permissions] = None,
        include_nsfw: bool = True,
        dm_only: bool = False,
    ) -> List[str]:
        """Return a unique list of command group names.

        Useful if you wish to have an autocomplete for users to select from available
        command groups

        Parameters
        ----------
        guild_id : Optional[int]
            Filter categories with commands registered to the specified guild_id. If not
            specified, all categories may be returned.
        permissions: Optional[disnake.Permissions]
            Filter commands that do not exceed permissions. If not specified,
            commands will not be filtered by permissions.
            !!! Note
                Should not be used with `dm_only`
        include_nsfw : bool
            Whether or not to include categories NSFW commands.
        dm_only: bool
            Whether or not to include only commands with direct message enabled.
            !!! Note
                Should not specify `guild_id` or `permissions` if setting this to True

        Example:
        ```py
        @some_command.autocomplete('category')
        async def some_command_group_autocomplete(
            inter: disnake.ApplicationCommandInteraction, string: str
        ) -> List[str]:
            string = string.casefold()
            commands = helper.get_command_categories(inter.guild.id)
            return [g for g in commands if string in g.casefold()]
        ```

        Returns
        -------
        List[str]
            A list of unique command categories.
        """
        categories: List[str] = []

        for command in self.get_all_commands(
            guild_id,
            permissions=permissions,
            include_nsfw=include_nsfw,
            dm_only=dm_only,
        ):
            if command.category not in categories:
                categories.append(command.category)

        return categories

    def get_dm_only_commands(self, *, include_nsfw: bool = False) -> List[AppCommand]:
        """A shortcut method for returning only commands with direct message enabled.

        Parameters
        ----------
        include_nsfw: bool
            Whether or not to include NSFW commands.

        Returns
        -------
        List[AppCommand]
            A list of commands with `.dm_permissions` set to True
        """
        return self.get_all_commands(dm_only=True, include_nsfw=include_nsfw)

    def get_guild_commands(
        self,
        guild_id: int,
        *,
        include_nsfw: bool = False,
        permissions: Optional[disnake.Permissions] = None,
    ) -> List[AppCommand]:
        """This method returns global and guild-specific commands available to a guild.

        !!! Note
            Including `permissions` will restrict the command list to prevent commands hidden by
            default_command_permissions from appearing to the command author.

        Parameters
        guild_id: int
            ID for the guild for which guild-specific command are registered.
        include_nsfw: bool
            Whether or not to include NSFW commands.
        permissions: Optional[disnake.Permissions]
            Set the permission limit of the resulting commands.  Any commands that exceed specified
            permissions will be omitted
        """
        return self.get_all_commands(guild_id, include_nsfw=include_nsfw, permissions=permissions)

    @staticmethod
    def roles_from_checks(checks: CommandChecks, guild: disnake.Guild) -> List[disnake.Role]:
        """Parse the command's role checks and return a list of `disnake.Role`.

        Parameters
        ----------
        checks : CommandChecks
            A command's checks

        Returns
        -------
        List[disnake.Role]
            `Roles` that have been successfully converted from name or ID.
        """
        role_checks = checks.roles
        roles: List[disnake.Role] = []

        for name_or_id in role_checks:
            if isinstance(name_or_id, int) or name_or_id.isdigit():
                role = guild.get_role(int(name_or_id))
            else:
                role = disnake.utils.get(guild.roles, name=name_or_id)

            if role:
                roles.append(role)

        return roles
