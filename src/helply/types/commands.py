import dataclasses
from typing import TYPE_CHECKING, List, Optional

from disnake import Permissions

from .checks import CommandChecks

if TYPE_CHECKING:
    from .enums import AppCommandType


__all__ = (
    "AppCommand",
    "Argument",
    "SlashCommand",
    "UserCommand",
    "MessageCommand",
)


@dataclasses.dataclass
class Argument:
    """Represents a SlashCommand argument.

    Attributes
    ----------
    name : str
        Name of the argument.
    required : bool
        Indicate if the argument is required.
    description : str
        A brief description of the argument.
    """

    name: str
    required: bool
    description: str

    def __str__(self) -> str:
        """Return the argument as a string.

        Required arguments will have `[]` wrapped around their name,
        while optional arguments will be wrapped with `()`.
        """
        if self.required:
            return f"[{self.name}]"
        return f"({self.name})"


@dataclasses.dataclass
class AppCommand:
    """Represents an AppCommand.

    AppCommands are dataclasses that include various attributes from both
    `.ApplicationCommand` and `.InvokableApplicationCommand`

    Attributes
    ----------
    id : int
        The command's unique identifier.
    name : str
        The name of the command.
    checks : CommandChecks
        The command's permission and role requirements.
    type: AppCommandType
        Type of command
    category: str
        Name of cog or category the command belongs to
    description : str
        A brief description of the command.
    dm_permission : bool
        Whether the command is available in DMs or not.
    nsfw : bool
        Whether the command is NSFW (Not Safe For Work).
    guild_id : int, optional
        The ID of the guild where the command is available.
    default_member_permissions : Permissions, optional
        Default member permissions required to use this command.
    mention : str
        Return the command as a mentionable if slash command, else returns bolded name.
    """

    id: int
    name: str
    checks: CommandChecks
    type: "AppCommandType"
    category: str = "None"
    dm_permission: bool = True
    nsfw: bool = False
    description: str = "-"
    guild_id: Optional[int] = None
    default_member_permissions: Optional[Permissions] = None

    @property
    def mention(self) -> str:
        if isinstance(self, SlashCommand):
            return f"</{self.name}:{self.id}>"
        return f"**{self.name}**"


@dataclasses.dataclass
class SlashCommand(AppCommand):
    """Represents a SlashCommand type AppCommand.

    Attributes
    ----------
    args : List[Argument]
        A list of the command's Arguments, if any.
    """

    args: List[Argument] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class UserCommand(AppCommand):
    """Represents a UserCommand type of AppCommand."""

    ...


@dataclasses.dataclass
class MessageCommand(AppCommand):
    """Represents a MessageCommand type of AppCommand."""

    ...
