from itertools import zip_longest

from brownie import web3
from eth_utils import encode_hex, to_bytes

class MerkleTree:
    def __init__(self, elements):
        self.elements = [web3.keccak(hexstr=el) for el in elements]
        self.layers = MerkleTree.get_layers(self.elements)

    @property
    def root(self):
        return self.layers[-1][0]

    def get_proof(self, el):
        el = web3.keccak(hexstr=el)
        idx = self.elements.index(el)
        proof = []
        for layer in self.layers:
            pair_idx = idx + 1 if idx % 2 == 0 else idx - 1
            if pair_idx < len(layer):
                proof.append(encode_hex(layer[pair_idx]))
            idx //= 2
        return proof

    def get_slice_proof(self, start, end):
        start_index = start
        end_index = end - 1
        proof = []

        for layer in self.layers:
            if start_index % 2 == 1:
                proof.append(encode_hex(layer[start_index - 1]))

            if end_index % 2 == 0 and len(layer) > end_index + 1:
                proof.append(encode_hex(layer[end_index + 1]))

            start_index //= 2
            end_index //= 2

        return proof

    @staticmethod
    def sort_elements(elements):
        return sorted(elements, key=lambda hex_str: web3.keccak(hexstr=hex_str))

    @staticmethod
    def get_layers(elements):
        layers = [elements]
        while len(layers[-1]) > 1:
            layers.append(MerkleTree.get_next_layer(layers[-1]))
        return layers

    @staticmethod
    def get_next_layer(elements):
        return [
            MerkleTree.combined_hash(a, b)
            for a, b in zip_longest(elements[::2], elements[1::2])
        ]

    @staticmethod
    def combined_hash(a, b):
        if a is None:
            return b
        if b is None:
            return a
        return web3.keccak(b"".join(sorted([a, b])))

    @staticmethod
    def verify_proof(root, proof, target):
        computedHash = web3.keccak(hexstr=target)

        for proofItem in proof:
            computedHash = MerkleTree.combined_hash(computedHash, to_bytes(hexstr=proofItem))

        return root == computedHash

    @staticmethod
    def verify_slice_proof(root, proof, elements, start):
        layer = [web3.keccak(hexstr=el) for el in elements]
        start_index = start
        end_index = start + len(elements) - 1
        proof_index = 0
        while proof_index < len(proof) or len(layer) > 1:
            if start_index % 2 == 1:
                layer.insert(0, to_bytes(hexstr=proof[proof_index]))
                proof_index += 1

            if end_index % 2 == 0:
                layer.append(to_bytes(hexstr=proof[proof_index]))
                proof_index += 1

            layer = [
                MerkleTree.combined_hash(a, b)
                for a, b in zip_longest(layer[::2], layer[1::2])
            ]

            start_index //= 2
            end_index //= 2

        return root == layer[0]


if __name__ == "__main__":

    text_leafs = list(range(0,32))
    leafs = MerkleTree.sort_elements([encode_hex(str(el)) for el in text_leafs])
    tree = MerkleTree(leafs)
    proof = tree.get_slice_proof(0,1)
    print(proof)
    print(MerkleTree.verify_slice_proof(tree.root, proof, leafs[0:1], 0))
