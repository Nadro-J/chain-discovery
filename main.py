#!/usr/bin/python3

import flask
from flask import request
from src import rpc_request
from src import block_extract

app = flask.Flask(__name__)
app.config["DEBUG"] = True
rpc = rpc_request.rpc()

@app.route('/api/v1/gobject', methods=['GET'])
def gobject_API():
    cmd = request.args.get('cmd')
    arg = request.args.get('arg')
    return rpc.gobject(cmd, arg)

@app.route('/api/v1/getgovernanceinfo', methods=['GET'])
def getgovernanceinfo_API():
    return rpc.getgovernanceinfo()

@app.route('/api/v1/masternodelist', methods=['GET'])
def masternodelist_API():
    mode = request.args.get('mode')
    filter = request.args.get('filter')
    return rpc.masternodelist(mode, filter)

@app.route('/api/v1/masternode', methods=['GET'])
def masternode_API():
    cmd = request.args.get('cmd')
    arg = request.args.get('arg')
    return rpc.masternode(cmd, arg)

@app.route('/api/v1/getblockchaininfo', methods=['GET'])
def getblockchaininfo_API():
    return rpc.getblockchaininfo()

@app.route('/api/v1/getblockhash', methods=['GET'])
def getblockhash_API():
    block_height = request.args.get('height')
    return rpc.getblockhash(block_height)

@app.route('/api/v1/getblockheader', methods=['GET'])
def getblockheader_API():
    block_height = request.args.get('hash')
    verbose = request.args.get('verbose')
    return rpc.getblockheader(block_height, verbose)

@app.route('/api/v1/getblock', methods=['GET'])
def getblock_API():
    hash = request.args.get('hash')
    verbose = request.args.get('verbose')
    return rpc.getblock(hash, verbose)

@app.route('/api/v1/getblockstats', methods=['GET'])
def getblockstats_API():
    hash = request.args.get('hash')
    verbose = request.args.get('verbose')
    return rpc.getblockstats(hash, verbose)

@app.route('/api/v1/getblockcount', methods=['GET'])
def getblockcount_API():
    return rpc.getblockcount()

@app.route('/api/v1/spork', methods=['GET'])
def spork_API():
    cmd = request.args.get('cmd')
    return rpc.spork(cmd)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    #chain = block_extract.scrape_chain()
    #chain.process_blocks()