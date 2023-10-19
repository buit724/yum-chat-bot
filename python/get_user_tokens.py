import asyncio
import configparser
import os
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, TwitchAPIException
from flask import Flask, redirect, request

TARGET_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT, AuthScope.MODERATOR_MANAGE_ANNOUNCEMENTS]
MY_URL = 'http://localhost:5000/login/confirm'

app = Flask(__name__)
twitch: Twitch
auth: UserAuthenticator


@app.route('/login')
def login():
    return redirect(auth.return_auth_url())


@app.route('/login/confirm')
async def login_confirm():
    state = request.args.get('state')
    if state != auth.state:
        return 'Bad state', 401
    code = request.args.get('code')
    #print(code)
    if code is None:
        return 'Missing code', 400
    try:
        print(code)
        token, refresh = await auth.authenticate(user_token=code)
        print(f"token: {token}")
        print(f'refresh_token: {refresh}')
        await twitch.set_user_authentication(token, TARGET_SCOPE, refresh)
    except TwitchAPIException as e:
        return 'Failed to generate auth token', 400
    return 'Successfully authenticated!'


async def get_tokens():
    """
    Gets the token and refresh token for the currently logged-in user that the script can use to send messages.
    Make sure the currently logged-in user is the Bot account and not your personal account. Should be run as a flask
    app and the BOT_PROP_FILE environment variable is set to the path of the property file containing
    the client id and secret
    :return:
    """
    # Read in config file
    config = configparser.ConfigParser()
    print(os.environ['BOT_PROP_FILE'])
    config.read(os.environ['BOT_PROP_FILE'])

    global twitch, auth
    twitch = await Twitch(config['app']['CLIENT_ID'], config['app']['CLIENT_SECRET'])
    auth = UserAuthenticator(twitch, TARGET_SCOPE, url=MY_URL)
    token, refresh = await auth.authenticate()
    print("Done")
    print(f"token: {token}")
    print(f'refresh_token: {refresh}')


def wrapper():
    asyncio.run(get_tokens())


scheduler = BackgroundScheduler()
scheduler.add_job(wrapper)
scheduler.start()
