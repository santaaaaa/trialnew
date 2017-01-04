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
    if req.get("result").get("action") != "customsearchtrial":
        return {}
    baseurl = "https://www.googleapis.com/customsearch/v1?"
    gse_query = makegseQuery(req)
    if gse_query is None:
        return {}
    gse_url = baseurl + urllib.urlencode({'q': gse_query}) + "&cx=004041591984903320296:4qlxcgnnbvs&num=1&key=AIzaSyCbVAZvrSARaerACN-s0VeIybozDaP6Zg8"
    result = urllib.urlopen(gse_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makegseQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    sweat = parameters.get("sweat")
    if sweat is None:
        return None
    
    return "('" + sweat + "')"


def makeWebhookResult(data):
    items = data.get('items')
    if items is None:
        return {}

    title = items.get('title')
    if title is None:
        return {}

    snippet = items.get('snippet')
    if snippet is None:
        return {}
        
    link = items.get('link')
    if link is none:
        return {}    


    # print(json.dumps(item, indent=4))

    speech = "I have found this" + ": " + 'snippet' + "from" + 'link'

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        "contextOut": [{"name":"gen", "lifespan":1}],
        "source": "apiai-python-webhook"
    
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
