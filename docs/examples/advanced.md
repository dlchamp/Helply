This is a full example that implements all features of this project.
Using the below example automatically handles commands being used within the context of a guild
or via direct message to the bot.

```py
from typing import Optional, Tuple

import disnake
from disnake.ext import commands

from helply import Helpy, utils

bot = commands.InteractionBot()

# construct the Helpy instance with the passed in `bot`
helpy = Helply(bot)


@bot.slash_command(name="ping")
async def ping(inter: disnake.ApplicationCommandInteraction):
    """Ping the bot to see its latency"""
    await inter.response.send_message(
        f"Pong! Responded in {(bot.latency * 1000):.2f} ms.",
    )


@bot.slash_command(name="help")
async def help_command(
    inter: disnake.GuildCommandInteraction,
    name: Optional[str] = None,
    category: Optional[str] = None,
):
    """Display help info about this bot's commands.

    Parameters
    ----------
    name: Select an available command to view its details
    category: Select an available category to view its commands.
    """

    if name and category:
        await inter.response.send_message(
            "Please only select a command or a category.", ephemeral=True
        )
        return

    # Since autocomplete for name is a dict[name, str(id)], name in this case
    # will be the str(id), convert it to int and try to find the command.
    if name:
        command = helply.get_command(int(name))
        if command is None:
            await inter.response.send_message(
                "It appears this command is not available.", ephemeral=True
            )
            return

        # use the included helper embeds module to create the detailed
        # view of the command.
        embed = utils.command_detail_embed(command, guild=inter.guild)
        view = disnake.utils.MISSING

    elif category:
        guild_id, dm_only, nsfw, permissions = get_helper_query_attrs(inter)

        commands = helply.get_commands_by_category(
            category, guild_id=guild_id, permissions=permissions, dm_only=dm_only
        )

        if not commands:
            await inter.response.send_message(
                "No commands available in the selected category.", ephemeral=True
            )
            return

        category_embeds = utils.commands_overview_embeds(
            commands, max_fields=3, max_field_chars=100, color=disnake.Color.random()
        )

        if len(category_embeds) > 1:
            view = utils.Paginator(embeds=category_embeds)
        else:
            view = disnake.utils.MISSING

        embed = category_embeds[0]

    else:
        guild_id, dm_only, nsfw, permissions = get_helper_query_attrs(inter)

        commands = helply.get_all_commands(
            guild_id, dm_only=dm_only, include_nsfw=nsfw, permissions=permissions
        )
        if not commands:
            await inter.response.send_message(
                "Could not find any available commands.", ephemeral=True
            )
            return

        command_embeds = utils.commands_overview_embeds(
            commands, max_fields=3, max_field_chars=100, color=disnake.Color.random()
        )

        if len(command_embeds) > 1:
            view = utils.Paginator(embeds=command_embeds)
        else:
            view = disnake.utils.MISSING

        embed = command_embeds[0]

    await inter.response.send_message(embed=embed, view=view)


@help_command.autocomplete("name")
async def autocomplete_command_names(
    inter: disnake.ApplicationCommandInteraction,
    string: str,
):
    string = string.casefold()

    guild_id, dm_only, nsfw, permissions = get_helper_query_attrs(inter)

    commands = helply.get_all_commands(
        guild_id, dm_only=dm_only, include_nsfw=nsfw, permissions=permissions
    )

    return {c.name: str(c.id) for c in commands}


@help_command.autocomplete("category")
async def autocomplete_command_categories(
    inter: disnake.ApplicationCommandInteraction, string: str
):
    string = string.casefold()

    guild_id, dm_only, nsfw, permissions = get_helper_query_attrs(inter)

    categories = helply.get_categories(
        guild_id, dm_only=dm_only, include_nsfw=nsfw, permissions=permissions
    )

    return [cat for cat in categories if string in cat.casefold()]


def get_helper_query_attrs(
    inter: disnake.ApplicationCommandInteraction,
) -> Tuple[Optional[int], bool, bool, Optional[disnake.Permissions]]:
    # command does not originate from within a guild
    if not inter.guild or isinstance(inter.author, disnake.User):
        guild_id = None
        dm_only = True
        nsfw = False
        permissions = None

    else:
        guild_id = inter.guild_id
        dm_only = False
        nsfw = getattr(inter.channel, "nsfw", False)
        permissions = inter.author.guild_permissions

    return guild_id, dm_only, nsfw, permissions


if __name__ == "__main__":
    import os
    bot.run(os.getenv("TOKEN"))
```