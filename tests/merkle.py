from functools import reduce
from math import floor

from tests.merkle_tree import MerkleTree
from tests.tx_sum import tx_sum


class Merkle:
    def __init__(self, merkle_NOR, node_operator, stranger, helpers):
        self.merkle_NOR = merkle_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers


    def deposit(self, tree_size, portion):

        keys_and_signs = [(self.helpers.get_random_pseudo_key(), self.helpers.get_random_pseudo_sign()) for i in
                          range(0, tree_size)]

        leafs = [self.helpers.hash_num_key_sign(i, keys_and_signs[i][0], keys_and_signs[i][1]) for i in range(0, tree_size)]

        tree = MerkleTree(leafs)

        self.merkle_NOR.addMerkleRoot(tree.root, tree_size, {'from': self.node_operator})

        self.merkle_NOR.submit({'from': self.stranger, 'amount': tree_size * 32 * 10 ** 18})

        keys_and_signs.reverse()
        leafs.reverse()

        txs = []
        for i in range(0, floor(tree_size / portion)):
            start = i * portion
            end = (i + 1) * portion
            keys_and_signs_portion = keys_and_signs[start:end]
            tx = self.merkle_NOR.depositBufferedEther([ks[0] for ks in keys_and_signs_portion],
                                                             [ks[1] for ks in keys_and_signs_portion],
                                                             [tree.get_proof(l) for l in leafs[start:end]],
                                                             {'from': self.stranger})
            txs.append(tx)

            for j in range(0, portion):
                assert tx.events['DepositEvent'][j]['pubkey'] == keys_and_signs_portion[j][0]
                assert tx.events['DepositEvent'][j]['signature'] == keys_and_signs_portion[j][1]

        return reduce(tx_sum, txs, 0)
