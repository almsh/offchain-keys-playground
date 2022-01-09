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

        uint256 proofIndex = 0;
        uint256 startIndex = _startIndex;
        uint256 endIndex = _startIndex + leafs.length - 1;
        bytes32[] memory layer;

        bytes32[] memory firstLayer = new bytes32[](leafs.length);
        for (uint256 i = 0; i < leafs.length; i++) {
            firstLayer[i] = keccak256(abi.encode(leafs[i]));
        }

        layer = firstLayer;


        while (proofIndex < proof.length || layer.length > 1) {

            if (startIndex % 2 == 1) {
                layer = _unshiftArray(proof[proofIndex], layer);
                proofIndex++;
            }

            if (endIndex % 2 == 0) {
                layer = _pushToArray(proof[proofIndex], layer);
                proofIndex++;
            }

            layer = _getNextLayer(layer);

            startIndex /= 2;
            endIndex /= 2;
        }

        // Check if the computed hash (root) is equal to the provided root
        return layer[0] == root;
    }

    function _combineHashes(bytes32 a, bytes32 b) internal pure returns (bytes32){
        if (a <= b) {
            return keccak256(abi.encodePacked(a, b));
        } else {
            return keccak256(abi.encodePacked(b, a));
        }
    }


    function _unshiftArray(bytes32 item, bytes32[] memory array) internal pure returns (bytes32[] memory){
        bytes32[] memory newArray = new bytes32[](array.length + 1);
        newArray[0] = item;
        for (uint256 i = 0; i < array.length; i++) {
            newArray[i + 1] = array[i];
        }
        return newArray;
    }

    function _pushToArray(bytes32 item, bytes32[] memory array) internal pure returns (bytes32[] memory){
        bytes32[] memory newArray = new bytes32[](array.length + 1);
        for (uint256 i = 0; i < array.length; i++) {
            newArray[i] = array[i];
        }
        newArray[newArray.length - 1] = item;
        return newArray;
    }

    function _getNextLayer(bytes32[] memory layer) internal pure returns (bytes32[] memory){
        uint256 len = layer.length / 2;
        bytes32[] memory newLayer = new bytes32[](len);

        uint256 j = 0;
        for (uint256 i = 1; i < layer.length; i += 2) {
            newLayer[j++] = _combineHashes(layer[i - 1], layer[i]);
        }

        return newLayer;
    }


}
