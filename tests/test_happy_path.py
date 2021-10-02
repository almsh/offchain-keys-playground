import pytest
from merkle_tree import MerkleTree
from conftest import Helpers
from eth_abi import encode_single
from eth_utils import encode_hex



def test_encoding(node_operator_registry):
    tx = node_operator_registry.testEncode(0, '0x01', '0x02')
    encodedPy = encode_hex(encode_single('(uint256,bytes,bytes)', [0, b'\x01', b'\x02']))
    assert str(tx) == encodedPy

def test_encode_packed(node_operator_registry):
    tx = node_operator_registry.testEncodePacked(0, '0x01', '0x02')
    encodedPy = encode_hex(b''.join([(0).to_bytes(32, 'big'), b'\x01', b'\x02']))
    assert str(tx) == encodedPy


def test_happy_path(node_operator_registry, node_operator, governance, stranger, helpers: Helpers):
    assert node_operator_registry.totalMerkleRoots() == 0

    keys_and_signs = [(helpers.get_random_pseudo_key(), helpers.get_random_pseudo_sign()) for i in range(0, 4)]

    leafs = [helpers.hash_num_key_sign(i, keys_and_signs[i][0], keys_and_signs[i][1]) for i in range(0, 4)]

    tree = MerkleTree(leafs)

    node_operator_registry.addMerkleRoot(tree.root, {'from': node_operator})
    assert node_operator_registry.totalMerkleRoots() == 1

    node_operator_registry.approveMerkleRoots(1, {'from': governance})
    assert node_operator_registry.approvedRoots() == 1

    node_operator_registry.submit({'from':stranger, 'amount': 5 * 32 * 10**18})

    tx = node_operator_registry.depositBufferedEther([ks[0] for ks in keys_and_signs], [ks[1] for ks in keys_and_signs], [tree.get_proof(l) for l in leafs] ,{'from': stranger})

    for i in range(0, 4):
        assert tx.events['DepositEvent'][i]['pubkey'] == keys_and_signs[i][0]
        assert tx.events['DepositEvent'][i]['signature'] == keys_and_signs[i][1]

    assert node_operator_registry.usedRoots() == 1
