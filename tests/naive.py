import pytest
from functools import reduce


def tx_sum(prev, tx):
    return prev + tx.gas_used

class Naive:
    def __init__(self, naive_NOR, node_operator, stranger, helpers):
        self.naive_NOR = naive_NOR
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers



    def deposit(self, keys_amount):
        txs = []

        keys_and_signs = [(self.helpers.get_random_pseudo_key(), self.helpers.get_random_pseudo_sign()) for i in range(0, keys_amount)]


        tx = self.naive_NOR.addPubkeysAndSignatures([ks[0] for ks in keys_and_signs],[ks[1] for ks in keys_and_signs], {'from': self.node_operator});
        txs.append(tx)

        self.naive_NOR.submit({'from':self.stranger, 'amount': keys_amount * 32 * 10**18})

        tx = self.naive_NOR.depositBufferedEther(keys_amount ,{'from': self.stranger})
        txs.append(tx)

        for i in range(0, keys_amount):
            assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
            assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

        return reduce(tx_sum, txs, 0)
