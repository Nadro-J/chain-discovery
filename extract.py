#!/usr/bin/python3
# TODO
#   == Blockchain ==
#       - getblockstats
#       - getchaintxstats
#   == Raw Transactions ==
#       - getrawtransaction
#
#  Build SQL server with relevant tables to populate data with.
#
#  Theory-query:
#   SELECT * FROM blockinfo WHERE tx = '39d15a41590a04edefc007d3d8c3eb6e81df54d6efe0ca3d155b5de8a0364f79'
#   SELECT * FROM blockinfo WHERE flags LIKE '%proof-of-stake%' AND weight <= 300

import json, requests

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
        self.height = self.getblockheight()
        self.blocks_processed = 0
        self.blockinfo_construct = {}

    def getblockheight(self):
        return self.rpc.request('getblockcount')

#    def getblockstats(self):
#        block_stats = self.rpc.request("getblockstats", [self.blocks_processed])
#        return block_stats

    def blockchaininfo(self):
        """
        RETURN: json object
        Perform RPC commands getblockhash, getblock and dump the output into json

        JSON Keys:
            hash                    chainwork
            confirmations           nTx
            strippedsize            nextblockhash
            size                    mint
            weight                  moneysupply
            height                  flags
            version                 proofhash
            versionHex              entropybit
            merkleroot              modifier
            tx                      modifierchecksum
            time                    blocksignature
            mediantime              chainlock
            nonce                   merkleRootMNList
            bits                    merkleRootQuorums
            difficulty              previousblockhash
        """
        block_hash = self.rpc.request("getblockhash", [self.blocks_processed])
        block      = self.rpc.request("getblock", [block_hash])

        try:
            for key in block.keys():
                # extract subkey 'cbTx' data
                if type(block[key]) == dict:
                    for subkey in block[key].keys():
                        self.blockinfo_construct[subkey] = block[key][subkey]

                # Add 8 decimal places
                if type(block[key]) == float:
                    self.blockinfo_construct[key] = format(block[key], '.8f')

                # skip over cbTx, difficulty and mint to avoid double printing
                if key == 'cbTx':
                    pass
                elif (key == 'difficulty'):
                    pass
                elif (key == 'mint'):
                    pass
                else:
                    self.blockinfo_construct[key] = str(block[key]).translate(str.maketrans('', '', '[]')).translate(str.maketrans({"'": None}))
        except Exception as error:
            return f"Exception raised on getblockinfo():\n {error}"

        block = json.dumps(self.blockinfo_construct)
        return json.loads(block)

    def process_blocks(self):
        while self.blocks_processed < self.height:
            print(self.blockchaininfo())  # printing to debug

            self.blocks_processed = self.blocks_processed + 1

if __name__ == '__main__':
    chain = blockchain()
    chain.process_blocks()