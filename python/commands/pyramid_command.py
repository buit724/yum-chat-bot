from typing import List, Union

from twitchAPI.chat import ChatCommand
from twitchAPI.chat.middleware import UserRestriction, BaseCommandMiddleware

from python.commands.command import Command


class PyramidCommand(Command):
    MAX_PYRAMID_WIDTH: int = 5

    def get_middleware(self) -> Union[List[BaseCommandMiddleware], None]:
        """
        Only myself can use it
        :return: The user middleware with only myself
        """
        return [UserRestriction(allowed_users=['buit724'])]

    def get_name(self) -> str:
        """
        Get the name of this build pyramid command
        :return: Name of build pyramid command
        """
        return "pyramid"

    async def process_command(self, cmd: ChatCommand) -> None:
        """
        Send multiple messages to build a pyramid with width specified by the user using the specified emote
        Usage: !yum_pyramid [emote] [pyramid_width <= 5]
        :param cmd:     The command with the emote and width
        :return:
        """
        build_pyramid_usage: str = f"Usage: !yum_pyramid [emote] [pyramid_width <= {self.MAX_PYRAMID_WIDTH}]"
        args: List[str] = cmd.parameter.strip().split()

        # Arg count check (at least 2)
        if len(args) < 2:
            await cmd.reply(build_pyramid_usage)
            return
        # Check that width is a positive number
        if not args[1].isdigit():
            await cmd.reply(build_pyramid_usage)
            return

        # CHeck width range so it doesn't spam the chat too much
        pyramid_width: int = int(args[1])
        if pyramid_width > self.MAX_PYRAMID_WIDTH:
            await cmd.reply(build_pyramid_usage)
            return

        emote = args[0].strip()
        for i in range(1, pyramid_width * 2):
            msg: str = " ".join([emote] * (pyramid_width - abs(pyramid_width - i)))
            await cmd.chat.send_message(cmd.room, msg)
