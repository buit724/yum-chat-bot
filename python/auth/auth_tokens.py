import asyncio
import configparser

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator, UserAuthenticationStorageHelper
from twitchAPI.type import AuthScope

TARGET_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS]
MY_URL = 'http://localhost:17563'
PROP_FILE = ''


async def main():
    config = configparser.ConfigParser()
    # print(os.environ['BOT_PROP_FILE'])
    config.read(PROP_FILE)

    global twitch, auth
    twitch = await Twitch(config['app']['CLIENT_ID'], config['app']['CLIENT_SECRET'])



    auth = UserAuthenticator(twitch, TARGET_SCOPE)
    token, refresh = await auth.authenticate()
    print("Done")
    print(f"token: {token}")
    print(f'refresh_token: {refresh}')


asyncio.run(main())
