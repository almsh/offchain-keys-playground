from itertools import zip_longest

from brownie import web3
from eth_utils import encode_hex, to_bytes

class MerkleTree:
    def __init__(self, elements):
        self.elements = sorted(set(web3.keccak(hexstr=el) for el in elements))
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


if __name__ == "__main__":
    PUBKEY = '0x86ba17890f9e2190d6d8666124583858fb0c8f3135cc99b3a637ad5ca00b3aabe358e64fb4888554881158105234dea1'
    SIGNATURE = '0x8f486ac2d89e911ece802a9a8a15a537ac0f1f10578b6b3e4db43edda57cf8e7ac87914c51ef89eb8da271d1c2206aee014716b97e6676a3daa699e4672f764787a2d845170c9a7ee37326420c935271b80dee7fc83bd44598d73dd86f53d6f6'


    text_leafs = ['0'+PUBKEY+SIGNATURE, 'world', 'test', 'lex']
    leafs = [encode_hex(el) for el in text_leafs]
    tree = MerkleTree(leafs)
    proof = tree.get_proof(leafs[0])
    print(proof)
    if MerkleTree.verify_proof(tree.root, proof, leafs[0]) and not MerkleTree.verify_proof(tree.root, proof, encode_hex('bad leaf')):
        print('success')
    else:
        print('fail')