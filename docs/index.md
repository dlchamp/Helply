A user-friendly Python library designed to streamline the creation of "help" commands for
Discord bots using application commands within the disnake library. This library will automatically parse your commands
and provide details for each command, such as name, description, role and permission checks, etc.

!!! Disclaimer
    This library is not officially associated with the [disnake](https://github.com/DisnakeDev/disnake) project or any of its maintainers. It is an independent creation by a user of the Disnake library who wanted to streamline the process of creating `/help` commands without needing to
    rewrite the implementation each time.


## Installation

To install the `disnake-app-command-help` package, you will need git. If you don't have git installed on your system, you can download it from [here](https://git-scm.com/downloads).

Once you have git installed, run the following command inside your Python environment to install the package:

```
pip install git+https://github.com/dlchamp/disnake-app-command-help
```

## Usage

After installing the package, you can use it in your project by importing it as follows:

```python
from disnake_app_command_help import AppCommandHelp
```

## Custom Descriptions
The `disnake-app-command-help` extension enables you to provide custom descriptions for your command's help information using the `extras` feature. By utilizing the `extras` dictionary and assigning the description as the value to the "help" key, you can offer distinct and informative details separate from the main `description` provided to users when using the command.

!!! Note
    If a slash command already has a description set, extras are not required. However, you can use extras to provide additional helpful information beyond the 100 character limit. For user and message commands without inherent descriptions, you can use extras to provide the command's help info.

**Example - User Command**:
```python
# Since this is a user command that does not inherently have a description. We are using
# extras to set the description for the help command.
@bot.user_command(name="View Avatar", extras={"help": "Display the target user's avatar"})
async def view_avatar(...):
    ...
```

**Example - Slash Command**:
```python
# In this case, slash commands do have the ability to have a description set.  
# The `description` is what appears in the client when the user calls the command.
# In this case extras is optional, but allows you to provide a custom description
# that will appear when a user views the command's help info.
@bot.slash_command(
    name="kick",
    description="Kick the target member",
    extras={"help": "Removes the target member from the guild"}
)
async def kick_member(...):
    ...
```

This feature proves especially valuable for user and message commands, as they lack a native `description` keyword argument, enabling you to enrich the user experience by providing relevant details about each command.


## Automatic Parsing

This library makes the creation of help commands more convenient by automatically parsing all commands, both global and guild-specific, and extracting essential information such as role and permission requirements, sub-commands, and many other attributes. This ensures that only commands available to a guild are shown when calling from a guild.

### Support for `@commands` Checks

The `disnake-app-command-help` extension also supports parsing of `@commands` style checks. For instance, if you are using `@commands.has_permissions()` to restrict command usage, the extension will recognize and display these permission requirements in the help command.

**Example:**
```python
@bot.slash_command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick_member(inter: disnake.GuildCommandInteraction, member: disnake.Member):
    ...
```

In this example, the help command would display that "Kick Members" is a required permission to use the `/kick` command.

## Examples and Documentation

For more examples and detailed documentation on how to use the `disnake-app-command-help` extension, please visit the following links:

- [Example](https://dlchamp.github.io/disnake-app-command-help/examples/basic/)
- [Docs](https://dlchamp.github.io/disnake-app-command-help/)
