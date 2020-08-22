#!/usr/bin/python3
import re
import json
import requests

class rpc:
    def __init__(self):
        self.url = 'http://rpcuser:rpcpwd@localhost:8331'
        self.rpc_arguments = []  # Always clear rpc_arguments during every call to the API

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

    def arg_handler(self, args):
        self.rpc_arguments.clear()
        for value in args:
            if value != None:
                if re.search('true', value):
                    self.rpc_arguments.append(bool(value.title()))
                else:
                    self.rpc_arguments.append(value)
        return self.rpc_arguments

    # Set of commands to manage governance objects
    def gobject(self, *args):
        return self.request('gobject', self.arg_handler(args))

    def getgovernanceinfo(self):
        return self.request('getgovernanceinfo')

    def masternodelist(self, *args):
        return self.request('masternodelist', self.arg_handler(args))

    def masternode(self, *args):
        return self.request('masternode', self.arg_handler(args))

    def getblockchaininfo(self):
        return self.request('getblockchaininfo')

    def getblockhash(self, block_height):
        return self.request('getblockhash', [int(block_height)])

    def getblockheader(self, *args):
        return self.request('getblockheader', self.arg_handler(args))

    def getblock(self, *args):
        return self.request('getblock', self.arg_handler(args))

    def getblockstats(self, *args):
        return self.request('getblockstats', self.arg_handler(args))

    def getblockcount(self):
        return str(self.request('getblockcount'))

    def spork(self, *args):
        return self.request('spork', self.arg_handler(args))
