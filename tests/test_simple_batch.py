import pytest
from conftest import Helpers
from functools import reduce
from brownie import web3
from eth_abi import encode_abi
from math import floor
from eth_utils import decode_hex, encode_hex


def tx_sum(prev, tx):
    return prev + tx.gas_used

def run_simple_batch_deposit(simple_batch_NOR, node_operator, stranger, helpers: Helpers, batch_size, keys_amount):
    txs = []

    keys_and_signs = [(helpers.get_random_pseudo_key(), helpers.get_random_pseudo_sign()) for i in range(0, keys_amount)]

    keys = [ks[0] for ks in keys_and_signs]
    signs = [ks[1] for ks in keys_and_signs]

    hashes = []

    for i in range(0, floor(keys_amount/batch_size)):
        start = batch_size * i
        end = batch_size * (i + 1)
        keysSignsBytes = b''
        for j in range(start, end):
            keysSignsBytes = b''.join([keysSignsBytes,decode_hex(keys[j]), decode_hex(signs[j])])
        hash = web3.keccak(keysSignsBytes)
        hashes.append(hash)


    tx = simple_batch_NOR.addPubkeysAndSignsHashes(hashes, {'from': node_operator});
    txs.append(tx)

    simple_batch_NOR.submit({'from':stranger, 'amount': keys_amount * 32 * 10**18})

    tx = simple_batch_NOR.depositBufferedEther(keys, signs,{'from': stranger})
    txs.append(tx)

    for i in range(0, keys_amount):
        assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
        assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

    return reduce(tx_sum, txs, 0)


def test_simple_batch_4_4(simple_batch_4_NOR, node_operator, stranger, helpers: Helpers):
    batch_size = 4
    keys_amount = 4
    gas_used = run_simple_batch_deposit(simple_batch_4_NOR, node_operator, stranger, helpers, batch_size, keys_amount)
    print(f'simple batch {batch_size} {keys_amount}: {gas_used/keys_amount}')


def test_simple_batch_4_8(simple_batch_4_NOR, node_operator, stranger, helpers: Helpers):
    batch_size = 4
    keys_amount = 8
    gas_used = run_simple_batch_deposit(simple_batch_4_NOR, node_operator, stranger, helpers, batch_size, keys_amount)
    print(f'simple batch {batch_size} {keys_amount}: {gas_used/keys_amount}')

def test_simple_batch_4_32(simple_batch_4_NOR, node_operator, stranger, helpers: Helpers):
    batch_size = 4
    keys_amount = 32
    gas_used = run_simple_batch_deposit(simple_batch_4_NOR, node_operator, stranger, helpers, batch_size, keys_amount)
    print(f'simple batch {batch_size} {keys_amount}: {gas_used/keys_amount}')

def test_simple_batch_4_64(simple_batch_4_NOR, node_operator, stranger, helpers: Helpers):
    batch_size = 4
    keys_amount = 64
    gas_used = run_simple_batch_deposit(simple_batch_4_NOR, node_operator, stranger, helpers, batch_size, keys_amount)
    print(f'simple batch {batch_size} {keys_amount}: {gas_used/keys_amount}')

