import abc
from typing import List, Union

from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import BaseCommandMiddleware


class Command:
    @abc.abstractmethod
    def get_name(self) -> str:
        """
        Get the name of this command
        :return: The name of this command
        """
        pass

    @abc.abstractmethod
    def get_middleware(self) -> Union[List[BaseCommandMiddleware], None]:
        """
        Returns the middle, default to empty middleware if everybody can use it
        :return:
        """
        pass

    @abc.abstractmethod
    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Process the command sent
        :return: The ChatCommand object with the command arguments
        """
        pass
