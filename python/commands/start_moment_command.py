from typing import Union, Optional, Set

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twitchAPI.chat import ChatCommand
from twitchAPI.object.api import ChannelInformation
from twitchAPI.twitch import Twitch

import python.utils.time_utils as time_utils
from python.commands.command import Command
from datetime import datetime, timedelta


class StartMomentCommand(Command):
    CLAIMABLE_DURATION_MIN = 3

    def __init__(self, twitch: Twitch, channel: str, broadcaster_id: str, moderator_id: str,
                 scheduler: AsyncIOScheduler):
        self.twitch: Twitch = twitch
        self.channel: str = channel
        self.broadcaster_id: str = broadcaster_id
        self.moderator_id = moderator_id
        self.scheduler: AsyncIOScheduler = scheduler
        self.moment_claimable: bool = False
        self.moment_claim_end_time: Union[datetime, Optional] = None
        self.claimed_users: Set[str] = set()

    def get_name(self) -> str:
        """
        The name of this start moment comment
        :return:
        """
        return "startmoment"

    async def process_command(self, cmd: ChatCommand):
        """
        Enable moment to be claimed by users, no arguments needed
        :param cmd: The give moment command
        :return:
        """
        if self.moment_claimable:
            await cmd.reply("There is currently a moment going on. Please wait for the current moment to end")
            return

        # Reset variables
        self.moment_claimable = True
        self.moment_claim_end_time = datetime.now() + timedelta(minutes=self.CLAIMABLE_DURATION_MIN)
        self.claimed_users = set()

        channel_info: ChannelInformation = (await self.twitch.get_channel_information(self.broadcaster_id))[0]
        msg: str = (f'A moment has been started for the game "{channel_info.game_name}". It can be claimed by typing '
                    f'!yumcm within the next {self.CLAIMABLE_DURATION_MIN} minutes (until {time_utils.format_datetime_tz_unaware(self.moment_claim_end_time)})')
        await self.twitch.send_chat_announcement(self.broadcaster_id, self.moderator_id, msg, "blue")

        self.scheduler.add_job(self.turn_off_moment, next_run_time=self.moment_claim_end_time)

    async def turn_off_moment(self) -> None:
        """
        Turn off moment so it is no longer claimable. Send a message to the channel about who got the moment
        :return: None
        """
        self.moment_claimable = False
        users_msg: str = ", ".join([f'@{x}' for x in self.claimed_users])
        await self.twitch.send_chat_announcement(self.broadcaster_id, self.moderator_id,
                                                 f'Moment has ended. The following users have claimed the '
                                                 f'moment: {users_msg}',
                                                 "blue")

    def add_user(self, user: str) -> bool:
        """
        Add user to the list of claimed user
        :param user:    The user to add
        :return: True - the user was added. False - if the user is already in the list
        """
        if user in self.claimed_users:
            return False

        self.claimed_users.add(user)
        return True

    def is_moment_currently_going(self):
        """
        Check if there is currently a moment going on
        :return:    Whether there is a moment going on
        """
        return self.moment_claimable
