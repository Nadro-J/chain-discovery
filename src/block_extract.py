#!/usr/bin/python3
from src import rpc_request
from src import psql
import json
import pathlib

class scrape_chain:
    def __init__(self):
        self.dir = pathlib.Path(__file__).parent.parent
        self.rpc = rpc_request.rpc()
        self.height = self.getblockheight()
        self.blocks_processed = 1
        self.counter = 0
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
            time
            total_out               total_size
            total_weight            totalfee
            txs                     utxo_increase
            utxo_size_inc
        """
        block_stats = self.rpc.request("getblockstats", [self.blocks_processed])
        try:
            for key in block_stats:
                self.blockstats_construct[key] = str(block_stats[key]).translate(str.maketrans('', '', '[]')).translate(str.maketrans({"'": None}))
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
        with open(f"{self.dir}/utils/sql/getblockstats_bulk_insert.sql", 'r')as f:
            batchInsertQuery = f.read()

        with open('config.json') as config:
            config = json.load(config)

        sql = psql.connector(config)
        blockstat_data = []
        block = ()

        while self.blocks_processed < self.height:

            # visual debugging/capturing of block data
            print(f"▓▓ HEIGHT: {self.blocks_processed} ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")

            for key in self.getblockstats():
                # Add square brackets [] inbetween feerate_percentiles output to resolve
                # issue with SQL query being incorrect
                if key == 'feerate_percentiles':
                    block = block + (str("[" + self.getblockstats()[key] + "]"),)
                    pass
                else:
                    block = block + (str(self.getblockstats()[key]),)

            # add the data insert into dictionary 'bulk_insert'
            blockstat_data.append(block)
            block = ()

            # insert data every 250 blocks
            if self.blocks_processed % 250 == 0:
                sql.cursor.execute(batchInsertQuery.format(SQL_INSERTS=str(blockstat_data)[1:-1]))
                sql.connection.commit()

                # clear bulk_insert
                blockstat_data = []
                
            self.blocks_processed = self.blocks_processed + 1

        if self.blocks_processed > 0:
            sql.cursor.execute(batchInsertQuery.format(SQL_INSERTS=str(blockstat_data)[1:-1]))
            sql.connection.commit()