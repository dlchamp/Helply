"""Helply command types"""
from typing import Any, List, Optional

from disnake import Locale, LocalizationValue, Permissions

from .abc_ import AppCommandBase, ArgumentBase
from .checks import CommandChecks, Cooldown
from .enums import AppCommandType
from .localized import (
    LocalizedAppCommand,
    LocalizedArgument,
    LocalizedMessageCommand,
    LocalizedSlashCommand,
    LocalizedUserCommand,
)

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
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a LocalizedArgument (*New in version 0.3.0*)
    """

    __slots__ = (
        "name_localizations",
        "description_localizations",
    )

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
        """Return localized or non-localized name. specified by the provided locale.

        If not available, return the non-localized name instead.

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
        """Return localized or non-localized description. specified by the provided locale.

        If not available, return the non-localized description instead.

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
        """Return a LocalizedArgument instance from this Argument.

        LocalizedArgument instances are just simplified Arguments with localized attribute values

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
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a LocalizedAppcommand, or sub-variant (*New in version 0.3.0*)
    """

    __slots__ = (
        "name_localizations",
        "description_localizations",
    )

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        name_localizations: LocalizationValue,
        category: str,
        dm_permission: bool,
        nsfw: bool,
        cooldown: Optional[Cooldown],
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
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )

        self.name_localizations: LocalizationValue = name_localizations
        self.description_localizations: Optional[LocalizationValue] = description_localizations

    @property
    def mention(self) -> str:
        """Return clickable mention if slash, else bolded name."""
        if self.type is AppCommandType.SLASH:
            return f"</{self.name}:{self.id}>"

        return f"**{self.name}**"

    def __eq__(self, other: Any) -> bool:
        """Return True if self == other, else False"""
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id or (
            self.description == other.description
            and self.checks == other.checks
            and self.category == other.category
            and self.cooldown == other.cooldown
            and self.nsfw == other.nsfw
            and self.default_member_permissions == other.default_member_permissions
        )

    def get_localized_name(self, locale: Locale) -> str:
        """Return localized or non-localized name. specified by the provided locale.

        If not available return the non-localized name instead.

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
        """Return localized or non-localized description. specified by the provided locale.

        If not available, Return the non-localized description instead.

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
        """Return a localized variant of the AppCommand.

        Parameters
        ----------
        locale: disnake.Locale
            Locale key used to set new attributes.

        Returns
        -------
        LocalizedAppCommand
            A localized variant of the AppCommand.
        """
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
                cooldown=self.cooldown,
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
                cooldown=self.cooldown,
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
            cooldown=self.cooldown,
            guild_id=self.guild_id,
            default_member_permissions=self.default_member_permissions,
        )


class SlashCommand(AppCommand):
    """Represents a slash command type AppCommand.

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
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a LocalizedSlashCommand
    """

    __slots__ = ("args",)

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        args: List[Argument],
        name_localizations: LocalizationValue,
        description_localizations: LocalizationValue,
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
            name_localizations=name_localizations,
            description_localizations=description_localizations,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )

        self.args: list[Argument] = args


class UserCommand(AppCommand):
    """Represents a user command type AppCommand.


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
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a LocalizedAppcommand, or sub-variant. (*New in version 0.3.0*)
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        name_localizations: LocalizationValue,
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
            name_localizations=name_localizations,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )


class MessageCommand(AppCommand):
    """Represents a message command type AppCommand.

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
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a LocalizedAppcommand, or sub-variant
    """

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        checks: CommandChecks,
        type: AppCommandType,
        name_localizations: LocalizationValue,
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
            name_localizations=name_localizations,
            category=category,
            dm_permission=dm_permission,
            nsfw=nsfw,
            cooldown=cooldown,
            guild_id=guild_id,
            default_member_permissions=default_member_permissions,
        )
