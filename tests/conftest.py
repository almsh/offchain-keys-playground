import pytest
from brownie import web3
from secrets import token_hex
from eth_utils import encode_hex, to_bytes
from eth_abi import encode_single

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

