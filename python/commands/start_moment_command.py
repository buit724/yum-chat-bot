from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twitchAPI.chat import ChatCommand
from twitchAPI.object.api import ChannelInformation
from twitchAPI.twitch import Twitch

import python.utils.time_utils as time_utils
from python.commands.command import Command
from datetime import datetime, timedelta

from python.models.moment import Moment
from python.state.global_state import GlobalState


class StartMomentCommand(Command):
    CLAIMABLE_DURATION_MIN = 1

    def __init__(self, global_state: GlobalState, twitch: Twitch, channel: str, broadcaster_id: str, moderator_id: str,
                 command_prefix: str, scheduler: AsyncIOScheduler):
        self.global_state = global_state
        self.twitch: Twitch = twitch
        self.channel: str = channel
        self.broadcaster_id: str = broadcaster_id
        self.moderator_id = moderator_id
        self.command_prefix = command_prefix
        self.scheduler: AsyncIOScheduler = scheduler

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
        # Checking for name
        name: str = cmd.parameter.strip()
        if len(name) == 0:
            await cmd.reply("Please provide a name for this moment")
            return

        # Check if a moment is going on
        if self.global_state.current_moment is not None:
            await cmd.reply("There is currently a moment going on. Please wait for the current moment to end")
            return

        # Start the moment
        channel_info: ChannelInformation = (await self.twitch.get_channel_information(self.broadcaster_id))[0]
        start_time: datetime = datetime.now()
        moment: Moment = Moment(name, int(channel_info.game_id), start_time,
                                start_time + timedelta(minutes=self.CLAIMABLE_DURATION_MIN))
        self.global_state.start_moment(moment)

        # Alert user with the option to add a description
        await cmd.chat.send_message(self.broadcaster_id,
                                    f"@{cmd.user.display_name} You can add description to this moment with {self.command_prefix}momentdescription")

        # Alert viewers that a moment has been started
        msg: str = (f'The "{moment.name}" moment has been started for the game "{channel_info.game_name}". '
                    f'It can be claimed by typing !yumcm within the next {self.CLAIMABLE_DURATION_MIN} minutes '
                    f'(until {time_utils.format_datetime_tz_unaware(moment.end_time)})')
        await self.twitch.send_chat_announcement(self.broadcaster_id, self.moderator_id, msg, "blue")

        # Schedule the time when the moment will end
        self.scheduler.add_job(self.turn_off_moment, next_run_time=moment.end_time)

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

