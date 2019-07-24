from dotenv import find_dotenv, load_dotenv
import os
import rollbar
from flask import Flask
from flask import (
    render_template,
    request,
    url_for,
    session
)
import json


load_dotenv(find_dotenv())

rollbar.init(os.getenv('ROLLBAR_POST_SERVER_ITEM'))
# The session object makes use of a secret key.
app = Flask(__name__)


@app.route('/rollbar', methods=['POST'])
def post_error():
    twilio_payload = json.loads(request.form['Payload'])
    print(request.form)
    msg = twilio_payload.get('error_code')
    if twilio_payload.get('more_info'):
        if twilio_payload['more_info'].get('msg'):
            msg += f' - {twilio_payload["more_info"]["msg"]}'
    try:
        rollbar.report_message(msg, (request.form['Level'].lower()), request.form)
    except Exception as e:
        print(e)
    return '', 204


if __name__ == '__main__':
    app.run()
