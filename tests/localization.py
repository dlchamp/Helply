import os
from typing import Any

import disnake
from disnake import Localized, OptionChoice
from disnake.ext import commands

from helply import Helply, utils

intents = disnake.Intents.default()
bot = commands.InteractionBot()
helply = Helply(bot)


bot.i18n.load(f"{os.path.dirname(__file__)}/locale/")


@bot.slash_command()
async def highscore(
    inter: disnake.CommandInteraction,
    user: disnake.User,
    game: str,
    interval: str = commands.Param(
        choices=[
            OptionChoice(Localized("Last Day", key="CHOICE_DAY"), "day"),
            OptionChoice(Localized("Last Week", key="CHOICE_WEEK"), "week"),
            OptionChoice(Localized("Last Month", key="CHOICE_MONTH"), "month"),
        ]
    ),
):
    """Shows the highscore of the selected user within the specified interval.
    {{ HIGHSCORE_COMMAND }}

    Parameters
    ----------
    user: The user to show data for. {{ HIGHSCORE_USER }}
    game: Which game to check scores in. {{ HIGHSCORE_GAME }}
    interval: The time interval to use. {{ HIGHSCORE_RANGE }}
    """
    db: Any = ...  # a placeholder for an actual database connection
    data = await db.highscores.find(user=user.id, game=game).filter(interval).max()
    await inter.send(f"max: {data}")


@highscore.autocomplete("game")
async def game_autocomp(inter: disnake.CommandInteraction, string: str):
    # this clearly isn't great autocompletion as it autocompletes based on the English name,
    # but for the purposes of this example it'll do
    games = ("Tic-tac-toe", "Chess", "Risk")
    return [
        Localized(game, key=f"GAME_{game.upper()}")
        for game in games
        if string.lower() in game.lower()
    ]


@bot.slash_command(name="help")
async def help_command(
    inter: disnake.ApplicationCommandInteraction,
    _command: str = commands.Param(None, name="command"),
):
    if _command:
        command = helply.get_command(int(_command))

        embed = utils.command_detail_embed(command, locale=disnake.Locale.de)
        await inter.send(embed=embed)
        return

    commands = helply.get_all_commands()
    embeds = utils.commands_overview_embeds(commands, locale=disnake.Locale.de)
    embed = embeds[0]

    await inter.send(embed=embed)


@help_command.autocomplete("command")
async def help_command_autocomplete(inter: disnake.AppCommandInter, command: str) -> dict[str, str]:
    commands = helply.get_all_commands()

    locale = disnake.Locale.de  # inter.locale

    return {
        c.get_localized_name(locale): str(c.id)
        for c in commands
        if command.casefold() in c.get_localized_name(locale).casefold()
    }


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()
    bot.run(os.getenv("TOKEN"))
