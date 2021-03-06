pragma solidity ^0.8.6;

import "GNSPS/solidity-bytes-utils@0.8.0/contracts/BytesLib.sol";
import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/utils/math/SafeMath.sol";

interface IDepositContract {
    /// @notice A processed deposit event.
    event DepositEvent(
        bytes pubkey,
        bytes withdrawal_credentials,
        bytes amount,
        bytes signature,
        bytes index
    );

    /// @notice Submit a Phase 0 DepositData object.
    /// @param pubkey A BLS12-381 public key.
    /// @param withdrawal_credentials Commitment to a public key for withdrawals.
    /// @param signature A BLS12-381 signature.
    /// @param deposit_data_root The SHA-256 hash of the SSZ-encoded DepositData object.
    /// Used as a protection against malformed input.
    function deposit(
        bytes calldata pubkey,
        bytes calldata withdrawal_credentials,
        bytes calldata signature,
        bytes32 deposit_data_root
    ) external payable;

    /// @notice Query the current deposit root hash.
    /// @return The deposit root hash.
    function get_deposit_root() external view returns (bytes32);

    /// @notice Query the current deposit count.
    /// @return The deposit count encoded as a little endian 64-bit number.
    function get_deposit_count() external view returns (bytes memory);
}

contract DummyNodeOperatorsRegistry {
    using SafeMath for uint256;

    uint256 constant public SIGNATURE_LENGTH = 96;

    uint256 constant public DEPOSIT_SIZE = 32 ether;
    uint256 internal constant DEPOSIT_AMOUNT_UNIT = 1000000000 wei;
    bytes32 internal constant WITHDRAWAL_CREDENTIALS = 0x010000000000000000000000b9d7934878b5fb9610b3fe8a5e441e8fad7e293f;

    uint256 constant public TREE_LEAF_AMOUNT = 4;

    address public nodeOperator;

    IDepositContract depositContract;

    struct MerkleRoot {
        uint256 keysLeft;
        bytes32 merkleRoot;
    }
    
    modifier onlyNodeOperator() {
        require(msg.sender == nodeOperator, "AUTH_FAILED");
        _;
    }
    
    struct PubkeyAndSignature {
        bytes pubkey;
        bytes signature;
    }

    MerkleRoot[] public merkleRoots;

    uint256 public usedRoots;
    
    
    constructor(address _nodeOperator, address _depositContract) {
        nodeOperator = _nodeOperator;
        depositContract = IDepositContract(_depositContract);
    }
    
    function totalMerkleRoots() public view returns (uint256) {
        return merkleRoots.length;
    }

    function submit() public payable {}

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

    function testEncode(uint256 num, bytes memory key, bytes memory sign) external pure returns (bytes memory){
        return abi.encode(num, key, sign);
    }

    function testEncodePacked(uint256 num, bytes memory key, bytes memory sign) external pure returns (bytes memory){
        return abi.encodePacked(num, key, sign);
    }
    
   /**
    * @dev Invokes a deposit call to the official Deposit contract
    * @param _pubkey Validator to stake for
    * @param _signature Signature of the deposit call
    */
    function _stake(bytes memory _pubkey, bytes memory _signature) internal {
        bytes32 withdrawalCredentials = WITHDRAWAL_CREDENTIALS;
        require(withdrawalCredentials != 0, "EMPTY_WITHDRAWAL_CREDENTIALS");


        uint256 value = DEPOSIT_SIZE;

        // The following computations and Merkle tree-ization will make official Deposit contract happy
        uint256 depositAmount = value.div(DEPOSIT_AMOUNT_UNIT);
        assert(depositAmount.mul(DEPOSIT_AMOUNT_UNIT) == value);    // properly rounded

        // Compute deposit data root (`DepositData` hash tree root) according to deposit_contract.sol
        bytes32 pubkeyRoot = sha256(_pad64(_pubkey));
        bytes32 signatureRoot = sha256(
            abi.encodePacked(
                sha256(BytesLib.slice(_signature, 0, 64)),
                sha256(_pad64(BytesLib.slice(_signature, 64, SIGNATURE_LENGTH.sub(64))))
            )
        );

        bytes32 depositDataRoot = sha256(
            abi.encodePacked(
                sha256(abi.encodePacked(pubkeyRoot, withdrawalCredentials)),
                sha256(abi.encodePacked(_toLittleEndian64(depositAmount), signatureRoot))
            )
        );

        uint256 targetBalance = address(this).balance.sub(value);

       depositContract.deposit{value:value}(
            _pubkey, abi.encodePacked(withdrawalCredentials), _signature, depositDataRoot);
        require(address(this).balance == targetBalance, "EXPECTING_DEPOSIT_TO_HAPPEN");
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


    /**
      * @dev Padding memory array with zeroes up to 64 bytes on the right
      * @param _b Memory array of size 32 .. 64
      */
    function _pad64(bytes memory _b) internal pure returns (bytes memory) {
        assert(_b.length >= 32 && _b.length <= 64);
        if (64 == _b.length)
            return _b;

        bytes memory zero32 = new bytes(32);
        assembly { mstore(add(zero32, 0x20), 0) }

        if (32 == _b.length)
            return BytesLib.concat(_b, zero32);
        else
            return BytesLib.concat(_b, BytesLib.slice(zero32, 0, uint256(64).sub(_b.length)));
    }

    /**
      * @dev Converting value to little endian bytes and padding up to 32 bytes on the right
      * @param _value Number less than `2**64` for compatibility reasons
      */
    function _toLittleEndian64(uint256 _value) internal pure returns (uint256 result) {
        result = 0;
        uint256 temp_value = _value;
        for (uint256 i = 0; i < 8; ++i) {
            result = (result << 8) | (temp_value & 0xFF);
            temp_value >>= 8;
        }

        assert(0 == temp_value);    // fully converted
        result <<= (24 * 8);
    }
}