"""A basic example of using Helply"""

import os
from typing import Optional, Union

import disnake
from disnake.ext import commands

from helply import Helply, utils

bot = commands.InteractionBot()

# construct the helper class with the bot and sequence of commands to ignore
helply = Helply(bot, commands_to_ignore=("help",))


@bot.slash_command(name="kick")
@commands.default_member_permissions(kick_members=True)
async def kick_member(
    inter: disnake.GuildCommandInteraction,
    member: disnake.Member,
    reason: Optional[str] = None,
) -> None:
    """Kick a member from the server

    Parameters
    ----------
    member: Select a member to kick
    """
    try:
        await member.kick(reason=reason)

    except disnake.Forbidden as e:
        await inter.response.send_message(f"Unable to kick {member.mention} - {e}", ephemeral=True)
        return

    await inter.response.send_message(
        f"{member} was kicked by {inter.author}. Reason: {reason}", ephemeral=True
    )


@bot.user_command(name="View Avatar", extras={"help": "Display user's avatar"})
async def user_avatar(
    inter: disnake.UserCommandInteraction, user: Union[disnake.User, disnake.Member]
):
    avatar = user.avatar or user.default_avatar
    await inter.response.send_message(avatar.url)


@bot.slash_command(name="help")
async def help_command(inter: disnake.ApplicationCommandInteraction) -> None:
    """Display command the bot's commands."""

    if not inter.guild:
        # since inter.guild is None, the command was called from a DM, so we should only
        # display commands that are available in DM.
        # We also pass the inter.locale so we can access localized variants of the commands,
        # where available
        commands = helply.get_dm_only_commands(locale=inter.locale)

    else:
        # Since the command was executed in a guild, we we to provide the `Member`'s
        # guild permissions as well to prevent any commands normally hidden by
        # `default_member_permissions` from appearing
        commands = helply.get_guild_commands(
            inter.guild_id, permissions=inter.author.guild_permissions, locale=inter.locale
        )

    # since it's possible that there might be 0 commands returned, we would need to handle that scenario
    if not commands:
        await inter.response.send_message("No commands available.", ephemeral=True)
        return

    # Now we use the optional included utility functions to create the embeds and Paginator.
    embeds = utils.commands_overview_embeds(commands)

    # a quick check to see if the Paginator is needed, since the number of embeds returned will
    # depend on how many commands you have and how many field characters, and fields specified.
    if len(embeds) > 1:
        view = utils.Paginator(embeds=embeds)
    else:
        view = disnake.utils.MISSING

    embed = embeds[0]
    await inter.response.send_message(embed=embed, view=view)


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
