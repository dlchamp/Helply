import typing

__all__ = ("CommandChecks",)


class CommandChecks(typing.NamedTuple):
    """Wrap the command's permission or role requirements.

    Attributes
    ----------
    permissions : List[str]
        A list of permission names required to use this command.
    roles : List[Union[str, int]]
        A list of role names or role IDs required to use this command.
    """

    permissions: typing.List[str]
    roles: typing.List[typing.Union[str, int]]
