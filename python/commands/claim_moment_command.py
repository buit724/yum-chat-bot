from twitchAPI.chat import ChatCommand

from python.commands.command import Command
from python.models.user import User
from python.state.global_state import GlobalState


class ClaimMomentCommand(Command):

    def __init__(self, global_state: GlobalState, channel: str):
        self.global_state = global_state
        self.channel: str = channel

    def get_name(self) -> str:
        """
        Get the name of claim moment command
        :return: The name of claim moment command
        """
        return "claimmoment"

    async def process_command(self, cmd: ChatCommand):
        """
        Clime the ongoing moment for this user
        :param cmd: The give moment command
        :return: NONE
        """
        # No moment going on at the moment
        if self.global_state.current_moment is None:
            await cmd.reply("There is no moment that can be claimed at this time")
            return

        user: User = User(int(cmd.user.id), cmd.user.display_name)

        # User already claimed this moment
        if not self.global_state.add_claimed_user(user):
            await cmd.reply("Error - You have already claimed this moment")
            return

        print(f"User {user.display_name} with id {user.id} has claimed the moment")
        await cmd.reply("You have claimed this moment")
    