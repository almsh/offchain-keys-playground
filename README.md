# Lido offchain keys experiment

To run deposit price tests, clone repository and run [brownie](https://github.com/eth-brownie/brownie) tests with [ganache](https://github.com/trufflesuite/ganache).

```sh
git clone https://github.com/almsh/offchain-keys-playground.git
brownie compile
WEB3_INFURA_PROJECT_ID=%infura_project_id% PYTHONUNBUFFERED=1 brownie test -s
```

This outputs csv formatted gas usage data for keys usage for different storage methods (Naive, Batch, Merkle, Merkle+Batch), separatly for adding and deposit.
