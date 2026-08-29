import pytest
from unittest.mock import patch

# Importing the contract from ProofBountyJudge.py
from ProofBountyJudge import ProofBountyJudge

@pytest.fixture
def mock_gl():
    """Fixture to mock the global gl object from GenLayer"""
    with patch("ProofBountyJudge.gl") as mock:
        # Mock the owner (deployer) address
        mock.message.sender_address = "0xOwnerAddress"
        yield mock

@pytest.fixture
def contract(mock_gl):
    """Fixture to initialize the contract before each test"""
    return ProofBountyJudge()

def test_initialization(contract):
    """Test proper initialization of owner and validator"""
    assert contract.owner == "0xOwnerAddress"
    assert contract._is_validator("0xOwnerAddress") == True
    assert contract.bounty_counter == "0"
    assert contract.submission_counter == "0"

def test_create_bounty(contract, mock_gl):
    """Test bounty creation"""
    bounty_id = contract.create_bounty(
        description="GitHub repository check",
        criteria="Must contain smart contract code",
        reward_amount="10"
    )
    assert bounty_id == "1"
    
    bounties = contract._load("bounties_json")
    assert bounties["1"]["description"] == "GitHub repository check"
    assert bounties["1"]["is_active"] == True

def test_fail_closed_validation(contract):
    """Test the strict typing fail-closed behavior requested by the steward"""
    # Pass correct type (bool)
    assert contract._ensure_bool(True) == True
    assert contract._ensure_bool(False) == False
    
    # Pass incorrect types and expect ERR_INVALID_APPROVAL_TYPE exception
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract._ensure_bool("true")
        
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract._ensure_bool("false")
        
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract._ensure_bool(1)

def test_set_bounty_active_strict_type(contract, mock_gl):
    """Test protection against text values when activating a bounty"""
    contract.create_bounty("Desc", "Crit", "10")
    
    # Correct status update
    contract.set_bounty_active("1", False)
    assert contract._load("bounties_json")["1"]["is_active"] == False
    
    # Attempting to pass a string should raise an exception
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract.set_bounty_active("1", "true")