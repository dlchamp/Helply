Here are some examples using autocompletion with your created `/help` command

All examples on this page assume you have the helper class and a help command defined like so:
```py
from helply import Helply


helper = Helply(bot)

...
...

@bot.slash_command(name='help')
async def help_command(inter: disnake.GuildCommandInteraction, name: Optional[str] = None)
```


### Autocomplete example using command names
This will construct a list of command names available to the user based on their guild_permissions.
We then return that list if the name matches what's been inputted into name argument, and we
slice the return to return no more than 25 items.

```py
@help_command.autocomplete('name')
async def helper_command_name(
    inter: disnake.GuildCommandInteraction, name: str
) -> List[str]:


    name = name.casefold()

    commands = helply.get_all_commands(
        inter.guild.id, permissions=inter.author.guild_permissions
    )

    return [c.name for c in commands if name in c.name.casefold()][:25]
```


### Autocomplete example using command names and IDs
Defining an autocomplete in this fashion will display the command name to the user, however
the bot will receive the command's ID as a string.  So it will need to be cast to an int before
being passed to the `help.get_command(ID) method.

```py
@help_command.autocomplete('name')
async def helper_command_name(
    inter: disnake.GuildCommandInteraction, name: str
) -> Dict[str, str]:

    name = name.casefold()

    commands = helply.get_all_commands(
        inter.guild.id, permissions=inter.author.guild_permissions
    )

    return {c.name: str(c.id) for c in commands if name in c.name.casefold()}
```


### Autocomplete for categories
You may also want to display all commands available within a specific category or cog.
Heres an example of what that might look like.

```py
@help_command.autocomplete('category')
async def helper_command_name(
    inter: disnake.GuildCommandInteraction, category: str)
 -> List[str]:
    category = category.casefold()

    categories = helper.get_categories(
        inter.guild.id, permissions=inter.author.guild_permissions
    )

    return [cat for cat in categories if category in cat.casefold()][:25]
```
