"""Helpy utilities."""
from __future__ import annotations

from operator import attrgetter
from typing import TYPE_CHECKING, Any, Callable, Iterable, List, Optional, TypeVar

if TYPE_CHECKING:
    from ..__wrappers import wrapper
    from ..types import CommandChecks

T = TypeVar("T")

__all__ = ("roles_from_checks",)


def _parse_docstring(func: Optional[Callable]) -> str:  # type: ignore[reportUnusedFunction]
    """Parse the first line of the docstring from the given callable.

    This function extracts the first line of the docstring, up until the first newline character.
    If the function does not have a docstring, it returns an empty string.

    Parameters
    ----------
    func: `Optional[Callable[..., Any]]`
        Callable from which to parse the docstring.


    Returns
    -------
    `str`
        The first line of the docstring or an empty string if no docstring is present.
    """
    if func is None or func.__doc__ is None:
        return ""

    docstring = func.__doc__
    return docstring.strip().split("\n", 1)[0]


def get(iterable: Iterable[T], **attrs: Any) -> Optional[T]:  # type: ignore[reportUnusedFunction]
    """Thanks disnake ;)"""
    _all = all
    attrget = attrgetter

    # Special case the single element call
    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace("__", "."))
        for elem in iterable:
            if pred(elem) == v:
                return elem
        return None

    converted = [(attrget(attr.replace("__", ".")), value) for attr, value in attrs.items()]

    for elem in iterable:
        if _all(pred(elem) == value for pred, value in converted):
            return elem
    return None


def roles_from_checks(checks: CommandChecks, guild: wrapper.Guild) -> List[wrapper.Role]:
    """Parse the command's role checks and return a list of `Role`.

    Parameters
    ----------
    checks : CommandChecks
        A command's checks
    guild: Guild
        An instance of Guild from the installed wrapper.

    Returns
    -------
    List[Role]
        `Roles` that have been successfully converted from name or ID.
    """
    role_checks = checks.roles
    roles: List[Any] = []

    for name_or_id in role_checks:
        if isinstance(name_or_id, int) or name_or_id.isdigit():
            role = guild.get_role(int(name_or_id))
        else:
            role = get(guild.roles, name=name_or_id)

        if role:
            roles.append(role)

    return roles
