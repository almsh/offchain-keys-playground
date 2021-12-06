pragma solidity ^0.8.6;

import "GNSPS/solidity-bytes-utils@0.8.0/contracts/BytesLib.sol";
import "./BaseNOR.sol";


contract SimpleBatchNOR is BaseNOR {
    uint256 public batchSize;

    bytes32[] keysBatchesHashes;

    uint256 public usedBatchHashes = 0;

    constructor(address _nodeOperator, address _depositContract, uint256 _batchSize) BaseNOR(_nodeOperator, _depositContract) {
        batchSize = _batchSize;
    }

    function addPubkeysAndSignsHashes(bytes32[] memory hashes) external onlyNodeOperator {
        for (uint256 i = 0; i < hashes.length; ++i) {
            keysBatchesHashes.push(hashes[i]);
        }
    }

    function depositBufferedEther(bytes[] calldata keys, bytes[] calldata signs) external {
        require(keys.length == signs.length);
        for(uint256 i = 0; i < keys.length/batchSize; i++){
            uint256 start = batchSize * i;
            uint256 end = batchSize * (i + 1);
            bytes memory keysSignsBytes;
            for(uint256 j = start; j < end; j++) {
                keysSignsBytes = BytesLib.concat(keysSignsBytes,BytesLib.concat(keys[j], signs[j]));
            }
            bytes32 passedBatchHash = keccak256(abi.encodePacked(keysSignsBytes));

            bytes32 batchHash = keysBatchesHashes[usedBatchHashes++];
            require(passedBatchHash == batchHash);
            for(uint256 j = 0; j < batchSize; j++){
                _stake(keys[start+j], signs[start+j]);
            }
        }
    }

}
