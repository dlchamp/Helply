"""Helply command types"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Optional

__all__ = (
    "AppCommand",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",
)

if TYPE_CHECKING:
    from disnake import Locale, LocalizationValue, Permissions

    from .argument import Argument
    from .checks import CommandChecks, Cooldown
    from .enums import AppCommandType


@dataclass
class AppCommand:
    """Base class for all AppCommand types.

    AppCommands are classes that include various attributes from both
    `.ApplicationCommand` and `.InvokableApplicationCommand`

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's name. (Can be localized)
    name_: str
        Command's non-localized name. (*Needed to maintain static non-localized name for mention*)
    description: str
        Command's description
    name_localizations: disnake.LocalizationValue
        Contains localizations for the command's name. (*New in version 0.3.0*)
    checks : CommandChecks
        The command's permission and role requirements.
    args: List[Argument]
        Contains the command's arguments. (Only applies to SlashCommand)
    type: AppCommandType
        Type of command
    dm_permission : bool
        Whether the command is available in DMs or not.
    nsfw : bool
        Whether the command is NSFW (Not Safe For Work).
    category: Optional[str]
        Name of "category", "plugin" or "cog" the command belongs to.
    description_localizations: Optional[LocalizationValue]
        Contains localization information for the command's description. (*SlashCommand only*)
        (*New in version 0.3.0*)
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    extras: Optional[Dict[str, Any]]
        A dict of user provided extras for the command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return an AppCommand with localized attributes. (*New in version 0.3.0*)
    """

    id: int
    name: str
    name_: str
    description: str
    checks: CommandChecks
    type: AppCommandType
    dm_permission: bool
    nsfw: bool
    name_localizations: LocalizationValue
    category: Optional[str]
    description_localizations: Optional[LocalizationValue] = None
    args: List[Argument] = field(default_factory=list)
    cooldown: Optional[Cooldown] = None
    guild_id: Optional[int] = None
    default_member_permissions: Optional[Permissions] = None
    extras: Optional[Dict[str, Any]] = None

    @property
    def mention(self) -> str:
        """Return the clickable tag if SlashCommand, else bolded name."""
        if isinstance(self, SlashCommand):
            return f"</{self.name_}:{self.id}>"
        return f"**{self.name_}**"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AppCommand):
            return False

        return (
            self.name == other.name
            and self.name_ == other.name_
            and self.type == other.type
            and self.description == other.description
            and self.nsfw == other.nsfw
            and self.category == other.category
            and self.dm_permission == other.dm_permission
            and self.dm_permission == other.dm_permission
            and self.checks == other.checks
            and self.cooldown == other.cooldown
        )

    def get_localized_name(self, locale: Locale) -> str:
        """Return localized or non-localized name. specified by the provided locale.

        If not available return the non-localized name instead.

        Parameters
        ----------
        locale: disnake.Locale
            The interaction locale that will be used to localize attributes.

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
            The interaction locale that will be used to localize attributes.

        Returns
        -------
        str
            The localized or non-localized description.
        """
        if not self.description_localizations or not self.description_localizations.data:
            return self.description

        return self.description_localizations.data.get(str(locale), self.description)

    def localize(self, locale: Locale) -> AppCommand:
        """Return aAppCommand with localized attributes.

        Parameters
        ----------
        locale: Locale
            The interaction locale that will be used to localize attributes.

        Returns
        -------
        Appcommand
            a AppCommand with localized attributes.
        """
        ...


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
    dm_permission : bool
        Whether the command is available in DMs or not.
    nsfw : bool
        Whether the command is NSFW (Not Safe For Work).
    category: Optional[str]
        Name of "category", "plugin" or "cog" the command belongs to.
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    extras: Optional[Dict[str, Any]]
        A dict of user provided extras for the command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a SlashCommand with localized attributes. (*New in version 0.3.0*)
    """

    def localize(self, locale: Locale) -> SlashCommand:
        """Return a localized instance of SlashCommand

        Parameters
        ----------
        locale: Locale
            The locale to be used for localizing the command.

        Returns
        -------
        SlashCommand
            The localized SlashCommand.
        """
        args = [a.localize(locale) for a in self.args]
        name = self.get_localized_name(locale)
        desc = self.get_localized_description(locale)

        return SlashCommand(
            id=self.id,
            name=name,
            name_=self.name_,
            description=desc,
            checks=self.checks,
            type=self.type,
            category=self.category,
            dm_permission=self.dm_permission,
            nsfw=self.nsfw,
            name_localizations=self.name_localizations,
            description_localizations=self.description_localizations,
            cooldown=self.cooldown,
            guild_id=self.guild_id,
            default_member_permissions=self.default_member_permissions,
            args=args,
            extras=self.extras,
        )


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
    dm_permission : bool
        Whether the command is available in DMs or not.
    nsfw : bool
        Whether the command is NSFW (Not Safe For Work).
    category: Optional[str]
        Name of "category", "plugin" or "cog" the command belongs to.
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    extras: Optional[Dict[str, Any]]
        A dict of user provided extras for the command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a UserCommand with localized attributes. (*New in version 0.3.0*)
    """

    def localize(self, locale: Locale) -> UserCommand:
        """Return a localized instance of UserCommand

        Parameters
        ----------
        locale: Locale
            The locale to be used for localizing the command.

        Returns
        -------
        UserCommand
            The localized UserCommand.
        """
        name = self.get_localized_name(locale)
        desc = self.get_localized_description(locale)

        return UserCommand(
            id=self.id,
            name=name,
            name_=self.name_,
            description=desc,
            checks=self.checks,
            type=self.type,
            category=self.category,
            dm_permission=self.dm_permission,
            nsfw=self.nsfw,
            name_localizations=self.name_localizations,
            description_localizations=self.description_localizations,
            cooldown=self.cooldown,
            guild_id=self.guild_id,
            default_member_permissions=self.default_member_permissions,
            extras=self.extras,
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
    dm_permission : bool
        Whether the command is available in DMs or not.
    nsfw : bool
        Whether the command is NSFW (Not Safe For Work).
    category: Optional[str]
        Name of "category", "plugin" or "cog" the command belongs to.
    cooldown: Optional[Cooldown]
        The configured cooldown, if available. (*New in 0.4.0*)
    guild_id : Optional[int]
        The ID of the guild where the command is available.
    default_member_permissions : Optional[Permissions]
        Default member permissions required to use this command.
    extras: Optional[Dict[str, Any]]
        A dict of user provided extras for the command.
    mention : str
        Get the command as a mentionable if slash command, else return bolded name.

    Methods
    -------
    get_localized_name(locale: Optional[Locale])
        Return localized or non-localized name. (*New in version 0.3.0*)
    get_localized_description(locale: disnake.Locale)
        Return localized or non-localized description. (*New in version 0.3.0*)
    localize(locale: disnake.Locale)
        Return a UserCommand with localized attributes. (*New in version 0.3.0*)
    """

    def localize(self, locale: Locale) -> MessageCommand:
        """Return a localized instance of MessageCommand

        Parameters
        ----------
        locale: Locale
            The locale to be used for localizing the command.

        Returns
        -------
        SlashCommand
            The localized MessageCommand.
        """
        name = self.get_localized_name(locale)
        desc = self.get_localized_description(locale)

        return MessageCommand(
            id=self.id,
            name=name,
            name_=self.name_,
            description=desc,
            checks=self.checks,
            type=self.type,
            category=self.category,
            dm_permission=self.dm_permission,
            nsfw=self.nsfw,
            name_localizations=self.name_localizations,
            description_localizations=self.description_localizations,
            cooldown=self.cooldown,
            guild_id=self.guild_id,
            default_member_permissions=self.default_member_permissions,
            extras=self.extras,
        )
