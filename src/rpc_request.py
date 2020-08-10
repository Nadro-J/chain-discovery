#!/usr/bin/python3

import json
import requests

class rpc:
    def __init__(self):
        self.url = 'http://rpcuser:rpcpwd@localhost:8331'

    def request(self, method, params=None):
        payload = {'id': 1, 'method': method, 'rpc': '1.0'}
        if params is not None:
            payload['params'] = params

        r = requests.post(self.url, data=json.dumps(payload))
        if r.status_code != 200:
            print("could not process your request: code=" + str(r.status_code) + " reason=" + r.reason + " text=" + r.text)
            return ""

        body = json.loads(r.text)
        return body['result']

    # Set of commands to manage governance objects
    def gobject(self, *args):
        build_args = []
        for value in args:
            if value != None:
                build_args.append(value)
        return self.request('gobject', build_args)
