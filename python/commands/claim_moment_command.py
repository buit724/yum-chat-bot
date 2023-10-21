from twitchAPI.chat import ChatCommand

from python.commands.command import Command
from python.commands.start_moment_command import StartMomentCommand


class ClaimMomentCommand(Command):

    def __init__(self, channel: str, give_moment_command: StartMomentCommand):
        self.channel: str = channel
        self.give_moment_command: StartMomentCommand = give_moment_command

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
        # TODO - might need to do some locking here for multi threading processing
        if not self.give_moment_command.is_moment_currently_going():
            await cmd.reply("There is no moment that can be claimed at this time")
            return

        user: str = cmd.user.name
        user_added: bool = self.give_moment_command.add_user(user)
        if not user_added:
            await cmd.reply("Error - You have already claimed this moment")
            return

        await cmd.reply("You have claimed this moment")
    