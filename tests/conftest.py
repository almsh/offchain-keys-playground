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
def merkle_NOR(deployer, node_operator, deposit_contract, MerkleNOR):
    return MerkleNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})

@pytest.fixture(scope='module')
def merkle_batch_NOR(deployer, node_operator, deposit_contract, MerkleBatchNOR):
    return MerkleBatchNOR.deploy(node_operator, deposit_contract.address, {'from': deployer})


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
def merkle(merkle_NOR, node_operator, stranger, helpers: Helpers):
    return Merkle(merkle_NOR, node_operator, stranger, helpers)

@pytest.fixture(scope='module')
def merkle_batch(merkle_batch_NOR, node_operator, stranger, helpers: Helpers):
    return MerkleBatch(merkle_batch_NOR, node_operator, stranger, helpers)