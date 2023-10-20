from typing import AsyncGenerator, Callable, Awaitable, List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twitchAPI.chat import Chat, ChatMessage, EventData, ChatCommand
from twitchAPI.object.api import TwitchUser
from twitchAPI.twitch import Twitch

import asyncio
import configparser
import sys

from twitchAPI.type import AuthScope, ChatEvent

from python.commands.claim_moment_command import ClaimMomentCommand
from python.commands.give_moment_command import GiveMomentCommand
from python.commands.pyramid_command import PyramidCommand
from python.commands.show_commands_command import ShowCommandsCommand

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS]
COMMAND_PREFIX = "!yum"


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    # Join channel on startup
    broadcaster: str = config['channel']['broadcaster']
    print(f'Joining {broadcaster}')
    await ready_event.chat.join_room(broadcaster)
    # you can do other bot initialization things in here


async def on_message(msg: ChatMessage):
    # Current only logging the messages. Might do something else later
    print(f"Got a message from {msg.user.display_name}: {msg.text}")


def add_command(chat: Chat, command: str, handler: Callable[[ChatCommand], Awaitable[None]]) -> str:
    """
    Register the command to the chat and returns the name of the command. Should use this to keep track of all
    the commands we have added
    :param chat:    The chat
    :param command: The command name
    :param handler: The command handler
    :return:    The command name
    """
    chat.register_command(command, handler)
    return command


async def main():
    # initialize the twitch instance, this will by default also create an app authentication for you
    twitch: Twitch = await Twitch(config['app']['CLIENT_ID'], config['app']['CLIENT_SECRET'])
    await twitch.set_user_authentication(config['token']['TOKEN'], USER_SCOPE, config['token']['REFRESH_TOKEN'])

    # get broadcaster id (ie channel id) and moderator id (ie the bot id that should be a moderator for the channel)
    broadcaster: str = config['channel']['broadcaster']
    users: AsyncGenerator[TwitchUser, None] = twitch.get_users(logins=[broadcaster, config['channel']['BOT']])
    user_ids = [x.id async for x in users]
    broadcaster_id: str = user_ids[0]
    moderator_id: str = user_ids[1]

    # Setting chat object for events
    chat: Chat = await Chat(twitch)

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)

    scheduler: AsyncIOScheduler = AsyncIOScheduler()

    # Register commands
    chat.set_prefix(COMMAND_PREFIX)
    commands: List[str] = []

    # Pyramid command
    pyramid_command: PyramidCommand = PyramidCommand()
    commands.append(add_command(chat, "p", pyramid_command.process_command))

    # Give moment command
    give_moment_command: GiveMomentCommand = GiveMomentCommand(twitch, broadcaster, broadcaster_id, moderator_id,
                                                               scheduler)
    commands.append(add_command(chat, "gm", give_moment_command.process_command))

    # Claim moment command
    claim_moment_command: ClaimMomentCommand = ClaimMomentCommand(broadcaster, give_moment_command)
    commands.append(add_command(chat, "cm", claim_moment_command.process_command))

    # Show available commands
    show_commands_command: ShowCommandsCommand = ShowCommandsCommand(COMMAND_PREFIX, commands)
    chat.register_command("commands", show_commands_command.process_command)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # Let the bot run in the background until we force quit
    try:
        # Run schedule tasks here for now
        scheduler.start()
        # scheduler.add_job(start_up)
        await asyncio.Event().wait()
        # loop = asyncio.get_event_loop()#.run_forever()
        # loop.run_forever()
    finally:
        # now we can close the chatbot and the twitch api client
        chat.stop()
        await twitch.close()


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    asyncio.run(main())
