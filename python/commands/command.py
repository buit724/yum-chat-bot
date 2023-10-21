import abc
from typing import Awaitable

from twitchAPI.chat import ChatCommand


class Command:
    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this command
        :return: The name of this command
        """
        pass

    @abc.abstractmethod
    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Process the command sent
        :return: The ChatCommand object with the command arguments
        """
        pass
