import pytest

BETH_DECIMALS = 18
UST_TOKEN = '0xa47c8bf37f92aBed4A126BDA807A7b7498661acD'

@pytest.fixture(scope='module')
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope='module')
def governance(accounts):
    return accounts[1]

@pytest.fixture(scope='module')
def node_operator(accounts):
    return accounts[2]

@pytest.fixture(scope='module')
def stranger(accounts):
    return accounts[3]

@pytest.fixture(scope='module')
def deposit_contract(deployer, DepositContractMock):
    return DepositContractMock.deploy({'from': deployer})

@pytest.fixture(scope='module')
def node_operator_registry(deployer, node_operator, governance, deposit_contract, DummyNodeOperatorsRegistry):
    return DummyNodeOperatorsRegistry.deploy(node_operator, governance, deposit_contract.address, {'from': deployer})
