from typing import List


class HelplyException(Exception):
    """Base exception for all exceptions raised by Helply."""


class NoSupportedWrappers(HelplyException):
    """Raised if no supported Discord wrappers are found."""

    def __init__(self) -> None:
        super().__init__(
            "No supported Discord libraries were found. Please install one of the following: "
            "disnake, discord.py, nextcord, py-cord"
        )


class MultipleSupportedWrappers(HelplyException):
    """Raised if more than one supported Discord wrapper is found."""

    def __init__(self, wrappers: List[str]) -> None:
        super().__init__(
            f'Multiple supported Discord wrappers were found: {", ".join(wrappers)}. '
            "Please uninstall all extras."
        )


class UnsupportedCommandType(HelplyException):
    """Raise if somehow a non supported ApplicationCommand is provided."""

    def __init__(self, command: object) -> None:
        msg = f"{command.__class__.__name__} is an unsupported application command type."
        super().__init__(msg)
