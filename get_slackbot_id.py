import os
from dotenv import load_dotenv, find_dotenv
import ssl
from slack import WebClient

load_dotenv(find_dotenv())

BOT_NAME = "twilioflexerrors"

slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
print(slack_client)


if __name__ == "__main__":
    print(slack_client.bots_info())

    api_call = slack_client.api_call('users.list', http_verb='GET')

    if api_call.get('ok'):
        print("WOHOO")
    # retrieve all users so we can find our bot
    users = api_call.get('members')
    for user in users:
       if 'name' in user and user.get('name') == BOT_NAME:
               print("Bot ID for '" + user['name'] + "' is " + user.get('id'))

