import pytest

from tests.contract_wrappers import ContractWrappers


def print_dict(dict):
    for key in dict:
        print(f'{str(key)}, {", ".join([str(i) for i in dict[key]])}')


def get_naive_costs(contract_wrappers: ContractWrappers):
    print("Naive, ", end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    naive = contract_wrappers.create_naive_wrapper()
    for i in [1, 4, 8, 16, 32, 64]:
        add_root_gas, deposit_gas = naive.deposit(i)
        add_root_gas_costs.append(add_root_gas / i)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{deposit_gas / i} {add_root_gas / i},', end='')

    # 128, 256 and 512 is too big to calc
    add_root_gas_costs += [None, None, None]
    deposit_gas_costs += [None, None, None]
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_simple_batch_4_costs(contract_wrappers: ContractWrappers):
    print('SimpleBatch_4,,', end='')
    add_root_gas_costs = [None]
    deposit_gas_costs = [None]
    simple_batch_4 = contract_wrappers.create_simple_batch_wrapper(4)
    for i in [4, 8, 16, 32, 64, 128, 256, 512]:
        add_root_gas, deposit_gas = simple_batch_4.deposit(i)
        add_root_gas_costs.append(add_root_gas / i)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{deposit_gas / i} {add_root_gas / i},', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_simple_batch_8_costs(contract_wrappers: ContractWrappers):
    print('SimpleBatch_8,,,', end='')
    add_root_gas_costs = [None, None]
    deposit_gas_costs = [None, None]
    simple_batch_8 = contract_wrappers.create_simple_batch_wrapper(8)
    for i in [8, 16, 32, 64, 128, 256, 512]:
        add_root_gas, deposit_gas = simple_batch_8.deposit(i)
        add_root_gas_costs.append(add_root_gas / i)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{deposit_gas / i} {add_root_gas / i},', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle_costs(contract_wrappers: ContractWrappers, tree_size: int):
    print(f'Merkle_{str(tree_size)}, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    merkle512 = contract_wrappers.create_merkle_wrapper(tree_size)
    for i in [1, 4, 8, 16, 32, 64, 128, 256, 512]:
        if i > tree_size:
            add_root_gas_costs.append(None)
            deposit_gas_costs.append(None)
        else:
            add_root_gas, deposit_gas = merkle512.deposit(i)
            add_root_gas_costs.append(add_root_gas / tree_size)
            deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle_batch_costs(contract_wrappers: ContractWrappers, tree_size, batch_size):
    print(f'Merkle_batch_{tree_size}_{batch_size}, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    merkle_batch = contract_wrappers.create_merkle_batch_wrapper(tree_size, batch_size)
    for i in [1, 4, 8, 16, 32, 64, 128, 256, 512]:
        if i < batch_size:
            add_root_gas_costs.append(None)
            deposit_gas_costs.append(None)
        else:
            add_root_gas, deposit_gas = merkle_batch.deposit(i)
            add_root_gas_costs.append(
                add_root_gas / ((i // merkle_batch.total_tree_keys + 1) * merkle_batch.total_tree_keys))
            deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def test_table(contract_wrappers: ContractWrappers):
    add_root_gas = {}
    deposit_gas = {}
    print('Approach\\batch_size, 1, 4, 8, 16, 32, 64, 128, 256, 512')

    naive_add, naive_deposit = get_naive_costs(contract_wrappers)
    add_root_gas['naive'] = naive_add
    deposit_gas['naive'] = naive_deposit

    simple_batch_4_add, simple_batch_4_deposit = get_simple_batch_4_costs(contract_wrappers)
    add_root_gas['simple_batch_4'] = simple_batch_4_add
    deposit_gas['simple_batch_4'] = simple_batch_4_deposit

    for i in range(6, 13):
        size = 2 ** i
        merkle_add, merkle_deposit = get_merkle_costs(contract_wrappers, size)
        add_root_gas[f'merkle{size}'] = merkle_add
        deposit_gas[f'merkle{size}'] = merkle_deposit

    batch_64_8_add, batch_64_8_deposit = get_merkle_batch_costs(contract_wrappers, 64, 8)
    add_root_gas['batch_64_8'] = batch_64_8_add
    deposit_gas['batch_64_8'] = batch_64_8_deposit

    batch_64_16_add, batch_64_16_deposit = get_merkle_batch_costs(contract_wrappers, 64, 16)
    add_root_gas['batch_64_16'] = batch_64_16_add
    deposit_gas['batch_64_16'] = batch_64_16_deposit

    batch_128_8_add, batch_128_8_deposit = get_merkle_batch_costs(contract_wrappers, 128, 8)
    add_root_gas['batch_128_8'] = batch_128_8_add
    deposit_gas['batch_128_8'] = batch_128_8_deposit

    batch_128_16_add, batch_128_16_deposit = get_merkle_batch_costs(contract_wrappers, 128, 16)
    add_root_gas['batch_128_16'] = batch_128_16_add
    deposit_gas['batch_128_16'] = batch_128_16_deposit

    print('Add root')
    print_dict(add_root_gas)
    print('Deposit')
    print_dict(deposit_gas)
