import pytest

from tests.contract_wrappers import ContractWrappers
from tests.helpers import Helpers
from tests.merkle import Merkle
from tests.merkle_batch import MerkleBatch
from tests.naive import Naive
from tests.node_operator_contracts import NodeOperatorContracts
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
def helpers():
    return Helpers

@pytest.fixture(scope='module')
def node_operator_contracts(deployer, node_operator, deposit_contract, NaiveNOR, SimpleBatchNOR, MerkleNOR, MerkleBatchNOR):
    return NodeOperatorContracts(deployer, node_operator, deposit_contract, NaiveNOR, SimpleBatchNOR, MerkleNOR, MerkleBatchNOR)

@pytest.fixture(scope='module')
def contract_wrappers(node_operator_contracts, node_operator, stranger, helpers):
    return ContractWrappers(node_operator_contracts, node_operator, stranger, helpers)