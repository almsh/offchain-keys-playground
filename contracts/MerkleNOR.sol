pragma solidity ^0.8.6;

import "./BaseNOR.sol";

contract MerkleNOR is BaseNOR {
    struct MerkleRoot {
        uint256 keysUsed;
        uint256 size;
        bytes32 merkleRoot;
    }

    MerkleRoot[] public merkleRoots;

    uint256 public usedRoots;

    constructor(address _nodeOperator, address _depositContract) BaseNOR(_nodeOperator, _depositContract) {}

    function totalMerkleRoots() public view returns (uint256) {
        return merkleRoots.length;
    }

    function addMerkleRoot(bytes32 root, uint16 size) external onlyNodeOperator {
        merkleRoots.push(MerkleRoot(0, size, root));
    }

    function depositBufferedEther(bytes[] calldata keys, bytes[] calldata signs, bytes32[] calldata proof) external {
        require(keys.length == signs.length);
        MerkleRoot storage root = merkleRoots[usedRoots];
        bytes32[] memory keysSignsHashes = new bytes32[](keys.length);


        for (uint256 i = 0; i < keys.length; ++i) {
            keysSignsHashes[i] = keccak256(abi.encodePacked(root.keysUsed + i, keys[i], signs[i]));
        }

        require(_verifyMerkleProof(root.merkleRoot, proof, keysSignsHashes, root.keysUsed));

        for (uint256 i = 0; i < keys.length; ++i) {
            _stake(keys[i], signs[i]);
        }

        root.keysUsed += keys.length;
        if (root.keysUsed >= root.size) {
            usedRoots += 1;
        }
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
        for(uint256 i = 0; i < array.length; i++){
            newArray[i+1] = array[i];
        }
        return newArray;
    }

    function _pushToArray(bytes32 item, bytes32[] memory array) internal pure returns (bytes32[] memory){
        bytes32[] memory newArray = new bytes32[](array.length + 1);
        for(uint256 i = 0; i < array.length; i++){
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
