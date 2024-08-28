from typing import List, Tuple, Dict, Union, TYPE_CHECKING
import os
from helply import errors

from pkg_resources import get_distribution, DistributionNotFound

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
    from disnake import version_info
    from disnake.ext.commands import Bot
    from .handlers.disnake_handler import DisnakeCommandHandler as CommandHandler
    from disnake import Permissions, Guild, Locale

else:
    from nextcord import version_info
    from .handlers.nextcord_handler import NextcordCommandHandler as CommandHandler
    from nextcord.ext.commands import Bot
    from nextcord import Permissions, Guild, Locale


if version_info.major < 2:
    raise RuntimeError(f"Helply requires at least version 2 of {installed_wrapper}.")


__all__ = (
    "Bot",
    "CommandHandler",
    "Permissions",
    "Guild",
    "Locale",
)
