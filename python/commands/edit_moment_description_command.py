from typing import Union

from twitchAPI.chat import ChatCommand

from python.commands.command import Command
from python.models.moment import Moment
from python.repositories.repository_provider import RepositoryProvider
from python.state.global_state import GlobalState


class EditMomentDescriptionCommand(Command):

    def __init__(self, global_state: GlobalState, repository_provider: RepositoryProvider):
        self.global_state = global_state
        self.repository_provider = repository_provider

    def get_name(self) -> str:
        """
        Get the name of this edit moment description command
        :return: The name of this edit moment description command
        """
        return "editmomentdesc"

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Edit the current moment description
        :param cmd: The edit moment description command
        :return: NONE
        """
        # Checking for name
        description: str = cmd.parameter.strip()
        if len(description) == 0:
            await cmd.reply("Please provide a description for this moment")
            return

        # Checking for moment
        current_moment: Union[Moment, None] = self.global_state.current_moment
        if self.global_state.current_moment is None:
            await cmd.reply("There is no moment going on at the moment")
            return

        # Update moment name
        current_moment.description = description
        self.repository_provider.moment_repository.update_moment(current_moment)
        await cmd.reply(f'You have successfully changed the description of this moment to "{description}"')
