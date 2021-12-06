pragma solidity ^0.8.6;

import "./BaseNOR.sol";

contract NaiveNOR is BaseNOR {

    struct PubkeyAndSignature {
        bytes pubkey;
        bytes signature;
    }

    PubkeyAndSignature[] public pubkeysAndSignatures;

    uint256 public usedKeys = 0;


    constructor(address _nodeOperator, address _depositContract) BaseNOR(_nodeOperator, _depositContract) {
    }

    function totalKeys() public view returns (uint256) {
        return pubkeysAndSignatures.length;
    }

    function addPubkeysAndSignatures(bytes[] memory keys, bytes[] memory signs) external onlyNodeOperator {
        require(keys.length == signs.length);
        for (uint256 i = 0; i < keys.length; ++i) {
            pubkeysAndSignatures.push(PubkeyAndSignature(keys[i], signs[i]));
        }
    }

    function depositBufferedEther(uint256 keysToDeposit) external {
        for (uint256 i = 0; i < keysToDeposit && usedKeys < totalKeys(); i++) {
            PubkeyAndSignature memory pubkeyAndSign = pubkeysAndSignatures[usedKeys++];
            _stake(pubkeyAndSign.pubkey, pubkeyAndSign.signature);
        }
    }

}