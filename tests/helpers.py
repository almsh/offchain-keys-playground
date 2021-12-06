from secrets import token_hex

from brownie import web3
from eth_utils import encode_hex, to_bytes


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