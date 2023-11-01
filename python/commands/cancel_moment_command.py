from typing import Union, List

from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import StreamerOnly, BaseCommandMiddleware
from twitchAPI.twitch import Twitch

from python.commands.command import Command
from python.models.moment import Moment
from python.repositories.repository_provider import RepositoryProvider
from python.state.global_state import GlobalState


class CancelMomentCommand(Command):
    def __init__(self, global_state: GlobalState, repository_provider: RepositoryProvider,
                 twitch: Twitch, broadcaster_id: str, moderator_id: str):
        self.global_state = global_state
        self.repository_provider = repository_provider
        self.twitch = twitch
        self.broadcaster_id = broadcaster_id
        self.moderator_id = moderator_id

    def get_name(self) -> str:
        """
        Get the name of cancel moment command
        :return: The name of cancel moment command
        """
        return "cancelmoment"

    def get_middleware(self) -> Union[List[BaseCommandMiddleware], None]:
        """
        Only the streamer can use this command
        :return: The streamer only middleware
        """
        return [StreamerOnly()]

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Cancel the ongoing moment
        :param cmd: The cancel moment command
        :return: None
        """
        # Checking for moment
        current_moment: Union[Moment, None] = self.global_state.current_moment
        if self.global_state.current_moment is None:
            await cmd.reply("There is no moment going on at the moment")
            return

        # Delete moment and send alert to chat
        self.repository_provider.moment_repository.delete_moment(current_moment)
        self.global_state.end_moment()
        msg: str = f'The "{current_moment.name}" moment has been cancelled.'
        await self.twitch.send_chat_announcement(self.broadcaster_id, self.moderator_id, msg, "blue")

