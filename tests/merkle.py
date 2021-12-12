from tests.merkle_tree import MerkleTree


class Merkle:
    def __init__(self, merkle_NOR, node_operator, stranger, helpers, tree_size):
        self.merkle_NOR = merkle_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers
        self.tree_size = tree_size
        self.offset = 0
        self.add_root()
       
    def add_root(self):
        self.keys_and_signs = [(self.helpers.get_random_pseudo_key(), self.helpers.get_random_pseudo_sign()) for i in
                               range(0, self.tree_size)]
        self.leafs = [self.helpers.hash_num_key_sign(i, self.keys_and_signs[i][0], self.keys_and_signs[i][1]) for i in
                      range(0, self.tree_size)]
        self.tree = MerkleTree(self.leafs)

        self.add_root_tx = self.merkle_NOR.addMerkleRoot(self.tree.root, self.tree_size, {'from': self.node_operator})
        self.add_root_tx.wait(1)
        self.merkle_NOR.submit({'from': self.stranger, 'amount': self.tree_size * 32 * 10 ** 18}).wait(1)
        self.offset = 0

    def deposit(self, portion):
        start = self.offset
        end = portion + self.offset
        keys_and_signs_portion = self.keys_and_signs[start:end]
        proof = self.tree.get_slice_proof(start, end)
        deposit_tx = self.merkle_NOR.depositBufferedEther([ks[0] for ks in keys_and_signs_portion],
                                                         [ks[1] for ks in keys_and_signs_portion],
                                                         proof,
                                                         {'from': self.stranger})
        deposit_tx.wait(1)

        for j in range(0, portion):
            assert deposit_tx.events['DepositEvent'][j]['pubkey'] == keys_and_signs_portion[j][0]
            assert deposit_tx.events['DepositEvent'][j]['signature'] == keys_and_signs_portion[j][1]

        self.offset += portion
        if self.offset == self.tree_size:
            self.add_root()

        return (self.add_root_tx.gas_used, deposit_tx.gas_used)
