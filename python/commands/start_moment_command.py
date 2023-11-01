from typing import List, Union

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import StreamerOnly, BaseCommandMiddleware
from twitchAPI.object.api import ChannelInformation
from twitchAPI.twitch import Twitch

import python.utils.time_utils as time_utils
from python.commands.command import Command
from datetime import datetime, timedelta

from python.models.game import Game
from python.models.moment import Moment
from python.repositories.repository_provider import RepositoryProvider
from python.state.global_state import GlobalState


class StartMomentCommand(Command):

    def __init__(self, global_state: GlobalState, repository_provider: RepositoryProvider, scheduler: AsyncIOScheduler,
                 twitch: Twitch, duration: int, broadcaster_id: str, moderator_id: str, command_prefix: str,
                 claim_moment_cmd_name: str, edit_moment_name_cmd_name: str, edit_moment_description_cmd_name: str,
                 cancel_moment_cmd_name: str):
        self.global_state: GlobalState = global_state
        self.repository_provider: RepositoryProvider = repository_provider
        self.scheduler: AsyncIOScheduler = scheduler
        self.twitch: Twitch = twitch
        self.duration = duration
        self.broadcaster_id: str = broadcaster_id
        self.moderator_id: str = moderator_id
        self.command_prefix: str = command_prefix
        self.claim_moment_cmd_name = claim_moment_cmd_name
        self.edit_moment_name_cmd_name: str = edit_moment_name_cmd_name
        self.edit_moment_description_cmd_name: str = edit_moment_description_cmd_name
        self.cancel_moment_cmd_name = cancel_moment_cmd_name

    def get_name(self) -> str:
        """
        The name of this start moment comment
        :return:
        """
        return "startmoment"

    def get_middleware(self) -> Union[List[BaseCommandMiddleware], None]:
        """
        Only the streamer can use this command
        :return: The streamer only middleware
        """
        return [StreamerOnly()]

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Enable moment to be claimed by users, no arguments needed
        :param cmd: The give moment command
        :return:
        """
        # Checking for name
        name: str = cmd.parameter.strip()
        if len(name) == 0:
            await cmd.reply("Please provide a name for this moment")
            return

        # Checking for moment
        if self.global_state.current_moment is not None:
            await cmd.reply("There is currently a moment going on. Please wait for the current moment to end")
            return

        # Start the moment
        channel_info: ChannelInformation = (await self.twitch.get_channel_information(self.broadcaster_id))[0]
        start_time: datetime = datetime.now()
        end_time: datetime = start_time + timedelta(minutes=self.duration)
        print(channel_info.game_id)
        game: Game = self.repository_provider.game_repository.find_game(int(channel_info.game_id),
                                                                        channel_info.game_name)
        moment: Moment = self.repository_provider.moment_repository.add_moment(Moment(name, game.id, start_time,
                                                                                      end_time))
        self.global_state.start_moment(moment)

        # Alert viewers that a moment has been started
        msg: str = (f'The "{moment.name}" moment has been started for the game "{channel_info.game_name}". '
                    f'It can be claimed by typing {self.command_prefix}{self.claim_moment_cmd_name} '
                    f'within the next {self.duration} minutes '
                    f'(until {time_utils.format_datetime_tz_unaware(moment.end_time)})')
        await self.twitch.send_chat_announcement(self.broadcaster_id, self.moderator_id, msg, "blue")

        # Schedule the time when the moment will end
        self.scheduler.add_job(self.turn_off_moment, next_run_time=moment.end_time)

        # Alert streamer with the option to edit name or description
        await cmd.chat.send_message(cmd.room,
                                    f"@{cmd.user.display_name} You can edit this moment's description with "
                                    f"{self.command_prefix}{self.edit_moment_description_cmd_name}, "
                                    f"change the name with {self.command_prefix}{self.edit_moment_name_cmd_name}, "
                                    f"or cancel the moment with {self.command_prefix}{self.cancel_moment_cmd_name}")

    async def turn_off_moment(self) -> None:
        """
        Turn off moment so it is no longer claimable. Send a message to the channel about who got the moment
        :return: None
        """
        # Send a message to show who have gotten the moment
        users_msg: str = ", ".join([f'@{x.display_name}' for x in self.global_state.claimed_users])
        await self.twitch.send_chat_announcement(self.broadcaster_id, self.moderator_id,
                                                 f'Moment has ended. The following users have claimed the '
                                                 f'moment: {users_msg}',
                                                 "blue")

        # End the moment
        self.global_state.end_moment()
