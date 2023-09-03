"""
Embeds module adds some pre-configured embeds to streamline the creation of your help command
"""
from typing import List, Optional

import disnake

from ..help import AppCommandHelp
from ..types import AppCommand, SlashCommand, UserCommand

MAX_CHARS_PER_FIELD = 1024
"""
Set the max and default character limit per embed field.

This is a Discord limitation, so we use this for chunking command
description lines for the overview embed(s) which allow us to split
into multiple fields within a single embed.

Notes
-----
I do not recommend exceeding 400 characters as this can create very tall embeds.
"""
MAX_FIELDS_PER_EMBED = 25
"""
Set the max and default field per embed.

Discord limits this to 25, so that's what has been set as the max here
as well.
"""


def command_detail_embed(
    command: AppCommand,
    *,
    thumbnail: Optional[disnake.File] = None,
    guild: Optional[disnake.Guild] = None,
    color: Optional[disnake.Color] = None,
) -> disnake.Embed:
    """Create and return an embed showing command details.

    Parameters
    ----------
    command: AppCommand
        The `AppCommand` retrieved from `AppCommandHelp.get_command_named`
    thumbnail: disnake.File, optional
        A `disnake.File` converted image to be set as the embed thumbnail.
    guild: disnake.Guild, optional
        Guild where this embed will be displayed. Used to convert
        any role checks into role objects
    color: disnake.Color, optional
        Set the color the embed. Default is None

    Examples
    --------
    ```py
    from disnake.ext.app_command_help import AppCommandHelp, utils

    ...
    app_command_help = AppCommandHelp(bot)

    ...
    command = app_command_help.get_command_named(name)
    embed = utils.command_detail_embed(command, guild=inter.guild)
    await inter.response.send_message(embed=embed)
    ```

    Returns
    -------
    disnake.Embed
        The created embed containing the command details.
    """
    type_ = (
        "Slash Command Details"
        if isinstance(command, SlashCommand)
        else "User Command Details"
        if isinstance(command, UserCommand)
        else "Message Command Details"
    )

    embed = disnake.Embed(description=f"{command.mention}\n{command.description}", color=color)
    embed.set_author(name=f'{type_} {"(NSFW)" if command.nsfw else ""}')
    if thumbnail:
        embed.set_thumbnail(file=thumbnail)

    if command.checks.permissions:
        permissions = ", ".join(command.checks.permissions)
        embed.add_field(name="Required Permissions", value=permissions, inline=True)

    if command.checks.roles:
        if guild:
            roles = AppCommandHelp.roles_from_checks(command.checks, guild)
            role_checks = ", ".join(r.mention for r in roles)
        else:
            role_checks = ", ".join(str(check) for check in command.checks.roles)

        roles_as_string = f"**Required Roles**:\n{role_checks}"
        embed.add_field(name="Required Role(s)", value=roles_as_string, inline=True)

    if isinstance(command, SlashCommand):
        embed.set_footer(text="[ required ] | ( optional )")
        if command.args:
            args = "\n".join(f"**{arg}**: *{arg.description}*" for arg in command.args)
            embed.add_field(name="Parameters", value=args, inline=False)
        else:
            embed.add_field(name="Parameters", value="None", inline=True)

    return embed


def commands_overview_embeds(
    commands: List[AppCommand],
    *,
    thumbnail: Optional[disnake.File] = None,
    max_field_chars: int = MAX_CHARS_PER_FIELD,
    max_fields: int = MAX_FIELDS_PER_EMBED,
    color: Optional[disnake.Color] = None,
) -> List[disnake.Embed]:
    """Create and return one or more embeds containing all commands and descriptions.

    Parameters
    ----------
    commands: List[AppCommand]
        List of `AppCommand` received from `AppCommandHelp.get_all_commands`
    thumbnail: disnake.File, optional
        A `disnake.File` converted image to be set as the embed thumbnail.
    max_field_chars: int
        Max number of characters per embed field description, default is MAX_CHARS_PER_FIELD (1024)
    max_fields: int
        Max number of fields per embed. default is MAX_FIELDS_PER_EMBED (10)
    color: disnake.Color, optional
        Set the color the embed(s). Default is None
    Examples
    --------
    ```py
    from disnake.ext.app_command_help import AppCommandHelp, utils

    ...
    app_command_help = AppCommandHelp(bot)

    ...
    commands = app_command_help.get_all_commands(inter.guild)
    embeds = utils.commands_overview_embeds()
    await inter.response.send_message(embeds=embeds)
    ```

    Returns
    ------
    List[disnake.Embed]
        A list of disnake.Embed containing an overview of the commands.
    """

    if max_field_chars > MAX_CHARS_PER_FIELD:
        max_field_chars = MAX_CHARS_PER_FIELD

    if max_fields > MAX_FIELDS_PER_EMBED:
        max_fields = MAX_FIELDS_PER_EMBED

    embeds: List[disnake.Embed] = []
    current_embed: Optional[disnake.Embed] = None
    current_field: str = ""
    current_field_chars: int = 0

    for command in commands:
        command_type = (
            "Slash Command"
            if isinstance(command, SlashCommand)
            else "User Command"
            if isinstance(command, UserCommand)
            else "Message Command"
        )

        nsfw = "*(NSFW)*" if command.nsfw else ""

        command_lines = (
            f"{command.mention} *({command_type})* {nsfw}\n" f"{command.description}\n\n"
        )

        if current_embed is None:
            title = "Commands Overview" if not embeds else "Commands Overview (continued)"
            current_embed = _create_base_embed(title, color, thumbnail)
            current_field_chars = 0

        if current_field_chars + len(command_lines) <= max_field_chars:
            current_field += command_lines
            current_field_chars += len(command_lines)
        else:
            current_embed.add_field(name="\u200b", value=current_field, inline=False)
            current_field = command_lines
            current_field_chars = len(command_lines)

        if len(current_embed.fields) >= max_fields:
            embeds.append(current_embed)
            current_embed = None

    if current_embed is not None:
        current_embed.add_field(name="\u200b", value=current_field, inline=False)
        embeds.append(current_embed)

    return embeds


def _create_base_embed(
    title: str, color: Optional[disnake.Color] = None, thumbnail: Optional[disnake.File] = None
) -> disnake.Embed:
    embed = disnake.Embed(title=title, color=color)
    if thumbnail:
        embed.set_thumbnail(file=thumbnail)
    return embed
