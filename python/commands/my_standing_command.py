from typing import Union, List

from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import BaseCommandMiddleware

from python.commands.command import Command
from python.models.user import User
from python.repositories.repository_provider import RepositoryProvider


class MyStandingCommand(Command):
    def __init__(self, repository_provider: RepositoryProvider):
        self.repository_provider = repository_provider

    def get_name(self) -> str:
        """
        Get the name of standing command
        :return: The name of standing command
        """
        return "mystanding"

    def get_middleware(self) -> Union[List[BaseCommandMiddleware], None]:
        """
        Everybody can use this command
        :return: None
        """
        return None

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Get the current top 10 user with the most moments
        :param cmd: The standing command
        :return:
        """
        # Get the user
        user: User = self.repository_provider.user_repository.find_user(cmd.user.id, cmd.user.display_name)
        all_user_moment_count: List[str, int] = self.repository_provider.user_moment_assoc_repository.user_moment_counts()
        user_moment_count: List[str, int] = [x for x in all_user_moment_count if x[0] == user.display_name]

        # No moment claimed yet
        if len(user_moment_count) == 0:
            await cmd.reply("You have not claimed any moment")

        # Have claimed something
        users_with_more_moments: int = len([x for x in all_user_moment_count if x[1] > user_moment_count[0][1]])
        await cmd.reply(f"You are ranked {users_with_more_moments + 1} with {user_moment_count[0][1]} moments")
