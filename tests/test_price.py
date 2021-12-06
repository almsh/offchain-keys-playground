import pytest

def test_table(naive, simple_batch_4, simple_batch_8, merkle, merkle_batch):
    print('Approach\\batch_size, 1, 4, 8, 32, 64')
    print("Naive, ", end='')
    for i in [1, 4, 8, 32, 64]:
        if i != 64:
            print(f'{naive.deposit(i)/i},', end='')
        else:
            print(f'{naive.deposit(i)/i}')

    print('SimpleBatch_4,,', end='')
    for i in [4, 8, 32, 64]:
        if i != 64:
            print(f'{simple_batch_4.deposit(i)/i}, ', end='')
        else:
            print(f'{simple_batch_4.deposit(i)/i}')

    print('SimpleBatch_8,,,', end='')
    for i in [8, 32, 64]:
        if i != 64:
            print(f'{simple_batch_4.deposit(i) / i}, ', end='')
        else:
            print(f'{simple_batch_4.deposit(i) / i}')

    print('Merkle_32, ', end='')
    for i in [1, 4, 8, 32, 64]:
        if i != 64:
            print(f'{merkle.deposit(32, i) / 32}, ', end='')
        else:
            print(f',')

    print('Merkle_128, ', end='')
    for i in [1, 4, 8, 32, 64]:
        if i != 64:
            print(f'{merkle.deposit(128, i) / 128}, ', end='')
        else:
            print(f'{merkle.deposit(128, i) / 128}')

    print('MerkleBatch_32_4,,', end='')
    for i in [1, 2, 8, 16]:
        if i != 16:
            print(f'{merkle_batch.deposit(4, 32, i) / 128}, ', end='')
        else:
            print(f'{merkle_batch.deposit(4, 32, i) / 128}')

    print('MerkleBatch_32_8,,,', end='')
    for i in [1, 4, 8]:
        if i != 8:
            print(f'{merkle_batch.deposit(8, 32, i) / 256}, ', end='')
        else:
            print(f'{merkle_batch.deposit(8, 32, i) / 256}')

    print('MerkleBatch_64_8,,,', end='')
    for i in [1, 4, 8]:
        if i != 8:
            print(f'{merkle_batch.deposit(8, 64, i) / 512}, ', end='')
        else:
            print(f'{merkle_batch.deposit(8, 64, i) / 512}')
