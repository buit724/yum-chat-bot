from twitchAPI.chat import ChatCommand


class Command:
    async def process_command(self, cmd: ChatCommand):
        """
        Process the command sent
        :return: The ChatCommand object with the command arguments
        """
        pass
