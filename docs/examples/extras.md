This project also allows you to create some help descriptions for your menu commands
`@bot.user_command`, and `@bot.message_command`.  Since these commands do not inherently have
a description that is parsed, we can simply add their descriptions as `extras`




```py
@bot.user_command(name="User Avatar", extras={"help": "Display a user's avatar"})
async def user_avatar_menu(
    inter: disnake.UserCommandInteraction, user: Union[disnake.User, disnake.Member]
):
    avatar = user.avatar or user.default_avatar
    embed = disnake.Embed().set_image(url=avatar.url)

    await inter.response.send_message(embed=embed)


```



This method can also be used to provide a different description to your slash commands separate
from the description displayed in the user's client allowing you to exceed the 100 character limit
set by Discord.


```py
@bot.slash_command(
    name="example",
    extras={
        "help": (
            "This is a much longer description for the command that would normally "
            "exceed the 100 character limit set by Discord"
        )
    },
)
async def example(inter: disnake.ApplicationCommandInteraction):
    """A shorter description that does not exceed the 100 character limit"""
    ...

)```
