import pytest
from functools import reduce
from brownie import web3
from math import floor
from eth_utils import decode_hex

from tests.tx_sum import tx_sum


class SimpleBatch:
    def __init__(self, simple_batch_NOR, node_operator, stranger, helpers, batch_size):
        self.simple_batch_NOR = simple_batch_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers
        self.batch_size = batch_size

    def deposit(self, keys_amount):
        txs = []

        keys_and_signs = [(self.helpers.get_random_pseudo_key(), self.helpers.get_random_pseudo_sign()) for i in range(0, keys_amount)]

        keys = [ks[0] for ks in keys_and_signs]
        signs = [ks[1] for ks in keys_and_signs]

        hashes = []

        for i in range(0, floor(keys_amount/self.batch_size)):
            start = self.batch_size * i
            end = self.batch_size * (i + 1)
            keysSignsBytes = b''
            for j in range(start, end):
                keysSignsBytes = b''.join([keysSignsBytes,decode_hex(keys[j]), decode_hex(signs[j])])
            hash = web3.keccak(keysSignsBytes)
            hashes.append(hash)


        tx = self.simple_batch_NOR.addPubkeysAndSignsHashes(hashes, {'from': self.node_operator});
        txs.append(tx)

        self.simple_batch_NOR.submit({'from':self.stranger, 'amount': keys_amount * 32 * 10**18})

        tx = self.simple_batch_NOR.depositBufferedEther(keys, signs,{'from': self.stranger})
        txs.append(tx)

        for i in range(0, keys_amount):
            assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
            assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

        return reduce(tx_sum, txs, 0)
