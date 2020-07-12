#!/usr/bin/python3
import requests
import json

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

class blockchain:
    def __init__(self):
        self.height = rpc().request('getblockcount')
        self.blocks_processed = 0

    def blockinfo(self):
        while self.blocks_processed < self.height:
            #if self.blocks_processed % 1000 == 1:
            #    print(self.blocks_processed)

            block_hash = rpc().request("getblockhash", [self.blocks_processed])
            block = rpc().request("getblock", [block_hash])

            for key in block.keys():
                # extract subkey 'cbTx'
                if (type(block[key]) == dict):
                    for subkey in block[key].keys():
                        print(f"{subkey}: {block[key][subkey]}")

                # skip over cbTx to avoid double print as the info is extracted above
                if (key == 'cbTx'):
                    pass
                else:
                    print(f"""{key}: {str(block[key]).translate(str.maketrans('', '', '[]')).translate(str.maketrans({"'":None}))}""")

            self.blocks_processed = self.blocks_processed + 1

if __name__ == '__main__':
    chain = blockchain()
    chain.blockinfo()