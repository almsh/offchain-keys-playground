import pytest
from merkle_tree import MerkleTree
from conftest import Helpers
from eth_abi import encode_single
from eth_utils import encode_hex
from math import floor
from functools import reduce



# def test_encoding(node_operator_registry):
#     tx = node_operator_registry.testEncode(0, '0x01', '0x02')
#     encodedPy = encode_hex(encode_single('(uint256,bytes,bytes)', [0, b'\x01', b'\x02']))
#     assert str(tx) == encodedPy
#
# def test_encode_packed(node_operator_registry):
#     tx = node_operator_registry.testEncodePacked(0, '0x01', '0x02')
#     encodedPy = encode_hex(b''.join([(0).to_bytes(32, 'big'), b'\x01', b'\x02']))
#     assert str(tx) == encodedPy


def test_happy_path(node_operator_registry, node_operator, governance, stranger, helpers: Helpers):

    tree_size = 4

    assert node_operator_registry.totalMerkleRoots() == 0

    keys_and_signs = [(helpers.get_random_pseudo_key(), helpers.get_random_pseudo_sign()) for i in range(0, tree_size)]

    leafs = [helpers.hash_num_key_sign(i, keys_and_signs[i][0], keys_and_signs[i][1]) for i in range(0, tree_size)]

    tree = MerkleTree(leafs)

    tx = node_operator_registry.addMerkleRoot(tree.root, tree_size, {'from': node_operator})
    assert node_operator_registry.totalMerkleRoots() == 1
    print(f'Add merkle root cost {tx.gas_used}')

    node_operator_registry.approveMerkleRoots(1, {'from': governance})
    assert node_operator_registry.approvedRoots() == 1

    node_operator_registry.submit({'from':stranger, 'amount': tree_size * 32 * 10**18})

    keys_and_signs.reverse()
    leafs.reverse()

    tx = node_operator_registry.depositBufferedEther([ks[0] for ks in keys_and_signs], [ks[1] for ks in keys_and_signs], [tree.get_proof(l) for l in leafs] ,{'from': stranger})

    for i in range(0, tree_size):
        assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
        assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

    assert node_operator_registry.usedRoots() == 1


def run_deposit(node_operator_registry, node_operator, governance, stranger, helpers: Helpers, tree_size, portion):

    keys_and_signs = [(helpers.get_random_pseudo_key(), helpers.get_random_pseudo_sign()) for i in range(0, tree_size)]

    leafs = [helpers.hash_num_key_sign(i, keys_and_signs[i][0], keys_and_signs[i][1]) for i in range(0, tree_size)]

    tree = MerkleTree(leafs)

    node_operator_registry.addMerkleRoot(tree.root, tree_size, {'from': node_operator})
    total_roots = node_operator_registry.totalMerkleRoots()

    node_operator_registry.approveMerkleRoots(total_roots + 1, {'from': governance})

    node_operator_registry.submit({'from': stranger, 'amount': tree_size * 32 * 10 ** 18})

    keys_and_signs.reverse()
    leafs.reverse()

    txs = []
    for i in range(0, floor(tree_size/portion)):
        start = i * portion
        end = (i +1) * portion
        keys_and_signs_portion = keys_and_signs[start:end]
        tx = node_operator_registry.depositBufferedEther([ks[0] for ks in keys_and_signs_portion], [ks[1] for ks in keys_and_signs_portion],
                                                     [tree.get_proof(l) for l in leafs[start:end]], {'from': stranger})
        txs.append(tx)

        for j in range(0, portion):
            assert tx.events['DepositEvent'][j]['pubkey'] == keys_and_signs_portion[j][0]
            assert tx.events['DepositEvent'][j]['signature'] == keys_and_signs_portion[j][1]

    return txs


def tx_sum(prev, tx):
    return prev + tx.gas_used

def test_deposits(node_operator_registry, node_operator, governance, stranger, helpers: Helpers):
    for i in range(2, 10):
        tree_size = 2**i
        prices = []
        portions = []
        print(f'{tree_size}, ', end='')
        for j in range(2, i+1):
            portion = 2**j
            portions.append(portion)
            txs = run_deposit(node_operator_registry, node_operator, governance, stranger, helpers, tree_size, portion)
            price = reduce(tx_sum, txs, 0)
            prices.append(price)
            if(j < i):
                print(f'{price}, ', end='')
            else:
                print(f'{price}', end='')
        #print(f',  {", ".join(str(portion) for portion in portions)}')
        #print(f'{tree_size},  {", ".join(str(price) for price in prices)}')
        print('\n', end='')



