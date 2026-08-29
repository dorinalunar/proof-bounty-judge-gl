import pytest
from unittest.mock import patch, MagicMock

# Припускаємо, що твій основний файл називається contract.py
from contract import ProofBountyJudge

@pytest.fixture
def mock_gl():
    """Фікстура для мокання глобального об'єкта gl з GenLayer"""
    with patch("contract.gl") as mock:
        # Мокаємо адресу власника (деплоєра)
        mock.message.sender_address = "0xOwnerAddress"
        yield mock

@pytest.fixture
def contract(mock_gl):
    """Фікстура для ініціалізації контракту перед кожним тестом"""
    return ProofBountyJudge()

def test_initialization(contract):
    """Перевірка правильної ініціалізації власника та валідатора"""
    assert contract.owner == "0xOwnerAddress"
    assert contract._is_validator("0xOwnerAddress") == True
    assert contract.bounty_counter == "0"
    assert contract.submission_counter == "0"

def test_create_bounty(contract, mock_gl):
    """Перевірка створення баунті"""
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
    """Перевірка строгої типізації, яку вимагав стюард"""
    # Передаємо правильний тип (bool)
    assert contract._ensure_bool(True) == True
    assert contract._ensure_bool(False) == False
    
    # Передаємо неправильні типи і очікуємо помилку ERR_INVALID_APPROVAL_TYPE
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract._ensure_bool("true")
        
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract._ensure_bool("false")
        
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract._ensure_bool(1)

def test_set_bounty_active_strict_type(contract, mock_gl):
    """Перевірка захисту від текстових значень при активації баунті"""
    contract.create_bounty("Desc", "Crit", "10")
    
    # Правильне оновлення статусу
    contract.set_bounty_active("1", False)
    assert contract._load("bounties_json")["1"]["is_active"] == False
    
    # Спроба передати рядок має викликати помилку
    with pytest.raises(Exception, match="ERR_INVALID_APPROVAL_TYPE"):
        contract.set_bounty_active("1", "true")
