#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "chuckNorrisJoke":
        return {}
    baseurl = "http://api.icndb.com/jokes/random?exclude=[nerdy,explicit]"
    result = urllib.urlopen(baseurl).read()
    data = json.loads(result)
    print("Data: ")
    print(data)
    res = makeWebhookResult(data)
    return res

def makeWebhookResult(data):
    success = data.get('success')
    print("Success: ")
    print(success)

    if success == False:
        return {}
    else:
        value = data.get('value')
        print("Value: ")
        print(value)
        if value is None:
            return {}
        else:
            joke = value.get('joke')



    print("Joke:")
    print(joke)

    return {
        "speech": joke,
        "displayText": joke,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-chuck-norris-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
