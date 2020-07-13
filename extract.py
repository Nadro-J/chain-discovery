#!/usr/bin/python3
# TODO
#   == Blockchain ==
#       - getblockstats
#       - getchaintxstats
#   == Raw Transactions ==
#       - getrawtransaction
#
#  Build SQL server with relevant tables to populate data with.

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
        self.rpc = rpc()
        self.height = self.rpc.request('getblockcount')
        self.blocks_processed = 0

    # Store output into SQL table [blockinfo]
    # theory-query:
    #   SELECT * FROM blockinfo WHERE tx = '39d15a41590a04edefc007d3d8c3eb6e81df54d6efe0ca3d155b5de8a0364f79'
    #   SELECT * FROM blockinfo WHERE flags LIKE '%proof-of-stake%' AND weight <= 300
    def blockinfo(self):
        while self.blocks_processed < self.height:
            #if self.blocks_processed % 1000 == 1:
            #    print(self.blocks_processed)

            block_hash = self.rpc.request("getblockhash", [self.blocks_processed])
            block = self.rpc.request("getblock", [block_hash])

            for key in block.keys():
                # extract subkey 'cbTx'
                if (type(block[key]) == dict):
                    for subkey in block[key].keys():
                        print(f"cbTx-{subkey}: {block[key][subkey]}")

                if (type(block[key]) == float):
                    print(f"{key}: {format(block[key], '.8f')}")

                # skip over cbTx to avoid double print as the info is extracted above
                if (key == 'cbTx'):
                    pass
                elif (key == 'difficulty'):
                    pass
                else:
                    print(f"""{key}: {str(block[key]).translate(str.maketrans('', '', '[]')).translate(str.maketrans({"'":None}))}""")

            self.blocks_processed = self.blocks_processed + 1

if __name__ == '__main__':
    chain = blockchain()
    chain.blockinfo()
