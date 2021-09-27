pragma solidity ^0.8.1;

contract DummyNodeOperatorsRegistry {
    address public nodeOperator;
    address public governance;
    
    modifier onlyNodeOperator() {
        require(msg.sender == nodeOperator, "AUTH_FAILED");
        _;
    }
    
    modifier onlyGovernance() {
        require(msg.sender == governance, "AUTH_FAILED");
        _;
    }
    
    struct PubkeyAndSignature {
        bytes pubkey;
        bytes signature;
    }
    
    PubkeyAndSignature[] public keys; 
    
    uint256 public approvedKeys; 
    uint256 public usedKeys;
    
    
    constructor(address _nodeOperator, address _governance) {
        nodeOperator = _nodeOperator;
        governance = _governance;
    }
    
    function totalKeys() public view returns (uint256) {
        return keys.length;
    }
    
    function addSigningKey(bytes memory _pubkey, bytes memory _signature) external onlyNodeOperator {
        // add new pubkey and signature
        keys.push(PubkeyAndSignature(_pubkey, _signature));
    }
    
    function approveSigningKeys(uint256 newApprovedKeys) external onlyGovernance {
        approvedKeys = newApprovedKeys;
    }
    
    function depositBufferedEther() external {
        // checks that we have next approved key and call:
        // _stake(pubkey, signature);
        usedKeys = usedKeys + 1;
    }
    
    function _stake(bytes memory _pubkey, bytes memory _signature) internal {
       // actually call deposit function, might be a mock
    }
}