A very simple implementation using only a single command.  This example should work as is
and provides some basic insight into how to use this project.

```py
import os
from typing import Optional

import disnake
from disnake.ext import commands

from helply import Helply, utils

bot = commands.InteractionBot()

# construct the helper class with the bot and sequence of commands to ignore
helply = Helply(bot, commands_to_ignore=("help",))


@bot.slash_command_name(name="kick")
@commands.has_permissions(kick_members=True)
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


@bot.slash_command(name="help")
async def help_command(inter: disnake.GuildCommandInteraction, name: Optional[str] = None) -> None:
    """Display command information

    Parameters
    ----------
    name: Choose a command to view its details.
    """

    if name is None:
        # get all commands available to the command author
        # by passing in the inter.guild_id, we ensure only global commands and any commands
        # available only for this guild are retrieved.
        commands = helply.get_all_commands(
            inter.guild_id, permissions=inter.author.guild_permissions
        )

        # since this takes into consideration the default_member_permissions required to use commands
        # and we passed in the command author's permissions, retrieved commands may be an empty list
        # if they cannot use any commands the bot provides.
        if not commands:
            await inter.response.send_message("There are no commands available.", ephemeral=True)
            return

        # now we use the include embed builder utility to create the embeds.
        # in this instance, since there is only one command, embeds will be a single embed
        embeds = utils.commands_overview_embeds(commands)

        embed = embeds[0]

    else:
        # Since autocomplete does not force a user to make a selection, we will try to get
        # the command by the provided name, however, it could result in `None`, so we handle it.
        command = helply.get_command_named(name)
        if not command:
            await inter.response.send_message("Unable to find that command.", ephemeral=True)
            return

        # Now we again use the embed builder utility for the specific command to view its
        # full details, description, parameters, if any, and required permissions
        embed = utils.command_detail_embed(command)

    await inter.response.send_message(embed=embed)


if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))


```
