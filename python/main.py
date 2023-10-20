from typing import AsyncGenerator

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from twitchAPI.chat import Chat, ChatMessage, EventData
from twitchAPI.object.api import TwitchUser
from twitchAPI.twitch import Twitch

import asyncio
import configparser
import sys

from twitchAPI.type import AuthScope, ChatEvent

from python.commands.claim_moment_command import ClaimMomentCommand
from python.commands.give_moment_command import GiveMomentCommand
from python.commands.pyramid_command import PyramidCommand

USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS]


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
    chat = await Chat(twitch)

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)

    scheduler: AsyncIOScheduler = AsyncIOScheduler()

    # Register commands
    # Pyramid command
    pyramid_command: PyramidCommand = PyramidCommand()
    chat.register_command("yum_pyramid", pyramid_command.process_command)

    # Give moment command
    give_moment_command: GiveMomentCommand = GiveMomentCommand(twitch, broadcaster, broadcaster_id, moderator_id,
                                                               scheduler)
    chat.register_command("yum_give_moment", give_moment_command.process_command)

    # Claim moment command
    claim_moment_command: ClaimMomentCommand = ClaimMomentCommand(broadcaster, give_moment_command)
    chat.register_command("yum_claim_moment", claim_moment_command.process_command)

    # we are done with our setup, lets start this bot up!
    chat.start()

    # Let the bot run in the background until we force quit
    try:
        # print("Hello")
        # Run schedule tasks here for now
        scheduler.start()
        # scheduler.add_job(start_up)
        await asyncio.Event().wait()
        #loop = asyncio.get_event_loop()#.run_forever()
        #loop.run_forever()
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


if __name__ == "__main__":
    global config
    config = configparser.ConfigParser()
    config.read(sys.argv[1])
    asyncio.run(main())