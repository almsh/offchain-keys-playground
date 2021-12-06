from functools import reduce
from math import floor

from brownie import web3
from eth_utils import decode_hex, encode_hex

from tests.merkle_tree import MerkleTree
from tests.tx_sum import tx_sum

def flatten(t):
    return [item for sublist in t for item in sublist]

class MerkleBatch:
    def __init__(self, merkle_batch_NOR, node_operator, stranger, helpers):
        self.merkle_batch_NOR = merkle_batch_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers


    def deposit(self, batch_size, tree_size, portion):

        keys_batches = []
        signs_batches = []

        for i in range(0, tree_size):
            keys_batches.append([self.helpers.get_random_pseudo_key() for j in range(0, batch_size)])
            signs_batches.append([self.helpers.get_random_pseudo_sign() for j in range(0, batch_size)])

        hashes = []

        for i in range(0, tree_size):
            keysSignsBytes = b''.join([i.to_bytes(32, 'big')])
            for j in range(0, batch_size):
                keysSignsBytes = b''.join([keysSignsBytes, decode_hex(keys_batches[i][j]), decode_hex(signs_batches[i][j])])
            hash = encode_hex(web3.keccak(keysSignsBytes))
            hashes.append(hash)


        tree = MerkleTree(hashes)

        self.merkle_batch_NOR.addMerkleRoot(tree.root, tree_size, batch_size, {'from': self.node_operator})

        self.merkle_batch_NOR.submit({'from': self.stranger, 'amount': tree_size * batch_size * 32 * 10 ** 18})

        keys_batches.reverse()
        signs_batches.reverse()
        hashes.reverse()

        txs = []
        for i in range(0, floor(tree_size / portion)):
            start = i * portion
            end = (i + 1) * portion
            keys_portion = flatten(keys_batches[start:end])
            signs_portion = flatten(signs_batches[start:end])
            tx = self.merkle_batch_NOR.depositBufferedEther(keys_portion,
                                                            signs_portion,
                                                            [tree.get_proof(l) for l in hashes[start:end]],
                                                            {'from': self.stranger})
            txs.append(tx)

            for j in range(0, portion):
                assert tx.events['DepositEvent'][j]['pubkey'] == keys_portion[j]
                assert tx.events['DepositEvent'][j]['signature'] == signs_portion[j]

        return reduce(tx_sum, txs, 0)
