

class NodeOperatorContracts:
    def __init__(self, deployer, node_operator, deposit_contract_adress, NaiveNOR, SimpleBatchNOR, MerkleNOR, MerkleBatchNOR):
        self.deployer = deployer
        self.node_operator = node_operator
        self.deposit_contract_address = deposit_contract_adress
        self.NaiveNOR = NaiveNOR
        self.SimpleBatchNOR = SimpleBatchNOR
        self.MerkleNOR = MerkleNOR
        self.MerkleBatchNOR = MerkleBatchNOR

    def deploy_naive_NOR(self):
        return self.NaiveNOR.deploy(self.node_operator, self.deposit_contract_address, {'from': self.deployer})

    def deploy_simple_batch_NOR(self, batch_size):
        return self.SimpleBatchNOR.deploy(self.node_operator, self.deposit_contract_address, batch_size, {'from': self.deployer})


    def deploy_merkle_NOR(self):
        return self.MerkleNOR.deploy(self.node_operator, self.deposit_contract_address, {'from': self.deployer})

    def deploy_merkle_batch_NOR_64_16(self, batch_size):
        return self.MerkleBatchNOR.deploy(self.node_operator, self.deposit_contract_address, batch_size, {'from': self.deployer})
