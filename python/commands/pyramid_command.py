from typing import List

from twitchAPI.chat import ChatCommand

from python.commands.command import Command


class PyramidCommand(Command):
    MAX_PYRAMID_WIDTH: int = 5

    async def process_command(self, cmd: ChatCommand):
        """
        Send multiple messages to build a pyramid with width specified by the user using the specified emote
        Usage: !yum_pyramid [emote] [pyramid_width <= 5]
        :param cmd:     The command with the emote and
        :return:
        """

        build_pyramid_usage: str = f"Usage: !yum_pyramid [emote] [pyramid_width <= {self.MAX_PYRAMID_WIDTH}]"
        args: List[str] = cmd.parameter.strip().split(" ")

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
