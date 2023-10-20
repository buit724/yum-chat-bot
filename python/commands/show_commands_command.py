from twitchAPI.chat import ChatCommand

from python.commands.command import Command


class ShowCommandsCommand(Command):

    async def process_command(self, cmd: ChatCommand):
        """
        Show all the available commands
        :return: The ChatCommand object with the command arguments
        """
        commands: str = ", ".join([f"!yum{x}" for x in ["p", "gm", "cm"]])
        await cmd.reply(f"Available yum commands are: {commands}")
