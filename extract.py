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
import flask
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

class scrape_chain:
    def __init__(self):
        self.rpc = rpc()
        self.height = self.getblockheight()
        self.blocks_processed = 0
        self.blockinfo_construct = {}
        self.blockstats_construct = {}
        self.blockheader_construct = {}

    def getblockheight(self):
        return self.rpc.request('getblockcount')

    def getblockheader(self):
        """
        RETURN: json object
        Perform RPC commands getblockheader and dump the output into json

        JSON Keys:
            hash                    nTx
            confirmations           nextblockhash
            strippedsize            chainlock
            size                    previousblockhash
            weight                  versionHex
            height                  chainwork
            version                 difficulty
            bits                    nonce
            merkleroot              mediantime
            time
        """
        blockheader = self.rpc.request("getblockhash", [self.blocks_processed])
        blockheader_data = self.rpc.request("getblockheader", [blockheader])

        try:
            for key in blockheader_data:
                self.blockheader_construct[key] = blockheader_data[key]
            return json.loads(json.dumps(self.blockheader_construct))
        except Exception as error:
            return f"Exception raised on getblockheader():\n {error}"

    def getblockstats(self):
        """
        RETURN: json object
        Perform RPC commands getblockstats and dump the output into json

        JSON Keys:
            avgfee                  avgfeerate
            avgtxsize               blockhash
            feerate_percentiles     height
            ins                     maxfee
            maxfeerate              maxtxsize
            medianfee               mediantime
            mediantxsize            minfee
            minfeerate              mintxsize
            outs                    subsidy
            swtotal_size            swtotal_weight
            swtxs                   time
            total_out               total_size
            total_weight            totalfee
            txs                     utxo_increase
            utxo_size_inc
        """
        block_stats = self.rpc.request("getblockstats", [self.blocks_processed])
        try:
            for key in block_stats:
                self.blockstats_construct[key] = block_stats[key]
            return json.loads(json.dumps(self.blockstats_construct))
        except Exception as error:
            return f"Exception raised on getblockstats():\n {error}"

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
        return json.loads(json.dumps(self.blockinfo_construct))

    def process_blocks(self):
        while self.blocks_processed < self.height:

            # visual debugging/capturing of block data
            print(f"▓▓ HEIGHT: {self.blocks_processed} ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
            print(self.blockchaininfo())
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print(self.getblockstats())
            print("░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
            print(self.getblockheader())
            print("\n")

            self.blocks_processed = self.blocks_processed + 1

@app.route('/api/v1/gobject', methods=['GET'])
def gobject_API():
    cmd = request.args.get('cmd')
    arg = request.args.get('arg')
    return rpc().gobject(cmd, arg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    # commented out whilst messing around with Flask API.
    #chain = scrape_chain()
    #chain.process_blocks()