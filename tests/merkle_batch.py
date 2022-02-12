from functools import reduce
from math import floor

from brownie import web3
from eth_utils import decode_hex, encode_hex

from tests.merkle_tree import MerkleTree
from tests.tx_sum import tx_sum

def flatten(t):
    return [item for sublist in t for item in sublist]

class MerkleBatch:
    def __init__(self, merkle_batch_NOR, node_operator, stranger, helpers, tree_size, batch_size):
        self.merkle_batch_NOR = merkle_batch_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers
        self.tree_size = tree_size
        self.batch_size = batch_size
        self.offset = 0
        self.add_root()

    @property
    def total_tree_keys(self):
        return self.tree_size * self.batch_size

    def add_root(self):
        self.keys_batches = []
        self.signs_batches = []

        for i in range(0, self.tree_size):
            self.keys_batches.append([self.helpers.get_random_pseudo_key() for j in range(0, self.batch_size)])
            self.signs_batches.append([self.helpers.get_random_pseudo_sign() for j in range(0, self.batch_size)])

        hashes = []

        for i in range(0, self.tree_size):
            keysSignsBytes = b''.join([i.to_bytes(32, 'big')])
            for j in range(0, self.batch_size):
                keysSignsBytes = b''.join([keysSignsBytes, decode_hex(self.keys_batches[i][j]), decode_hex(self.signs_batches[i][j])])
            hash = encode_hex(web3.keccak(keysSignsBytes))
            hashes.append(hash)


        self.tree = MerkleTree(hashes)

        self.add_root_tx = self.merkle_batch_NOR.addMerkleRoot(self.tree.root, self.tree_size, {'from': self.node_operator})
        self.add_root_tx.wait(1)

        self.offset = 0

    def deposit(self, portion):

        batches_to_deposit = portion // self.batch_size
        add_cost = 0
        deposit_cost = 0

        if batches_to_deposit < self.tree_size and batches_to_deposit > self.tree_size - self.offset:
            self.deposit_one_tree((self.tree_size - self.offset) * self.batch_size)  # deposit left keys to trigger adding new root
            return self.deposit_one_tree(portion)
        elif batches_to_deposit < self.tree_size:
            return self.deposit_one_tree(portion)
        elif batches_to_deposit >= self.tree_size and self.offset > 0:
            self.deposit_one_tree((self.tree_size - self.offset) * self.batch_size)  # deposit left keys to trigger adding new root

        for i in range(0, batches_to_deposit // self.tree_size):
            add, deposit = self.deposit_one_tree(self.total_tree_keys)
            add_cost += add
            deposit_cost += deposit

        left_items = batches_to_deposit % self.tree_size

        if left_items > 0:
            add, deposit = self.deposit_one_tree(left_items * self.batch_size)
            add_cost += add
            deposit_cost += deposit

        return add_cost, deposit_cost

    def deposit_one_tree(self, portion):
        batches_to_deposit = portion // self.batch_size
        start = self.offset
        end = self.offset + batches_to_deposit
        keys_portion = flatten(self.keys_batches[start:end])
        signs_portion = flatten(self.signs_batches[start:end])
        proof = self.tree.get_slice_proof(start, end)
        self.merkle_batch_NOR.submit(
            {'from': self.stranger, 'amount': portion * 32 * 10 ** 18}).wait(1)
        deposit_tx = self.merkle_batch_NOR.depositBufferedEther(keys_portion,
                                                        signs_portion,
                                                        proof,
                                                        {'from': self.stranger})

        for j in range(0, batches_to_deposit * self.batch_size):
            assert deposit_tx.events['DepositEvent'][j]['pubkey'] == keys_portion[j]
            assert deposit_tx.events['DepositEvent'][j]['signature'] == signs_portion[j]

        self.offset += batches_to_deposit
        if self.offset == self.tree_size:
            self.add_root()

        return (self.add_root_tx.gas_used, deposit_tx.gas_used)
