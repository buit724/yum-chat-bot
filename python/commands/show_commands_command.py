from typing import List

from twitchAPI.chat import ChatCommand

from python.commands.command import Command


class ShowCommandsCommand(Command):
    def __init__(self, command_prefix: str, commands: List[str]):
        """
        All the commands that have been added by this bot
        :param command_prefix   The command prefix
        :param commands:        The list of command names
        """
        self.commands: str = ", ".join([f"{command_prefix}{x}" for x in commands])

    async def process_command(self, cmd: ChatCommand):
        """
        Show all the available commands
        :return: The ChatCommand object with the command arguments
        """
        await cmd.reply(f"Available yum commands are: {self.commands}")
