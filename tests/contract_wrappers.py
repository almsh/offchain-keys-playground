from tests.helpers import Helpers
from tests.merkle import Merkle
from tests.merkle_batch import MerkleBatch
from tests.naive import Naive
from tests.node_operator_contracts import NodeOperatorContracts
from tests.simple_batch import SimpleBatch


class ContractWrappers:
    def __init__(self, node_operator_contracts: NodeOperatorContracts, node_operator, stranger, helpers: Helpers):
        self.node_operator_contracts = node_operator_contracts
        self.node_operator = node_operator
        self.stranger = stranger
        self.helpers = helpers

    def create_naive_wrapper(self):
        naive_NOR = self.node_operator_contracts.deploy_naive_NOR()
        return Naive(naive_NOR, self.node_operator, self.stranger, self.helpers)

    def create_simple_batch_wrapper(self, batch_size):
        simple_batch_NOR = self.node_operator_contracts.deploy_simple_batch_NOR(batch_size)
        return SimpleBatch(simple_batch_NOR, self.node_operator, self.stranger, self.helpers, batch_size)

    def create_merkle_wrapper(self, tree_size):
        merkle_NOR = self.node_operator_contracts.deploy_merkle_NOR()
        return Merkle(merkle_NOR, self.node_operator, self.stranger, self.helpers, tree_size)

    def create_merkle_batch_wrapper(self, tree_size, batch_size):
        merkle_batch_NOR = self.node_operator_contracts.deploy_merkle_batch_NOR_64_16(batch_size)
        return MerkleBatch(merkle_batch_NOR, self.node_operator, self.stranger, self.helpers, tree_size, batch_size)