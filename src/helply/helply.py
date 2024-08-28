"""# Helply

Handles the creation and storing of the app commands and provides the methods to retrive them
"""

from typing import List, Optional, Sequence, Union

from .__wrappers import Bot, CommandHandler, Locale, Permissions
from .types import AppCommand, AppCommandType


class Helply:
    """An application command helper.

    Helply is an application command helper that interfaces with the different
    forks of discord.py.  Currently, only disnake and nextcord are supported.

    This class dynamically selects an appropriate command handler for the supported
    wrapper and provides methods that allow you to access your commands and create
    "help" responses for them.
    """

    def __init__(self, bot: Bot, commands_to_ignore: Union[Sequence[str], None] = None) -> None:
        self.bot = bot
        self._handler = CommandHandler(bot, commands_to_ignore)

        self.bot.add_listener(self._walk_app_commands_coro, "on_ready")

    @property
    def app_commands(self) -> List[AppCommand]:
        """Return all app commands cached by Helply."""
        return self._handler._app_commands

    def _walk_app_commands(self) -> List[AppCommand]:
        return self._handler._walk_app_commands()

    async def _walk_app_commands_coro(self) -> List[AppCommand]:
        """Coroutine version of `_walk_app_commands.

        Only used so we can throw it in on_ready.
        """
        return self._walk_app_commands()

    def get_commands(
        self,
        guild_id: Optional[int] = None,
        *,
        permissions: Optional[Permissions] = None,
        include_nsfw: bool = False,
        dm_only: bool = False,
        locale: Optional[Locale] = None,
    ) -> List[AppCommand]:
        """Retrieve AppCommands based on the provided arguments.

        By default, this method returns all registered commands.
        Provide arguments to narrow down the results.'''

        Parameters
        ----------
        guild_id : Optional[int]
            Filter commands registered to the specified guild_id.  If not specified,
            all commands may be returned.
        permissions: Optional[Permissions]
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
        locale: Optional[Locale]
            Specify locale to get localized commands and arguments, where available.

        Returns
        -------
        List[AppCommand]
            Resulting list of `AppCommand`. If locale is specified, the command will be returned
            with localized attributes.
        """
        if not self.app_commands:
            self._walk_app_commands()

        commands: List[AppCommand] = []

        for command in self.app_commands:
            if guild_id and command.guild_ids and guild_id not in command.guild_ids:
                continue

            if dm_only and not command.dm_permission:
                continue

            if (
                permissions
                and command.default_member_permissions
                and permissions < command.default_member_permissions
            ):
                continue

            if not include_nsfw and command.nsfw:
                continue

            if locale:
                command = command.localize(locale)  # noqa: PLW2901

            if command not in commands:
                commands.append(command)

        return commands

    def get_command_named(
        self,
        name: str,
        locale: Optional[Locale] = None,
        cmd_type: Optional[AppCommandType] = None,
    ) -> Optional[AppCommand]:
        """Get a command by its name.

        !!! Warning
            When passing a locale, the provided name needs to match the localized name.
            This works best when receiving a command name from autocomplete.

        Parameters
        ----------
        name : str
            Name of the ApplicationCommand.
        locale: Optional[Locale]
            Specify locale to get a localized command and arguments.
        cmd_type: Optional[AppCommandType]
            Specify the type of command to be returned. If not specified, the first matching
            command will be returned regardless of its type.


        Returns
        -------
        Optional[AppCommand]
            The command that matches the provided name and type, if available.
        """
        for command in self.get_commands():
            if command.name == name and (cmd_type is None or command.type is cmd_type):
                if locale:
                    return command.localize(locale)

                return command

    def get_dm_only_commands(
        self,
        *,
        include_nsfw: bool = False,
        locale: Optional[Locale] = None,
    ) -> List[AppCommand]:
        """Return only commands with dm_permission set to True.

        Parameters
        ----------
        include_nsfw: bool
            Whether or not to include NSFW commands.
        locale: Optional[nextcord.Locale]
            Include local to get localized commands.


        Returns
        -------
        List[AppCommand]
            A list of AppCommand where dm_permission is True.
        """
        return self.get_commands(dm_only=True, locale=locale, include_nsfw=include_nsfw)

    def get_guild_commands(
        self,
        guild_id: int,
        *,
        include_nsfw: bool = False,
        permissions: Optional[Permissions] = None,
        locale: Optional[Locale] = None,
    ) -> List[AppCommand]:
        """Return commands where guild_id is None or guild_id matches specified guild_id.

        !!! Note
            Including `permissions` will restrict the command list to prevent commands hidden by
            default_command_permissions from appearing to the command author.

        Parameters
        ----------
        guild_id: int
            ID for the guild for which guild-specific command are registered.
        include_nsfw: bool
            Whether or not to include NSFW commands.
        permissions: Optional[Permissions]
            Set the permission limit of the resulting commands.  Any commands that exceed specified
            permissions will be omitted
        locale: Optional[Locale]
            Specify locale to get localized commands and arguments.

        Returns
        -------
        List[AppCommand]
            A list of AppCommand where guild_id is not specified (global) or guild_id matches
            the specified guild_id.
        """
        return self.get_commands(
            guild_id, locale=locale, include_nsfw=include_nsfw, permissions=permissions
        )
