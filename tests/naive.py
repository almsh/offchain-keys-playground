import pytest
from functools import reduce

from tests.tx_sum import tx_sum


class Naive:
    def __init__(self, naive_NOR, node_operator, stranger, helpers):
        self.naive_NOR = naive_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers



    def deposit(self, keys_amount):
        add_root_txs = []
        deposit_txs = []

        keys_and_signs = [(self.helpers.get_random_pseudo_key(), self.helpers.get_random_pseudo_sign()) for i in range(0, keys_amount)]


        tx = self.naive_NOR.addPubkeysAndSignatures([ks[0] for ks in keys_and_signs],[ks[1] for ks in keys_and_signs], {'from': self.node_operator});
        add_root_txs.append(tx)

        self.naive_NOR.submit({'from':self.stranger, 'amount': keys_amount * 32 * 10**18})

        tx = self.naive_NOR.depositBufferedEther(keys_amount ,{'from': self.stranger})
        deposit_txs.append(tx)

        for i in range(0, keys_amount):
            assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
            assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

        return reduce(tx_sum, add_root_txs, 0), reduce(tx_sum, deposit_txs, 0)
