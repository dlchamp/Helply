"""Base classes for the types used within Helply."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

__all__ = ("Argument",)

if TYPE_CHECKING:
    from disnake import Locale, LocalizationValue


@dataclass
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
        Return an Argument with localized attributes (*New in version 0.3.0*)
    """

    name: str
    description: str
    required: bool
    name_localizations: LocalizationValue
    description_localizations: LocalizationValue

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
            return self.description

        return self.description_localizations.data.get(str(locale), self.description)

    def localize(self, locale: Locale) -> Argument:
        """Return a Argument instance with localized name and description.

        Parameters
        ----------
        locale: disnake.Locale
            The locale that should be used to localize the argument.

        Returns
        -------
        Argument
            This argument with localized name and description
        """
        return Argument(
            name=self.get_localized_name(locale),
            description=self.get_localized_description(locale),
            required=self.required,
            name_localizations=self.name_localizations,
            description_localizations=self.description_localizations,
        )
