import pytest

def test_naive_1(naive):
    keys_amount = 1
    gas_used = naive.deposit(keys_amount)
    print(f'Naive {keys_amount}: {gas_used/keys_amount}')


def test_simple_batch_4_32(simple_batch_4):
    keys_amount = 32
    gas_used = simple_batch_4.deposit(keys_amount)
    print(f'simple batch {keys_amount}: {gas_used/keys_amount}')

def test_simple_batch_8_32(simple_batch_8):
    keys_amount = 32
    gas_used = simple_batch_8.deposit(keys_amount)
    print(f'simple batch {keys_amount}: {gas_used/keys_amount}')