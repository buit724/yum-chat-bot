from twitchAPI.chat import ChatCommand

from python.commands.command import Command
from python.commands.give_moment_command import GiveMomentCommand


class ClaimMomentCommand(Command):
    def __init__(self, channel: str, give_moment_command: GiveMomentCommand):
        self.channel: str = channel
        self.give_moment_command: GiveMomentCommand = give_moment_command

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
    