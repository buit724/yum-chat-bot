from typing import Union, List

from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import BaseCommandMiddleware
from python.commands.command import Command
from python.models.moment import Moment
from python.models.user import User
from python.repositories.repository_provider import RepositoryProvider
from python.state.global_state import GlobalState


class ClaimMomentCommand(Command):
    def __init__(self, global_state: GlobalState, repository_provider: RepositoryProvider):
        self.global_state = global_state
        self.repository_provider = repository_provider

    def get_name(self) -> str:
        """
        Get the name of claim moment command
        :return: The name of claim moment command
        """
        return "claimmoment"

    def get_middleware(self) -> Union[List[BaseCommandMiddleware], None]:
        """
        Everybody can use this command
        :return: None
        """
        return None

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Claim the ongoing moment for this user
        :param cmd: The give moment command
        :return: NONE
        """
        # No moment going on at the moment
        current_moment: Union[Moment, None] = self.global_state.current_moment
        if self.global_state.current_moment is None:
            await cmd.reply("There is no moment that can be claimed at this time")
            return

        # Get user object
        user: User = self.repository_provider.user_repository.find_user(int(cmd.user.id), cmd.user.display_name)

        # User already claimed this moment
        if not self.global_state.add_claimed_user(user):
            await cmd.reply("Error - You have already claimed this moment")
            return

        # Claim the moment for this user
        self.repository_provider.user_moment_assoc_repository.assoc_user_moment(user, current_moment)
        print(f"User {user.display_name} with id {user.id} has claimed the moment")
        await cmd.reply("You have successfully claimed this moment")
