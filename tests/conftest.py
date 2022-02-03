import pytest
from tests.helpers import Helpers
from tests.merkle import Merkle
from tests.merkle_batch import MerkleBatch
from tests.naive import Naive
from tests.simple_batch import SimpleBatch

@pytest.fixture(scope='module')
def deployer(accounts):
    return accounts[0]

@pytest.fixture(scope='module')
def node_operator(accounts):
    return accounts[1]

@pytest.fixture(scope='module')
def stranger(accounts):
    return accounts[2]

@pytest.fixture(scope='module')
def deposit_contract(deployer, DepositContractMock):
    return DepositContractMock.deploy({'from': deployer})

@pytest.fixture(scope='module')
def node_operator_registry(deployer, node_operator, deposit_contract, DummyNodeOperatorsRegistry):
    return DummyNodeOperatorsRegistry.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def naive_NOR(deployer, node_operator, deposit_contract, NaiveNOR):
    return NaiveNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def simple_batch_4_NOR(deployer, node_operator, deposit_contract, SimpleBatchNOR):
    return SimpleBatchNOR.deploy(node_operator, deposit_contract.address, 4, {'from': deployer})

@pytest.fixture(scope='module')
def simple_batch_8_NOR(deployer, node_operator, deposit_contract, SimpleBatchNOR):
    return SimpleBatchNOR.deploy(node_operator, deposit_contract.address, 8, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_NOR32(deployer, node_operator, deposit_contract, MerkleNOR):
    return MerkleNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_NOR128(deployer, node_operator, deposit_contract, MerkleNOR):
    return MerkleNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_NOR256(deployer, node_operator, deposit_contract, MerkleNOR):
    return MerkleNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_NOR512(deployer, node_operator, deposit_contract, MerkleNOR):
    return MerkleNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_NOR1024(deployer, node_operator, deposit_contract, MerkleNOR):
    return MerkleNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR_32_4(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, 4, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR_32_8(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, 8, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR_64_8(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, 8, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR_128_8(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, 8, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR_32_16(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, 16, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR_64_16(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, 16, {'from': deployer})


@pytest.fixture(scope='module')
def helpers():
    return Helpers


@pytest.fixture(scope='module')
def naive(naive_NOR, node_operator, stranger, helpers: Helpers):
    return Naive(naive_NOR, node_operator, stranger, helpers)

@pytest.fixture(scope='module')
def simple_batch_4(simple_batch_4_NOR, node_operator, stranger, helpers: Helpers):
    return SimpleBatch(simple_batch_4_NOR, node_operator, stranger, helpers, 4)

@pytest.fixture(scope='module')
def simple_batch_8(simple_batch_8_NOR, node_operator, stranger, helpers: Helpers):
    return SimpleBatch(simple_batch_8_NOR, node_operator, stranger, helpers, 8)

@pytest.fixture(scope='module')
def merkle32(merkle_NOR32, node_operator, stranger, helpers: Helpers):
    return Merkle(merkle_NOR32, node_operator, stranger, helpers, 32)

@pytest.fixture(scope='module')
def merkle128(merkle_NOR128, node_operator, stranger, helpers: Helpers):
    return Merkle(merkle_NOR128, node_operator, stranger, helpers, 128)

@pytest.fixture(scope='module')
def merkle256(merkle_NOR256, node_operator, stranger, helpers: Helpers):
    return Merkle(merkle_NOR256, node_operator, stranger, helpers, 256)

@pytest.fixture(scope='module')
def merkle512(merkle_NOR512, node_operator, stranger, helpers: Helpers):
    return Merkle(merkle_NOR512, node_operator, stranger, helpers, 512)

@pytest.fixture(scope='module')
def merkle1024(merkle_NOR1024, node_operator, stranger, helpers: Helpers):
    return Merkle(merkle_NOR1024, node_operator, stranger, helpers, 1024)

@pytest.fixture(scope='module')
def merkle_batch_32_4(merkle_batch_NOR_32_4, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR_32_4, node_operator, stranger, helpers, 32, 4)

@pytest.fixture(scope='module')
def merkle_batch_32_8(merkle_batch_NOR_32_8, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR_32_8, node_operator, stranger, helpers, 32, 8)

@pytest.fixture(scope='module')
def merkle_batch_64_8(merkle_batch_NOR_64_8, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR_64_8, node_operator, stranger, helpers, 64, 8)

@pytest.fixture(scope='module')
def merkle_batch_128_8(merkle_batch_NOR_128_8, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR_128_8, node_operator, stranger, helpers, 128, 8)

@pytest.fixture(scope='module')
def merkle_batch_32_16(merkle_batch_NOR_32_16, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR_32_16, node_operator, stranger, helpers, 32, 16)

@pytest.fixture(scope='module')
def merkle_batch_64_16(merkle_batch_NOR_64_16, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR_64_16, node_operator, stranger, helpers, 64, 16)