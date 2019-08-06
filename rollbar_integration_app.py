import json
import os
from slack import WebClient
import rollbar
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask import (
    request
)
from post_to_slack import post_to_slack

load_dotenv(find_dotenv())
slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
rollbar.init(os.getenv('ROLLBAR_POST_SERVER_ITEM'))

app = Flask(__name__)

dbFile = './FlexErrors.json'
with open(dbFile, 'rU') as f:
    read_data = f.read()
    flex_errors = json.loads(read_data)
    f.close()


@app.route('/twiliodebugevents', methods=['POST'])
@validate_twilio_request
def post_event():
    payload = json.loads(request.form['Payload'])
    msg = error_code = str(payload.get('error_code'))
    if payload.get('more_info') and payload['more_info'].get('msg'):
        msg += f' - {payload["more_info"]["msg"]}'
    try:
        if error_code in flex_errors.keys():
            post_to_slack(request, msg, error_code)
        rollbar.report_message(msg, (request.form['Level'].lower()),
                               request.form)
    except Exception as e:
        print(e)
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
