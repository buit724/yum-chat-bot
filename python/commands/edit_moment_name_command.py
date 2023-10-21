from typing import Union

from twitchAPI.chat import ChatCommand

from python.commands.command import Command
from python.models.moment import Moment
from python.repositories.repository_provider import RepositoryProvider
from python.state.global_state import GlobalState


class EditMomentNameCommand(Command):

    def __init__(self, global_state: GlobalState, repository_provider: RepositoryProvider):
        self.global_state = global_state
        self.repository_provider = repository_provider

    def get_name(self) -> str:
        """
        Get the name of this edit moment name command
        :return: The name of this edit moment name command
        """
        return "editmomentname"

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Edit the current moment name
        :param cmd: The edit moment name command
        :return: NONE
        """
        # Checking for name
        name: str = cmd.parameter.strip()
        if len(name) == 0:
            await cmd.reply("Please provide a name for this moment")
            return

        # Checking for moment
        current_moment: Union[Moment, None] = self.global_state.current_moment
        if self.global_state.current_moment is None:
            await cmd.reply("There is no moment going on at the moment")
            return

        # Update moment name
        current_moment.name = name
        self.repository_provider.moment_repository.update_moment(current_moment)
        await cmd.reply(f'You have successfully changed the name of this moment to "{name}"')
