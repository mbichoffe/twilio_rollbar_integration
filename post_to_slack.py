from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from slack import WebClient
import os
import json

load_dotenv(find_dotenv())
slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))

dbFile = './FlexErrors.json'
with open(dbFile, 'rU') as f:
    read_data = f.read()
    flex_errors = json.loads(read_data)
    f.close()

def post_to_slack(request, msg, error_code):
    level = request.form.get('Level')
    account_sid = request.form.get('AccountSid')
    sid = request.form['Sid']
    datetimeObj = datetime.strptime(request.form["Timestamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
    date = datetimeObj.strftime("%a, %d %b %Y %H:%M:%S")
    color = "warning" if level == "WARNING" else "danger"
    try:
        slack_client.chat_postMessage(
            channel="#flex-prod",
            icon_url="https://s3.amazonaws.com/com.twilio.prod.twilio-docs/original_images/twilio-mark-red.png",
            attachments=[
                {
                    "title": f'{level} - {msg}: {flex_errors.get(error_code) } ',
                    "fallback": f'New occurrence on {date}',
                    "pretext": f'New occurrence on {date}',
                    "author_name": "See in Rollbar",
                    "author_link": "https://rollbar.com/Twilio/mbichoffe-signal-2019-demo/",
                    "author_icon": "http://flickr.com/icons/bobby.jpg",
                    "color": "danger",
                    "fields": [
                        {
                            "title": "AccountSid",
                            "value": account_sid,
                            "short": False
                        },
                        {
                            "title": "Sid",
                            "value": sid,
                            "short": False
                        },
                        {
                            "type": "section",
                            "block_id": "section567",
                            "text": {
                                "type": "mrkdwn",
                                "text": "<https://rollbar.com/Twilio/mbichoffe-signal-2019-demo/|See in Rollbar>"
                            }
                        }
                    ]
                },
            ]

        )
    except Exception as e:
        print("Exception", e)
    return
