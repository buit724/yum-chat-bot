from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twitchAPI.chat import Chat, ChatMessage, EventData
from twitchAPI.object.api import TwitchUser
from twitchAPI.twitch import Twitch

import asyncio
import configparser
import sys

from twitchAPI.type import AuthScope, ChatEvent

from python.commands.claim_moment_command import ClaimMomentCommand
from python.commands.command import Command
from python.commands.start_moment_command import StartMomentCommand
from python.commands.pyramid_command import PyramidCommand
from python.commands.show_commands_command import ShowCommandsCommand
from python.state.global_state import GlobalState

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS]
COMMAND_PREFIX = "!y"


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


def add_commands(chat: Chat, commands: List[Command]) -> List[str]:
    """
    Register all commands to chat
    :param chat:        The chat
    :param commands:    The commands
    :return: The names of added commands
    """
    return [add_command(chat, x) for x in commands]


def add_command(chat: Chat, command: Command) -> str:
    """
    Register the command to the chat and returns the name of the command. Should use this to keep track of all
    the commands we have added
    :param chat:    The chat
    :param command: The command name
    :return:    The command name
    """
    chat.register_command(command.get_name(), command.process_command)
    return command.get_name()


async def main():
    # initialize the twitch instance with both app and user tokens
    twitch: Twitch = await Twitch(config['app']['CLIENT_ID'], config['app']['CLIENT_SECRET'])
    await twitch.set_user_authentication(config['token']['TOKEN'], USER_SCOPE, config['token']['REFRESH_TOKEN'])

    # get broadcaster id (ie channel id) and moderator id (ie the bot id that should be a moderator for the channel)
    broadcaster: str = config['channel']['broadcaster']
    users: List[TwitchUser] = [x async for x in twitch.get_users(logins=[broadcaster, config['channel']['BOT']])]
    broadcaster_id: str = users[0].id
    moderator_id: str = users[1].id

    # Setting chat object for events
    chat: Chat = await Chat(twitch)

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages (for here so we can easily see what channel we're in and getting messages)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    # Setup objects
    scheduler: AsyncIOScheduler = AsyncIOScheduler()
    global_state: GlobalState = GlobalState()

    # Set prefix so it is different from other bot commands
    chat.set_prefix(COMMAND_PREFIX)

    # Register commands
    command_names = add_commands(chat, [
        PyramidCommand(),
        StartMomentCommand(global_state, twitch, broadcaster, broadcaster_id, moderator_id, COMMAND_PREFIX, scheduler),
        ClaimMomentCommand(global_state, broadcaster)
    ])

    # Register show available commands
    show_commands_command: ShowCommandsCommand = ShowCommandsCommand(COMMAND_PREFIX, command_names)
    add_command(chat, show_commands_command)

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
