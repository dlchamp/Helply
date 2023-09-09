"""
Provides a basic Paginator to provide a clean interface for users to navigator your
multiple embeds.

!!! Note
    This can be used for pretty much any list of
    [disnake.Embed](https://docs.disnake.dev/en/latest/api/messages.html#disnake.Embed)
"""
from __future__ import annotations

from typing import List, Optional

import disnake


class Paginator(disnake.ui.View):
    """Provides a basic paginator View that allows users to navigate over multiple embeds.

    Inspired by the paginator.py example provided by
    [disnake](https://github.com/DisnakeDev/disnake/blob/stable/examples/views/button/paginator.py)

    Attributes
    ----------
    message: disnake.InteractionMessage
        The interaction message associated with this Paginator.
        Only useful if a timeout has been provided and the original response will need to be
        edited.

    Parameters
    ----------
    embeds: List[disnake.Embed]
        List of embeds that will be cycled through
    user: disnake.User, optional
        Include a user to prevent others from using buttons.
    timeout: float
        Set the timeout in seconds.
    """

    message: disnake.InteractionMessage

    def __init__(
        self,
        *,
        embeds: List[disnake.Embed],
        user: Optional[disnake.Member] = None,
        timeout: float = 180.0,
    ) -> None:
        super().__init__(timeout=timeout)
        self.user: Optional[disnake.Member] = user
        self.embeds: List[disnake.Embed] = embeds
        self.index: int = 0

        self._update_state()

    async def on_timeout(self) -> None:
        """Call when Paginator has timed out.

        Requires a Paginator.message to be set and timeout to not be `None`

        Example
        --------
        ```py
        view = utils.Paginator(embeds=embeds, timeout=300)
        await inter.response.send_message(view=view)
        view.message = await inter.original_response()
        ```
        """
        if message := getattr(self, "message", None):
            try:
                await message.edit(view=None)
            except disnake.NotFound:
                # message may have already been deleted
                pass

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        """Check if interaction.author is allowed to interact.

        If no member is provided to Paginator, this check always returns True

        Parameters
        ----------
        interaction: disnake.MessageInteraction
            The interaction invoked by a button

        Returns
        -------
        bool
            True if the interaction check passes and the button callback should be invoked,
            else False and the callback will not be invoked.
        """
        if self.user and self.user.id != interaction.author.id:
            await interaction.response.send_message(
                "You do not have permission to interact with this button.", ephemeral=True
            )
            return False

        return True

    def _update_state(self) -> None:
        """
        Update the "state" of the view.

        Enable/disable navigation buttons and update the disable counter component
        """
        self._page_counter.label = f"{self.index + 1} / {len(self.embeds)}"
        self._first_page.disabled = self._prev_page.disabled = self.index == 0
        self._last_page.disabled = self._next_page.disabled = self.index == len(self.embeds) - 1

    @disnake.ui.button(label="First Page", style=disnake.ButtonStyle.primary)
    async def _first_page(
        self, _: disnake.ui.Button[Paginator], inter: disnake.MessageInteraction
    ) -> None:
        """Jump to the first embed."""
        self.index = 0
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(label="Prev Page", style=disnake.ButtonStyle.primary)
    async def _prev_page(
        self, _: disnake.ui.Button[Paginator], inter: disnake.MessageInteraction
    ) -> None:
        """Go back one page."""
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(label="", style=disnake.ButtonStyle.primary, disabled=True)
    async def _page_counter(
        self, _: disnake.ui.Button[Paginator], inter: disnake.MessageInteraction
    ) -> None:
        """Just a page counter and cannot be interacted with."""

    @disnake.ui.button(label="Next Page", style=disnake.ButtonStyle.primary)
    async def _next_page(
        self, _: disnake.ui.Button[Paginator], inter: disnake.MessageInteraction
    ) -> None:
        """Go to next page."""
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(label="Last Page", style=disnake.ButtonStyle.primary)
    async def _last_page(
        self, _: disnake.ui.Button[Paginator], inter: disnake.MessageInteraction
    ) -> None:
        """Go to last page."""
        self.index = len(self.embeds) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)
