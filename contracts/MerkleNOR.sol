pragma solidity ^0.8.6;

import "./BaseNOR.sol";

contract MerkleNOR is BaseNOR {
    struct MerkleRoot {
        uint256 keysLeft;
        bytes32 merkleRoot;
    }

    MerkleRoot[] public merkleRoots;

    uint256 public usedRoots;

    constructor(address _nodeOperator, address _depositContract) BaseNOR(_nodeOperator, _depositContract) {}

    function totalMerkleRoots() public view returns (uint256) {
        return merkleRoots.length;
    }

     function addMerkleRoot(bytes32 root, uint16 keysLeft) external onlyNodeOperator {
        merkleRoots.push(MerkleRoot(keysLeft, root));
    }

    function depositBufferedEther(bytes[] calldata keys, bytes[] calldata signs, bytes32[][] calldata proofs) external {
        require(keys.length == signs.length);
        require(keys.length == proofs.length);
        MerkleRoot storage root = merkleRoots[usedRoots];
        for (uint256 i = 0; i < keys.length; ++i) {
            require(_verifyMerkleProof(proofs[i], root.merkleRoot, keccak256(abi.encodePacked(root.keysLeft - 1 - i, keys[i], signs[i]))));
            _stake(keys[i], signs[i]);
        }

        root.keysLeft -= keys.length;
        if(root.keysLeft == 0){
            usedRoots += 1;
        }
    }

     function _verifyMerkleProof(
        bytes32[] memory proof,
        bytes32 root,
        bytes32 leaf
    ) internal pure returns (bool) {
        bytes32 computedHash = keccak256(abi.encode(leaf));

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];

            if (computedHash <= proofElement) {
                // Hash(current computed hash + current element of the proof)
                computedHash = keccak256(abi.encodePacked(computedHash, proofElement));
            } else {
                // Hash(current element of the proof + current computed hash)
                computedHash = keccak256(abi.encodePacked(proofElement, computedHash));
            }
        }

        // Check if the computed hash (root) is equal to the provided root
        return computedHash == root;
    }

}
