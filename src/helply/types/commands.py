from typing import TYPE_CHECKING, List, Optional

from disnake import Locale, LocalizationValue, Permissions

from .abc_ import AppCommandBase, ArgumentBase
from .checks import CommandChecks
from .localized import (
    LocalizedAppCommand,
    LocalizedArgument,
    LocalizedMessageCommand,
    LocalizedSlashCommand,
    LocalizedUserCommand,
)

if TYPE_CHECKING:
    from .enums import AppCommandType

__all__ = (
    "Argument",
    "AppCommand",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",
)


class Argument(ArgumentBase):
    """Represents a SlashCommand argument.

    Attributes
    ----------
    name: str
        Argument's non-localized name
    description: str
        Argument's non-localized description
    required: bool
        Whether or not the argument is required.
    name_localizations: disnake.LocalizationValue
        Contains localizations for the argument's name. (*New in version 0.3.0*)
    description_localizations: disnake.LocalizationValue
        Contains localizations for the argument's description. (*New in version 0.3.0*)

    Methods
    -------
    get_localized_name(locale: disnake.Locale)
        Returns localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Returns a LocalizedArgument (*New in version 0.3.0*)
    """

    def __init__(
        self,
        name: str,
        description: str,
        required: bool,
        name_localizations: LocalizationValue,
        description_localizations: LocalizationValue,
    ) -> None:
        super().__init__(name=name, description=description, required=required)

        self.name_localizations: LocalizationValue = name_localizations
        self.description_localizations: LocalizationValue = description_localizations

    def get_localized_name(self, locale: Locale) -> str:
        """Returns localized or non-localized name. specified by the provided locale.

        If not available, returns the non-localized name instead.

        Parameters
        ----------
        locale: disnake.Local
            The interaction locale

        Returns
        -------
        str
            The localized or non-localized name.
        """
        if not self.name_localizations or not self.name_localizations.data:
            return self.name

        return self.name_localizations.data.get(str(locale), self.name)

    def get_localized_description(self, locale: Locale) -> str:
        """Returns localized or non-localized description. specified by the provided locale.

        If not available, returns the non-localized description instead.

        Parameters
        ----------
        locale: disnake.Local
            The interaction locale

        Returns
        -------
        str
            The localized or non-localized description.
        """
        if not self.description_localizations or not self.description_localizations.data:
            return self.name

        return self.description_localizations.data.get(str(locale), self.description)

    def localize(self, locale: Locale) -> LocalizedArgument:
        """Returns a LocalizedArgument instance from this Argument.

        LocalizedArument instances are just simplified Arguments with localized attribute values

        Parameters
        ----------
        locale: disnake.Locale
            The locale that should be used to localize the argument.

        Returns
        -------
        LocalizedArgument
            This argument with localized name and description
        """
        return LocalizedArgument(
            name=self.get_localized_name(locale),
            description=self.get_localized_description(locale),
            required=self.required,
        )


class AppCommand(AppCommandBase):
    """Represents an AppCommand.

    AppCommands are classes that include various attributes from both
    `.ApplicationCommand` and `.InvokableApplicationCommand`


    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's  name
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
    description_localizations: Optional[LocalizationValue]
        Contains localization information for the command's description. (*SlashCommand only*)
        (*New in version 0.3.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else returns bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Returns localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Returns a LocalizedAppcommand, or sub-variant (*New in version 0.3.0*)
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: "AppCommandType",
        name_localizations: LocalizationValue,
        category: str,
        dm_permission: bool,
        nsfw: bool,
        description_localizations: Optional[LocalizationValue] = None,
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

        self.name_localizations: LocalizationValue = name_localizations
        self.description_localizations: Optional[LocalizationValue] = description_localizations

    def get_localized_name(self, locale: Locale) -> str:
        """Returns localized or non-localized name. specified by the provided locale.

        If not available returns the non-localized name instead.

        Parameters
        ----------
        locale: disnake.Locale
            The interaction locale

        Returns
        -------
        str
            The localized or non-localized name.
        """
        if not self.name_localizations.data:
            return self.name

        return self.name_localizations.data.get(str(locale), self.name)

    def get_localized_description(self, locale: Locale) -> str:
        """Returns localized or non-localized description. specified by the provided locale.

        If not available, returns the non-localized description instead.

        Parameters
        ----------
        locale: disnake.Locale
            The interaction locale

        Returns
        -------
        str
            The localized or non-localized description.
        """
        if not self.description_localizations or not self.description_localizations.data:
            return self.description

        return self.description_localizations.data.get(str(locale), self.description)

    def localize(self, locale: Locale) -> LocalizedAppCommand:
        name = self.get_localized_name(locale)
        description = self.get_localized_description(locale)

        if isinstance(self, SlashCommand):
            args = [a.localize(locale) for a in self.args]
            return LocalizedSlashCommand(
                id=self.id,
                _name=self.name,
                name=name,
                description=description,
                args=args,
                checks=self.checks,
                type=self.type,
                category=self.category,
                nsfw=self.nsfw,
                dm_permission=self.dm_permission,
                guild_id=self.guild_id,
                default_member_permissions=self.default_member_permissions,
            )

        if isinstance(self, UserCommand):
            return LocalizedUserCommand(
                id=self.id,
                _name=self.name,
                name=name,
                description=description,
                checks=self.checks,
                type=self.type,
                dm_permission=self.dm_permission,
                category=self.category,
                nsfw=self.nsfw,
                guild_id=self.guild_id,
                default_member_permissions=self.default_member_permissions,
            )

        return LocalizedMessageCommand(
            id=self.id,
            _name=self.name,
            name=name,
            description=description,
            checks=self.checks,
            type=self.type,
            dm_permission=self.dm_permission,
            category=self.category,
            nsfw=self.nsfw,
            guild_id=self.guild_id,
            default_member_permissions=self.default_member_permissions,
        )


class SlashCommand(AppCommand):
    """Represents a slash command type AppCommand

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
    description_localizations: disnake.LocalizationValue
        Contains localizations for the command's description. (*New in version 0.3.0*)
    args: List[Argument]
        Contains the command's arguments
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
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else returns bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Returns localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Returns a LocalizedSlashCommand
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: "AppCommandType",
        args: List[Argument],
        name_localizations: LocalizationValue,
        description_localizations: LocalizationValue,
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
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )

        self.args: List[Argument] = args


class UserCommand(AppCommand):
    """Represents a user command type AppCommand


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
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else returns bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Returns localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Returns a LocalizedAppcommand, or sub-variant. (*New in version 0.3.0*)
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: "AppCommandType",
        name_localizations: LocalizationValue,
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
            name_localizations=name_localizations,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )


class MessageCommand(AppCommand):
    """Represents a message command type AppCommand

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
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else returns bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Returns localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Returns a LocalizedAppcommand, or sub-variant
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: "AppCommandType",
        name_localizations: LocalizationValue,
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
            name_localizations=name_localizations,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )
