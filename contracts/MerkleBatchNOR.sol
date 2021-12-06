pragma solidity ^0.8.6;

import "./BaseNOR.sol";

contract MerkleBatchNOR is BaseNOR {
    struct MerkleRoot {
        uint256 batchSize;
        uint256 batchesLeft;
        bytes32 merkleRoot;
    }

    MerkleRoot[] public merkleRoots;

    uint256 public usedRoots;

    constructor(address _nodeOperator, address _depositContract) BaseNOR(_nodeOperator, _depositContract) {}

    function totalMerkleRoots() public view returns (uint256) {
        return merkleRoots.length;
    }

     function addMerkleRoot(bytes32 root, uint256 batchesLeft, uint256 batchSize) external onlyNodeOperator {
        merkleRoots.push(MerkleRoot(batchSize, batchesLeft, root));
    }

    function depositBufferedEther(bytes[] calldata keys, bytes[] calldata signs, bytes32[][] calldata proofs) external {
        require(keys.length == signs.length);
        MerkleRoot storage root = merkleRoots[usedRoots];
        require(keys.length/root.batchSize == proofs.length);

        uint256 batchesToProcess = keys.length/root.batchSize;

        for (uint256 i = 0; i < batchesToProcess; ++i) {

            uint256 start = root.batchSize * i;
            uint256 end = root.batchSize * (i + 1);
            bytes memory keysSignsBytes;
            for(uint256 j = start; j < end; j++) {
                keysSignsBytes = BytesLib.concat(keysSignsBytes,BytesLib.concat(keys[j], signs[j]));
            }
            bytes32 passedBatchHash = keccak256(abi.encodePacked(root.batchesLeft - 1 - i, keysSignsBytes));

            require(_verifyMerkleProof(proofs[i], root.merkleRoot, passedBatchHash));

            for(uint256 j = 0; j < root.batchSize; j++){
                _stake(keys[start+j], signs[start+j]);
            }
        }

        root.batchesLeft -= batchesToProcess;
        if(root.batchesLeft == 0){
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
