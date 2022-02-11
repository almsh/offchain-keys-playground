pragma solidity ^0.8.6;

import "./BaseNOR.sol";

contract MerkleBatchNOR is BaseNOR {
    struct MerkleRoot {
        uint256 batchesUsed;
        uint256 size;
        bytes32 merkleRoot;
    }

    MerkleRoot[] public merkleRoots;

    uint256 public usedRoots;
    uint256 public batchSize;

    constructor(address _nodeOperator, address _depositContract, uint256 _batchSize) BaseNOR(_nodeOperator, _depositContract) {
        batchSize = _batchSize;
    }

    function totalMerkleRoots() public view returns (uint256) {
        return merkleRoots.length;
    }

    function addMerkleRoot(bytes32 root, uint256 size) external onlyNodeOperator {
        merkleRoots.push(MerkleRoot(0, size, root));
    }

    function depositBufferedEther(bytes[] calldata keys, bytes[] calldata signs, bytes32[] calldata proof) external {
        require(keys.length == signs.length);
        MerkleRoot storage root = merkleRoots[usedRoots];

        uint256 batchesToProcess = keys.length / batchSize;
        require(keys.length % batchSize == 0);
        bytes32[] memory batchesHashes = new bytes32[](batchesToProcess);

        for (uint256 i = 0; i < batchesToProcess; ++i) {
            uint256 start = batchSize * i;
            uint256 end = batchSize * (i + 1);
            batchesHashes[i] = keccak256(abi.encodePacked(root.batchesUsed + i, _hashCountersKeysAndSigns(keys, signs, start, end)));
        }

        require(_verifyMerkleProof(root.merkleRoot, proof, batchesHashes, root.batchesUsed));

        for (uint256 i = 0; i < keys.length; ++i) {
            _stake(keys[i], signs[i]);
        }

        root.batchesUsed += batchesToProcess;
        if (root.batchesUsed >= root.size) {
            usedRoots += 1;
        }
    }


    function _hashCountersKeysAndSigns(bytes[] calldata keys, bytes[] calldata signs, uint256 start, uint256 end) internal pure returns (bytes memory){
        bytes memory keysSignsBytes;
        for (uint256 j = start; j < end; j++) {
            keysSignsBytes = BytesLib.concat(keysSignsBytes, BytesLib.concat(keys[j], signs[j]));
        }
        return keysSignsBytes;
    }


       function _verifyMerkleProof(
        bytes32 root,
        bytes32[] memory proof,
        bytes32[] memory leafs,
        uint256 _startIndex
    ) internal pure returns (bool) {

        bytes32[] memory workLayer = new bytes32[](leafs.length + 2);

        for (uint256 i = 0; i < leafs.length; i++) {
            workLayer[i + 1] = keccak256(abi.encode(leafs[i]));
        }

        uint256 startIndex = _startIndex;
        uint256 endIndex = _startIndex + leafs.length - 1;
        uint256 proofIndex = 0;
        uint256 rangeEnd = leafs.length + 1;

        while (proofIndex < proof.length || rangeEnd > 2) {
            uint256 startOffset = 0;

            if (startIndex % 2 == 1) {
                workLayer[0] = proof[proofIndex];
                proofIndex++;
                startOffset = 1;
            }

            if (endIndex % 2 == 0) {
                workLayer[rangeEnd] = proof[proofIndex];
                proofIndex++;
                rangeEnd++;
            }

            rangeEnd = (rangeEnd + startOffset) / 2 + 1;

            for (uint256 i = 1; i < rangeEnd; i++) {
                uint256 pairFirstIndex = 2 * i - startOffset - 1;
                uint256 pairSecondIndex = 2 * i - startOffset;
                workLayer[i] = _combineHashes(workLayer[pairFirstIndex], workLayer[pairSecondIndex]);
            }

            startIndex /= 2;
            endIndex /= 2;
        }

        // Check if the computed hash (root) is equal to the provided root
        return workLayer[1] == root;
    }

    function _combineHashes(bytes32 a, bytes32 b) internal pure returns (bytes32){
        if (a <= b) {
            return keccak256(abi.encodePacked(a, b));
        } else {
            return keccak256(abi.encodePacked(b, a));
        }
    }
}
