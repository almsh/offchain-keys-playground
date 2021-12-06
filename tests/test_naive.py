import pytest
from conftest import Helpers
from functools import reduce


def tx_sum(prev, tx):
    return prev + tx.gas_used

def run_naive_NOR_deposit(naive_NOR, node_operator, stranger, helpers: Helpers, keys_amount):
    txs = []

    keys_and_signs = [(helpers.get_random_pseudo_key(), helpers.get_random_pseudo_sign()) for i in range(0, keys_amount)]


    tx = naive_NOR.addPubkeysAndSignatures([ks[0] for ks in keys_and_signs],[ks[1] for ks in keys_and_signs], {'from': node_operator});
    txs.append(tx)

    naive_NOR.submit({'from':stranger, 'amount': keys_amount * 32 * 10**18})

    tx = naive_NOR.depositBufferedEther(keys_amount ,{'from': stranger})
    txs.append(tx)

    for i in range(0, keys_amount):
        assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
        assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

    return reduce(tx_sum, txs, 0)



def test_naive_1_key(naive_NOR, node_operator, stranger, helpers: Helpers):
    keys_amount = 1
    gas_used = run_naive_NOR_deposit(naive_NOR, node_operator, stranger, helpers, keys_amount)
    print(f'Naive approach {keys_amount} {gas_used/keys_amount} per key')

def test_naive_4_key(naive_NOR, node_operator, stranger, helpers: Helpers):
    keys_amount = 4
    gas_used = run_naive_NOR_deposit(naive_NOR, node_operator, stranger, helpers, keys_amount)
    print(f'Naive approach {keys_amount} {gas_used/keys_amount} per key')

def test_naive_8_key(naive_NOR, node_operator, stranger, helpers: Helpers):
    keys_amount = 8
    gas_used = run_naive_NOR_deposit(naive_NOR, node_operator, stranger, helpers, keys_amount)
    print(f'Naive approach {keys_amount} {gas_used/keys_amount} per key')

def test_naive_32_key(naive_NOR, node_operator, stranger, helpers: Helpers):
    keys_amount = 32
    gas_used = run_naive_NOR_deposit(naive_NOR, node_operator, stranger, helpers, keys_amount)
    print(f'Naive approach {keys_amount} {gas_used/keys_amount} per key')

def test_naive_64_key(naive_NOR, node_operator, stranger, helpers: Helpers):
    keys_amount = 64
    gas_used = run_naive_NOR_deposit(naive_NOR, node_operator, stranger, helpers, keys_amount)
    print(f'Naive approach {keys_amount} {gas_used/keys_amount} per key')
