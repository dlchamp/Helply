"""
Provides a basic Paginator to provide a clean interface for users to navigator your
multiple embeds.

!!! Note
    This can be used for pretty much any list of
    [disnake.Embed](https://docs.disnake.dev/en/latest/api/messages.html#disnake.Embed)
"""

from __future__ import annotations

from typing import List, Optional

from ..__wrappers import Bot, wrapper


class Paginator(wrapper.ui.View):
    """Provides a basic paginator View that allows users to navigate over multiple embeds.

    Inspired by the paginator.py example provided by
    [disnake](https://github.com/DisnakeDev/disnake/blob/stable/examples/views/button/paginator.py)

    Attributes
    ----------
    message: InteractionMessage
        The interaction message associated with this Paginator.
        Only useful if a timeout has been provided and the original response will need to be
        edited.

    Parameters
    ----------
    embeds: List[Embed]
        List of embeds that will be cycled through
    user: User, optional
        Include a user to prevent others from using buttons.
    timeout: float
        Set the timeout in seconds.
    """

    message: wrapper.InteractionMessage

    def __init__(
        self,
        *,
        embeds: List[wrapper.Embed],
        user: Optional[wrapper.Member] = None,
        timeout: float = 180.0,
    ) -> None:
        super().__init__(timeout=timeout)
        self.user: Optional[wrapper.Member] = user
        self.embeds: List[wrapper.Embed] = embeds
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
            except wrapper.NotFound:
                # message may have already been deleted
                pass

    async def interaction_check(self, interaction: wrapper.Interaction[Bot]) -> bool:
        """Check if interaction.author is allowed to interact.

        If no member is provided to Paginator, this check always returns True

        Parameters
        ----------
        interaction: wrapper.Interaction[Bot]
            The interaction invoked by a button

        Returns
        -------
        bool
            True if the interaction check passes and the button callback should be invoked,
            else False and the callback will not be invoked.
        """
        if self.user and interaction.user and interaction.user.id != self.user.id:
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

    @wrapper.ui.button(label="First Page", style=wrapper.ButtonStyle.primary)
    async def _first_page(
        self, _: wrapper.ui.Button[Paginator], inter: wrapper.Interaction[Bot]
    ) -> None:
        """Jump to the first embed."""
        self.index = 0
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @wrapper.ui.button(label="Prev Page", style=wrapper.ButtonStyle.primary)
    async def _prev_page(
        self, _: wrapper.ui.Button[Paginator], inter: wrapper.Interaction[Bot]
    ) -> None:
        """Go back one page."""
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @wrapper.ui.button(label="", style=wrapper.ButtonStyle.primary, disabled=True)
    async def _page_counter(
        self, _: wrapper.ui.Button[Paginator], __: wrapper.Interaction[Bot]
    ) -> None:
        """Just a page counter and cannot be interacted with."""

    @wrapper.ui.button(label="Next Page", style=wrapper.ButtonStyle.primary)
    async def _next_page(
        self, _: wrapper.ui.Button[Paginator], inter: wrapper.Interaction[Bot]
    ) -> None:
        """Go to next page."""
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @wrapper.ui.button(label="Last Page", style=wrapper.ButtonStyle.primary)
    async def _last_page(
        self, _: wrapper.ui.Button[Paginator], inter: wrapper.Interaction[Bot]
    ) -> None:
        """Go to last page."""
        self.index = len(self.embeds) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)
