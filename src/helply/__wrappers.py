"""Handle multiple discord wrappers - inspired by mafic: https://github.com/ooliver1/mafic"""
import os
from typing import List, Tuple

from pkg_resources import DistributionNotFound, get_distribution

from helply import errors

try:
    import dotenv
except ModuleNotFoundError:
    pass
else:
    dotenv.load_dotenv()


wrappers: Tuple[str, ...] = (
    "disnake",
    "nextcord",
)


if not os.getenv("SKIP_LIB_CHECK"):
    installed: List[str] = []

    for wrapper in wrappers:
        try:
            get_distribution(wrapper)
        except DistributionNotFound:
            pass
        else:
            installed.append(wrapper)

    if len(installed) > 1:
        raise errors.MultipleSupportedWrappers(installed)

    elif not installed:
        raise errors.NoSupportedWrappers

    installed_wrapper = installed[0]
else:
    installed_wrapper = "nextcord"

if installed_wrapper == "disnake":
    from disnake import Color, Embed, Guild, Locale, Permissions, Role, version_info
    from disnake.ext.commands import Bot

    from .handlers.disnake_handler import DisnakeCommandHandler as CommandHandler

else:
    from nextcord import Color, Embed, Guild, Locale, Permissions, Role, version_info
    from nextcord.ext.commands import Bot

    from .handlers.nextcord_handler import NextcordCommandHandler as CommandHandler


if version_info.major < 2:  # noqa: PLR2004
    msg = f"Helply requires at least version 2 of {installed_wrapper}"
    raise RuntimeError(msg)


__all__ = (
    "Bot",
    "CommandHandler",
    "Permissions",
    "Guild",
    "Locale",
    "Color",
    "Embed",
    "Role",
)
