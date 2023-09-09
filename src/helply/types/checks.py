"""Checks and Cooldowns used with Helply attributes"""
from typing import List, NamedTuple, Union

__all__ = (
    "CommandChecks",
    "Cooldown",
)


class CommandChecks(NamedTuple):
    """Wrap the command's permission or role requirements.

    Attributes
    ----------
    permissions : List[str]
        A list of permission names required to use this command.
    roles : List[Union[str, int]]
        A list of role names or role IDs required to use this command.
    """

    permissions: List[str]
    roles: List[Union[str, int]]


class Cooldown(NamedTuple):
    """Represents a commands.Cooldown.

    (*New in version: 0.4.0*)

    Attributes
    ----------
    rate: int
        Number of times the command can be used before triggering a cooldown
    per: float
        Amount of seconds to wait for a cooldown when it's been triggered
    type: str
        Type of cooldown



    ```
    |--------------------------------------------------------------------|
    |   Types    |                   Description                         |
    |------------|-------------------------------------------------------|
    | `default`  | The default bucket operates on a global basis.        |
    | `user`     | The user bucket operates on a per-user basis.         |
    | `guild`    | The guild bucket operates on a per-guild basis.       |
    | `channel`  | The channel bucket operates on a per-channel basis.   |
    | `member`   | The member bucket operates on a per-member basis.     |
    | `category` | The category bucket operates on a per-category basis. |
    | `role`     | The role bucket operates on a per-role basis.         |
    |--------------------------------------------------------------------|
    ```
    """

    rate: int
    per: float
    type: str
