import dataclasses
from typing import TYPE_CHECKING, List, Optional

from disnake import Locale, LocalizationValue, Permissions

from .checks import CommandChecks

if TYPE_CHECKING:
    from .enums import AppCommandType


__all__ = (
    "AppCommand",
    "Argument",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",
)


@dataclasses.dataclass
class Argument:
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
        Contains localizations for the argument's name
    description_localizations: disnake.LocalizationValue
        Contains localizations for the argument's description.

    Methods
    -------
    get_localized_name(locale: disnake.Locale)
        Returns localized or non-localized name.
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description.
    """

    name: str
    name_localizations: LocalizationValue
    description: str
    description_localizations: LocalizationValue
    required: bool

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


@dataclasses.dataclass
class AppCommand:
    """Represents an AppCommand.

    AppCommands are dataclasses that include various attributes from both
    `.ApplicationCommand` and `.InvokableApplicationCommand`

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name: str
        Command's non-localized name
    description: str
        Command's non-localized description
    name_localizations: disnake.LocalizationValue
        Contains localizations for the command's name
    description_localizations: Optional[disnake.LocalizationValue]
        Contains localizations for the command's description.
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
    guild_id : int, optional
        The ID of the guild where the command is available.
    default_member_permissions : Permissions, optional
        Default member permissions required to use this command.
    mention : str
        Get the command as a mentionable if slash command, else returns bolded name.

    Methods
    -------
    get_localized_mention(locale: disnake.Locale)
    get_localized_name(locale: Optional[Locale])
        Returns localized or non-localized name.
    get_localized_description(locale: disnake.Locale)
        Returns localized or non-localized description.
    """

    id: int
    name: str
    description: str
    checks: CommandChecks
    type: "AppCommandType"
    name_localizations: LocalizationValue
    description_localizations: Optional[LocalizationValue] = None
    category: str = "None"
    dm_permission: bool = True
    nsfw: bool = False
    guild_id: Optional[int] = None
    default_member_permissions: Optional[Permissions] = None

    @property
    def mention(self) -> str:
        """Returns the"""
        if isinstance(self, SlashCommand):
            return f"</{self.name}:{self.id}>"
        return f"**{self.name}**"

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


@dataclasses.dataclass
class SlashCommand(AppCommand):
    """Represents a SlashCommand type AppCommand.

    Attributes
    ----------
    args : List[Argument]
        A list of the command's Arguments, if any.
    """

    args: List[Argument] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class UserCommand(AppCommand):
    """Represents a UserCommand type of AppCommand."""

    ...


@dataclasses.dataclass
class MessageCommand(AppCommand):
    """Represents a MessageCommand type of AppCommand."""

    ...
