from typing import Union, List

from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import BaseCommandMiddleware

from python.commands.command import Command
from python.repositories.repository_provider import RepositoryProvider


class StandingCommand(Command):
    def __init__(self, repository_provider: RepositoryProvider):
        self.repository_provider = repository_provider

    def get_name(self) -> str:
        """
        Get the name of standing command
        :return: The name of standing command
        """
        return "standing"

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
        # Get the top 10 users with the most moments and send to chat
        top_10_users: List[str, int] = self.repository_provider.user_moment_assoc_repository.user_moment_counts()[:10]

        # Check if anyone has claimed a moment yet
        if len(top_10_users) == 0:
            await cmd.reply("Nobody has claimed a moment yet")
            return

        # Has something to show
        msg: str = ", ".join([f'{x[0]} ({x[1]})' for x in top_10_users])
        await cmd.reply(f'@{cmd.user.display_name} {msg}')
