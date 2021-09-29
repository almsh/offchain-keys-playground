import pytest

PUBKEY = '0x86ba17890f9e2190d6d8666124583858fb0c8f3135cc99b3a637ad5ca00b3aabe358e64fb4888554881158105234dea1'
SIGNATURE = '0x8f486ac2d89e911ece802a9a8a15a537ac0f1f10578b6b3e4db43edda57cf8e7ac87914c51ef89eb8da271d1c2206aee014716b97e6676a3daa699e4672f764787a2d845170c9a7ee37326420c935271b80dee7fc83bd44598d73dd86f53d6f6'

def test_happy_path(node_operator_registry, node_operator, governance, stranger):
    assert node_operator_registry.totalKeys() == 0
    node_operator_registry.addSigningKey(PUBKEY, SIGNATURE, {'from': node_operator})
    assert node_operator_registry.totalKeys() == 1
    node_operator_registry.approveSigningKeys(1, {'from': governance})
    assert node_operator_registry.approvedKeys() == 1
    node_operator_registry.submit({'from':stranger, 'amount': 64 * 10**18})
    assert node_operator_registry.balance1() > 32 * 10 ** 18
    tx = node_operator_registry.depositBufferedEther({'from': stranger})
    assert tx.events['DepositEvent']['pubkey'] == PUBKEY
    assert tx.events['DepositEvent']['signature'] == SIGNATURE


