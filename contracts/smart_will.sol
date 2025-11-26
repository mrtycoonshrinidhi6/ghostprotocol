// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title SmartWill
 * @dev Decentralized digital will with time-lock, multi-sig, and dead-man switch
 */
contract SmartWill {
    
    // ============================================================================
    // STATE VARIABLES
    // ============================================================================
    
    address public owner;
    uint256 public deathTimestamp;
    uint256 public constant TIME_LOCK_PERIOD = 30 days;
    uint256 public lastActivityTimestamp;
    uint256 public constant INACTIVITY_THRESHOLD = 90 days;
    
    bool public isDeathConfirmed;
    bool public willExecuted;
    
    // Multi-sig configuration
    address[] public validators;
    mapping(address => bool) public isValidator;
    uint256 public requiredValidations;
    uint256 public currentValidations;
    mapping(address => bool) public hasValidated;
    
    // Beneficiaries and asset distribution
    struct Beneficiary {
        address payable wallet;
        uint256 sharePercentage; // Out of 10000 (100.00%)
        bool claimed;
    }
    
    Beneficiary[] public beneficiaries;
    mapping(address => uint256) public beneficiaryIndex;
    
    // Asset inventory
    struct DigitalAsset {
        string assetType; // "ETH", "ERC20", "ERC721", "data"
        address tokenAddress; // For ERC20/ERC721
        uint256 tokenId; // For ERC721
        string metadataURI; // For data assets
        bool distributed;
    }
    
    DigitalAsset[] public assets;
    
    // ============================================================================
    // EVENTS
    // ============================================================================
    
    event WillCreated(address indexed owner, uint256 timestamp);
    event DeathReported(address indexed reporter, uint256 timestamp);
    event DeathValidated(address indexed validator, uint256 validationCount);
    event DeathConfirmed(uint256 deathTimestamp, uint256 executionTimestamp);
    event TimeLockActivated(uint256 unlockTimestamp);
    event BeneficiaryAdded(address indexed beneficiary, uint256 sharePercentage);
    event AssetDistributed(address indexed beneficiary, uint256 amount, string assetType);
    event WillExecuted(uint256 timestamp);
    event ActivityRecorded(uint256 timestamp);
    event DeadManSwitchTriggered(uint256 inactiveDays);
    event ValidatorAdded(address indexed validator);
    event ValidatorRemoved(address indexed validator);
    
    // ============================================================================
    // MODIFIERS
    // ============================================================================
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this");
        _;
    }
    
    modifier onlyValidator() {
        require(isValidator[msg.sender], "Only validator can call this");
        _;
    }
    
    modifier notExecuted() {
        require(!willExecuted, "Will already executed");
        _;
    }
    
    modifier afterTimeLock() {
        require(isDeathConfirmed, "Death not confirmed");
        require(block.timestamp >= deathTimestamp + TIME_LOCK_PERIOD, "Time-lock not expired");
        _;
    }
    
    // ============================================================================
    // CONSTRUCTOR
    // ============================================================================
    
    constructor(address[] memory _validators, uint256 _requiredValidations) {
        require(_validators.length >= _requiredValidations, "Invalid validator config");
        require(_requiredValidations >= 2, "Need at least 2 validators");
        
        owner = msg.sender;
        lastActivityTimestamp = block.timestamp;
        requiredValidations = _requiredValidations;
        
        for (uint256 i = 0; i < _validators.length; i++) {
            require(_validators[i] != address(0), "Invalid validator address");
            validators.push(_validators[i]);
            isValidator[_validators[i]] = true;
        }
        
        emit WillCreated(owner, block.timestamp);
    }
    
    // ============================================================================
    // OWNER FUNCTIONS
    // ============================================================================
    
    function addBeneficiary(address payable _wallet, uint256 _sharePercentage) external onlyOwner notExecuted {
        require(_wallet != address(0), "Invalid beneficiary address");
        require(_sharePercentage > 0 && _sharePercentage <= 10000, "Invalid share percentage");
        
        beneficiaries.push(Beneficiary({
            wallet: _wallet,
            sharePercentage: _sharePercentage,
            claimed: false
        }));
        
        beneficiaryIndex[_wallet] = beneficiaries.length - 1;
        
        emit BeneficiaryAdded(_wallet, _sharePercentage);
    }
    
    function addAsset(string memory _assetType, address _tokenAddress, uint256 _tokenId, string memory _metadataURI) 
        external onlyOwner notExecuted {
        
        assets.push(DigitalAsset({
            assetType: _assetType,
            tokenAddress: _tokenAddress,
            tokenId: _tokenId,
            metadataURI: _metadataURI,
            distributed: false
        }));
    }
    
    function recordActivity() external onlyOwner {
        lastActivityTimestamp = block.timestamp;
        emit ActivityRecorded(block.timestamp);
    }
    
    function addValidator(address _validator) external onlyOwner notExecuted {
        require(_validator != address(0), "Invalid validator address");
        require(!isValidator[_validator], "Already a validator");
        
        validators.push(_validator);
        isValidator[_validator] = true;
        
        emit ValidatorAdded(_validator);
    }
    
    function removeValidator(address _validator) external onlyOwner notExecuted {
        require(isValidator[_validator], "Not a validator");
        require(validators.length - 1 >= requiredValidations, "Cannot remove, would break multi-sig");
        
        isValidator[_validator] = false;
        
        // Remove from array (simple approach, doesn't preserve order)
        for (uint256 i = 0; i < validators.length; i++) {
            if (validators[i] == _validator) {
                validators[i] = validators[validators.length - 1];
                validators.pop();
                break;
            }
        }
        
        emit ValidatorRemoved(_validator);
    }
    
    // ============================================================================
    // DEATH CONFIRMATION - MULTI-SIG
    // ============================================================================
    
    function reportDeath() external onlyValidator notExecuted {
        require(!isDeathConfirmed, "Death already confirmed");
        require(!hasValidated[msg.sender], "Already validated");
        
        hasValidated[msg.sender] = true;
        currentValidations++;
        
        emit DeathValidated(msg.sender, currentValidations);
        
        // Check if threshold reached
        if (currentValidations >= requiredValidations) {
            _confirmDeath();
        }
    }
    
    function _confirmDeath() private {
        isDeathConfirmed = true;
        deathTimestamp = block.timestamp;
        
        emit DeathConfirmed(deathTimestamp, deathTimestamp + TIME_LOCK_PERIOD);
        emit TimeLockActivated(deathTimestamp + TIME_LOCK_PERIOD);
    }
    
    // ============================================================================
    // DEAD-MAN SWITCH
    // ============================================================================
    
    function triggerDeadManSwitch() external {
        require(!isDeathConfirmed, "Death already confirmed");
        require(block.timestamp >= lastActivityTimestamp + INACTIVITY_THRESHOLD, 
                "Owner still active");
        
        uint256 inactiveDays = (block.timestamp - lastActivityTimestamp) / 1 days;
        
        emit DeadManSwitchTriggered(inactiveDays);
        
        // Auto-confirm death
        isDeathConfirmed = true;
        deathTimestamp = block.timestamp;
        
        emit DeathConfirmed(deathTimestamp, deathTimestamp + TIME_LOCK_PERIOD);
        emit TimeLockActivated(deathTimestamp + TIME_LOCK_PERIOD);
    }
    
    // ============================================================================
    // WILL EXECUTION - ASSET DISTRIBUTION
    // ============================================================================
    
    function executeWill() external afterTimeLock notExecuted {
        willExecuted = true;
        
        // Distribute ETH
        _distributeETH();
        
        emit WillExecuted(block.timestamp);
    }
    
    function _distributeETH() private {
        uint256 totalBalance = address(this).balance;
        
        if (totalBalance == 0) return;
        
        for (uint256 i = 0; i < beneficiaries.length; i++) {
            Beneficiary storage beneficiary = beneficiaries[i];
            
            if (!beneficiary.claimed) {
                uint256 share = (totalBalance * beneficiary.sharePercentage) / 10000;
                
                if (share > 0) {
                    beneficiary.wallet.transfer(share);
                    beneficiary.claimed = true;
                    
                    emit AssetDistributed(beneficiary.wallet, share, "ETH");
                }
            }
        }
    }
    
    function claimAsset(uint256 assetIndex) external afterTimeLock {
        require(assetIndex < assets.length, "Invalid asset index");
        require(!assets[assetIndex].distributed, "Asset already distributed");
        
        DigitalAsset storage asset = assets[assetIndex];
        
        // Simple distribution: first beneficiary gets it (in production, use proper mapping)
        require(msg.sender == beneficiaries[0].wallet, "Not authorized to claim");
        
        asset.distributed = true;
        
        // For ERC20/ERC721, would call transfer here
        // IERC20(asset.tokenAddress).transfer(msg.sender, amount);
        // IERC721(asset.tokenAddress).transferFrom(address(this), msg.sender, asset.tokenId);
        
        emit AssetDistributed(msg.sender, 0, asset.assetType);
    }
    
    // ============================================================================
    // VIEW FUNCTIONS
    // ============================================================================
    
    function getTimeLockRemaining() external view returns (uint256) {
        if (!isDeathConfirmed) {
            return 0;
        }
        
        uint256 unlockTime = deathTimestamp + TIME_LOCK_PERIOD;
        
        if (block.timestamp >= unlockTime) {
            return 0;
        }
        
        return unlockTime - block.timestamp;
    }
    
    function getInactiveDays() external view returns (uint256) {
        return (block.timestamp - lastActivityTimestamp) / 1 days;
    }
    
    function getBeneficiaryCount() external view returns (uint256) {
        return beneficiaries.length;
    }
    
    function getAssetCount() external view returns (uint256) {
        return assets.length;
    }
    
    function getValidatorCount() external view returns (uint256) {
        return validators.length;
    }
    
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    function getBeneficiary(uint256 index) external view returns (
        address wallet,
        uint256 sharePercentage,
        bool claimed
    ) {
        require(index < beneficiaries.length, "Invalid index");
        Beneficiary memory b = beneficiaries[index];
        return (b.wallet, b.sharePercentage, b.claimed);
    }
    
    // ============================================================================
    // RECEIVE FUNCTION
    // ============================================================================
    
    receive() external payable {
        // Accept ETH deposits
    }
}
