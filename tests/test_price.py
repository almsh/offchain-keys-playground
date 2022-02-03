import pytest


def print_dict(dict):
    for key in dict:
        print(f'{str(key)}, {", ".join([str(i) for i in dict[key]])}')


def get_naive_costs(naive):
    print("Naive, ", end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64]:
        add_root_gas, deposit_gas = naive.deposit(i)
        add_root_gas_costs.append(add_root_gas / i)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{deposit_gas / i} {add_root_gas / i},', end='')

    # 128 is too big to calc
    add_root_gas_costs.append(None)
    deposit_gas_costs.append(None)
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_simple_batch_4_costs(simple_batch_4):
    print('SimpleBatch_4,,', end='')
    add_root_gas_costs = [None]
    deposit_gas_costs = [None]
    for i in [4, 8, 32, 64, 128]:
        add_root_gas, deposit_gas = simple_batch_4.deposit(i)
        add_root_gas_costs.append(add_root_gas / i)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{deposit_gas / i} {add_root_gas / i},', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_simple_batch_8_costs(simple_batch_8):
    print('SimpleBatch_8,,,', end='')
    add_root_gas_costs = [None, None]
    deposit_gas_costs = [None, None]
    for i in [8, 32, 64, 128]:
        add_root_gas, deposit_gas = simple_batch_8.deposit(i)
        add_root_gas_costs.append(add_root_gas / i)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{deposit_gas / i} {add_root_gas / i},', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle32_costs(merkle32):
    print('Merkle_32, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64, 128]:
        add_root_gas, deposit_gas = merkle32.deposit(i)
        add_root_gas_costs.append(add_root_gas / ((i // 32 + 1) * 32))
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle128_costs(merkle128):
    print('Merkle_128, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64, 128]:
        add_root_gas, deposit_gas = merkle128.deposit(i)
        add_root_gas_costs.append(add_root_gas / 128)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle256_costs(merkle256):
    print('Merkle_128, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64, 128]:
        add_root_gas, deposit_gas = merkle256.deposit(i)
        add_root_gas_costs.append(add_root_gas / 256)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle512_costs(merkle512):
    print('Merkle_128, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64, 128]:
        add_root_gas, deposit_gas = merkle512.deposit(i)
        add_root_gas_costs.append(add_root_gas / 512)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle1024_costs(merkle1024):
    print('Merkle_128, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64, 128]:
        add_root_gas, deposit_gas = merkle1024.deposit(i)
        add_root_gas_costs.append(add_root_gas / 1024)
        deposit_gas_costs.append(deposit_gas / i)
        print(f'{add_root_gas_costs[-1]} {deposit_gas_costs[-1]}, ', end='')
    print('')
    return add_root_gas_costs, deposit_gas_costs


def get_merkle_batch_costs(merkle_batch):
    print(f'Merkle_batch_{merkle_batch.tree_size}_{merkle_batch.batch_size}, ', end='')
    add_root_gas_costs = []
    deposit_gas_costs = []
    for i in [1, 4, 8, 32, 64, 128]:
        if i < merkle_batch.batch_size:
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


def tes_merkle32_offsets(merkle32):
    deposit_costs = {}
    for j in [2, 4, 8, 16]:
        deposit_costs[str(j)] = []
        for i in range(0, 8):
            if i != 0:
                merkle32.deposit(i)
            add_cost, deposit_cost = merkle32.deposit(j)
            deposit_costs[str(j)].append(deposit_cost / j)
            merkle32.deposit_rest_of_the_tree()
    print_dict(deposit_costs)


def tes_merkle_32(merkle32):
    i = 4
    merkle32.deposit(1)
    add_root_gas, deposit_gas = merkle32.deposit(i)
    add_root_gas_cost = add_root_gas / ((i // 32 + 1) * 32)
    deposit_gas_cost = (deposit_gas / i)
    print(f'Merkle 32 Add {add_root_gas_cost}, deposit {deposit_gas_cost}')


def tes_merkle_batch_32_4(merkle_batch_32_4):
    merkle_batch = merkle_batch_32_4
    i = 128
    add_root_gas, deposit_gas = merkle_batch.deposit(i)
    add_root_gas_cost = add_root_gas / ((i // merkle_batch.total_tree_keys + 1) * merkle_batch.total_tree_keys)
    deposit_gas_cost = deposit_gas / i
    print(f'Batch 32_4 Add {add_root_gas_cost}, deposit {deposit_gas_cost}')


def test_table(naive, simple_batch_4, simple_batch_8, merkle32, merkle128, merkle256, merkle512, merkle1024,
               merkle_batch_32_4, merkle_batch_32_8, merkle_batch_64_8, merkle_batch_128_8, merkle_batch_32_16,
               merkle_batch_64_16):
    add_root_gas = {}
    deposit_gas = {}
    print('Approach\\batch_size, 1, 4, 8, 32, 64, 128')

    naive_add, naive_deposit = get_naive_costs(naive)
    add_root_gas['naive'] = naive_add
    deposit_gas['naive'] = naive_deposit

    simple_batch_4_add, simple_batch_4_deposit = get_simple_batch_4_costs(simple_batch_4)
    add_root_gas['simple_batch_4'] = simple_batch_4_add
    deposit_gas['simple_batch_4'] = simple_batch_4_deposit

    simple_batch_8_add, simple_batch_8_deposit = get_simple_batch_8_costs(simple_batch_8)
    add_root_gas['simple_batch_8'] = simple_batch_8_add
    deposit_gas['simple_batch_8'] = simple_batch_8_deposit

    merkle32_add, merkle32_deposit = get_merkle32_costs(merkle32)
    add_root_gas['merkle32'] = merkle32_add
    deposit_gas['merkle32'] = merkle32_deposit

    merkle128_add, merkle128_deposit = get_merkle128_costs(merkle128)
    add_root_gas['merkle128'] = merkle128_add
    deposit_gas['merkle128'] = merkle128_deposit

    merkle256_add, merkle256_deposit = get_merkle256_costs(merkle256)
    add_root_gas['merkle256'] = merkle256_add
    deposit_gas['merkle256'] = merkle256_deposit

    merkle512_add, merkle512_deposit = get_merkle512_costs(merkle512)
    add_root_gas['merkle512'] = merkle512_add
    deposit_gas['merkle512'] = merkle512_deposit

    merkle1024_add, merkle1024_deposit = get_merkle1024_costs(merkle1024)
    add_root_gas['merkle1024'] = merkle1024_add
    deposit_gas['merkle1024'] = merkle1024_deposit

    batch_32_4_add, batch_32_4_deposit = get_merkle_batch_costs(merkle_batch_32_4)
    add_root_gas['batch_32_4'] = batch_32_4_add
    deposit_gas['batch_32_4'] = batch_32_4_deposit

    batch_32_8_add, batch_32_8_deposit = get_merkle_batch_costs(merkle_batch_32_8)
    add_root_gas['batch_32_8'] = batch_32_8_add
    deposit_gas['batch_32_8'] = batch_32_8_deposit

    batch_64_8_add, batch_64_8_deposit = get_merkle_batch_costs(merkle_batch_64_8)
    add_root_gas['batch_64_8'] = batch_64_8_add
    deposit_gas['batch_64_8'] = batch_64_8_deposit

    batch_128_8_add, batch_128_8_deposit = get_merkle_batch_costs(merkle_batch_128_8)
    add_root_gas['batch_128_8'] = batch_128_8_add
    deposit_gas['batch_128_8'] = batch_128_8_deposit

    batch_32_16_add, batch_32_16_deposit = get_merkle_batch_costs(merkle_batch_32_16)
    add_root_gas['batch_32_16'] = batch_32_16_add
    deposit_gas['batch_32_16'] = batch_32_16_deposit

    batch_64_16_add, batch_64_16_deposit = get_merkle_batch_costs(merkle_batch_64_16)
    add_root_gas['batch_64_16'] = batch_64_16_add
    deposit_gas['batch_64_16'] = batch_64_16_deposit

    print('Add root')
    print_dict(add_root_gas)
    print('Deposit')
    print_dict(deposit_gas)
