from typing import Optional, Tuple

import disnake
from disnake.ext import commands

from helply import Helply, utils

intents = disnake.Intents.default()
bot = commands.InteractionBot()

# Construct the Helply class and pass in the bot instance.
helply = Helply(bot, commands_to_ignore=("help",))


@bot.slash_command(name="ping", extras={"category": "General"})
async def ping(inter: disnake.ApplicationCommandInteraction):
    """Ping the bot to see its latency"""
    await inter.response.send_message(
        f"Pong! Responded in {(bot.latency * 1000):.2f} ms.",
    )


@bot.slash_command(
    name="kick",
    description="Kick the target member",
    extras={"help": "Removes the target member from the guild", "category": "Admin"},
)
@commands.cooldown(1, 1, type=commands.BucketType.member)
async def kick_member(inter: disnake.GuildCommandInteraction, member: disnake.Member):
    """Kick a member from the server

    Parameters
    ----------
    member: Select a member to kick
    """


@bot.slash_command(name="command1", guild_ids=[947543739671412878])
@commands.cooldown(1, 15, commands.BucketType.default)
async def command1(inter):
    """A cool slash command"""


@command1.sub_command_group(name="child")
@commands.cooldown(1, 10, commands.BucketType.user)
async def command_group(inter):
    """A cool slash command's child."""


@command1.sub_command(name="child2")
@commands.cooldown(1, 10, commands.BucketType.user)
async def command_child2(inter):
    """A cool slash command's second child sub command."""


@command_group.sub_command(name="grandchild1")
@commands.cooldown(1, 20, commands.BucketType.channel)
async def command_grandchild1(inter):
    """A cool slash command's grandchild."""


@command_group.sub_command(name="grandchild2")
@commands.cooldown(1, 20, commands.BucketType.channel)
async def command_grandchild2(inter):
    """A cool slash command's grandchild."""


@command_group.sub_command(name="grandchild3")
@commands.cooldown(1, 20, commands.BucketType.channel)
async def command_grandchild3(inter):
    """A cool slash command's grandchild."""


@command_group.sub_command(name="grandchild4")
@commands.cooldown(1, 20, commands.BucketType.channel)
async def command_grandchild4(inter):
    """A cool slash command's grandchild."""


@bot.slash_command(name="command2")
async def command2(inter, arg1: str, arg2: int | None = None):
    """Another command with args

    Parameters
    ----------
    arg1: A string argument
    arg2: An optional int argument
    """


@bot.user_command(name="command3", extras={"help": "A user command with checks"})
@commands.has_guild_permissions(moderate_members=True)
async def command3(inter, user: disnake.Member): ...


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

    # Since command IDs are shared between commands, sub command groups,
    # and sub commands, we can only accurately get them by their fully
    # qualified name
    if name:
        command = helply.get_command_named((name))
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
            commands,
            max_fields=1,
            max_field_chars=25,
            color=disnake.Color.random(),
            category=category,
        )

        if len(category_embeds) > 1:
            view = utils.Paginator(embeds=category_embeds)
        else:
            view = disnake.utils.MISSING

        embed = category_embeds[0]

    else:
        guild_id, dm_only, nsfw, permissions = get_helper_query_attrs(inter)

        commands = helply.get_commands(dm_only=dm_only, include_nsfw=nsfw, permissions=permissions)
        if not commands:
            await inter.response.send_message(
                "Could not find any available commands.", ephemeral=True
            )
            return

        command_embeds = utils.commands_overview_embeds(
            commands,
            max_fields=1,
            max_field_chars=100,
            color=disnake.Color.random(),
            thumbnail=bot.user.avatar.url,
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

    commands = helply.get_commands(
        guild_id, dm_only=dm_only, include_nsfw=nsfw, permissions=permissions
    )

    return [c.name for c in commands if string in c.name.casefold()]


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

    import dotenv

    dotenv.load_dotenv()
    bot.run(os.getenv("TOKEN"))

    # for command in bot.application_commands:
    #     cooldown = command._buckets._cooldown
    #     type_ = command._buckets._type
    #     if not cooldown:
    #         continue

    #     print(type(type_), str(type_))
    #     print(cooldown, type_)
