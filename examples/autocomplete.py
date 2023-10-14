"""A very basic autocomplete example for commands and categories"""


import os
from typing import List, Optional, Union

import disnake
from disnake.ext import commands

from helply import Helply, utils

bot = commands.InteractionBot()

# construct the helper class with the bot and sequence of commands to ignore
helply = Helply(bot, commands_to_ignore=("help",))


...
"""some commands"""
...


@bot.slash_command(name="help")
async def help_command(
    inter: disnake.ApplicationCommandInteraction,
    command: Optional[str] = None,
    category: Optional[str] = None,
):
    ...


@help_command.autocomplete("command")
async def help_command_autocomplete(
    inter: disnake.ApplicationCommandInteraction, command: str
) -> List[str]:
    command = command.casefold()

    commands = helply.get_commands()
    return [c.name for c in commands if command in c.name.casefold()][:25]


@help_command.autocomplete("category")
async def help_category_autocomplete(
    inter: disnake.ApplicationCommandInteraction, category: str
) -> List[str]:
    category = category.casefold()

    categories = helply.get_categories()
    return [c for c in categories if category in c.casefold()][:25]
