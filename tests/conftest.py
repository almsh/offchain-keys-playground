import pytest
from brownie import web3
from secrets import token_hex
from eth_utils import encode_hex, to_bytes
from eth_abi import encode_single

from tests.naive import Naive
from tests.simple_batch import SimpleBatch

BETH_DECIMALS = 18
UST_TOKEN = '0xa47c8bf37f92aBed4A126BDA807A7b7498661acD'

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


class Helpers:
    @staticmethod
    def get_random_pseudo_key():
        return '0x' + token_hex(48)

    @staticmethod
    def get_random_pseudo_sign():
        return '0x' + token_hex(96)

    @staticmethod
    def hash_num_key_sign(num: int, key: str, sign: str):
        return encode_hex(web3.keccak(b''.join([num.to_bytes(32, 'big'), to_bytes(hexstr=key), to_bytes(hexstr=sign)])))


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

