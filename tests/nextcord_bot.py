import os
from discord import Interaction
import nextcord
from nextcord.ext import commands, application_checks
from dotenv import load_dotenv

from helply.helply import Helply
from helply.utils import command_detail_embed


load_dotenv()


bot = commands.Bot(intents=nextcord.Intents.all())
helply = Helply(bot)


async def send(inter):
    await inter.response.send_message("Testing", ephemeral=True, delete_after=2)


@commands.cooldown(1, 20)
@application_checks.has_permissions(kick_members=True)
@bot.slash_command(name="test")
async def test(inter: nextcord.Interaction, user: str, another: int = None):
    command = helply._handler._get_command_named("test")
    embeds = command_detail_embed(command, guild=inter.guild)

    await inter.response.send_message(embed=embeds)


class Cog(commands.Cog):
    async def cog_application_command_check(self, interaction: nextcord.Interaction) -> bool:
        return True

    @application_checks.has_role(1215678837199741009)
    @nextcord.slash_command(
        name="parent",
    )
    async def parent(self, inter):
        ...

    @application_checks.has_any_role(123)
    @parent.subcommand(name="child")
    async def parent_child(self, inter):
        ...

    @parent_child.subcommand(name="grandchild")
    @application_checks.has_role(1215678837199741009)
    async def grandchild(self, inter):
        await send(inter)


bot.add_cog(Cog())
bot.run(os.getenv("TOKEN"))
