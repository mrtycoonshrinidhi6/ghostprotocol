"""
Ghost Protocol - Advanced Secret Loader
Secure API key management with validation and auto-fallback

Features:
- API key validation and missing key detection
- Automatic fallback to MOCK mode when keys missing
- AES-encrypted value support (placeholder)
- Detailed key status reporting
- Integration with config.py REALTIME_MODE
"""

import os
from typing import Dict, Optional, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from dotenv import load_dotenv
import base64

# Import config to access key requirements
from config import (
    CRITICAL_API_KEYS,
    OPTIONAL_API_KEYS,
    LOG_KEY_VALIDATION,
    REALTIME_MODE,
    USE_REALTIME,
    FORCE_REALTIME_OVERRIDE,
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class APIKeyStatus:
    """Status of a single API key"""
    key_name: str
    is_present: bool
    is_valid: bool
    value_preview: Optional[str]  # First 8 chars for debugging
    is_critical: bool
    error: Optional[str] = None


@dataclass
class LoadEnvResult:
    """Result of loading environment variables"""
    total_keys: int
    loaded_keys: int
    missing_keys: int
    critical_missing: List[str]
    optional_missing: List[str]
    can_use_realtime: bool
    key_statuses: Dict[str, APIKeyStatus]
    warnings: List[str]


# ============================================================================
# API KEY VALIDATION
# ============================================================================

def validate_api_key(key_name: str, key_value: Optional[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate an API key value
    
    Args:
        key_name: Name of the API key
        key_value: Value of the API key
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    
    if key_value is None or key_value == "":
        return False, "Key is empty or not set"
    
    # Check if it's a placeholder
    if key_value in ["your_key_here", "your_api_key_here", "your_gemini_api_key_here", 
                     "your_etherscan_key", "your_dropbox_token"]:
        return False, "Key is still a placeholder"
    
    # Specific validation rules per key type
    if "GEMINI" in key_name:
        if not key_value.startswith("AIzaSy"):
            return False, "Gemini key should start with 'AIzaSy'"
        if len(key_value) < 30:
            return False, "Gemini key too short"
    
    elif "ETHERSCAN" in key_name or "POLYGONSCAN" in key_name:
        if len(key_value) != 34:
            return False, f"Etherscan/Polygonscan keys should be 34 characters"
    
    elif "INFURA" in key_name:
        if len(key_value) != 32:
            return False, "Infura project ID should be 32 characters"
    
    elif key_name.endswith("_JSON"):
        # Path to JSON file - check if file exists
        if not os.path.exists(key_value):
            return False, f"JSON file not found: {key_value}"
    
    # If we get here, key looks valid
    return True, None


def get_key_preview(key_value: Optional[str], show_chars: int = 8) -> Optional[str]:
    """Get preview of API key (first N chars + ***)"""
    if not key_value or key_value == "":
        return None
    
    if len(key_value) <= show_chars:
        return key_value[:3] + "***"
    
    return key_value[:show_chars] + "***"


# ============================================================================
# ENVIRONMENT LOADING
# ============================================================================

# Default .env path: use the backend/.env file relative to the project root
DEFAULT_ENV_PATH = os.path.join(os.path.dirname(__file__), "backend", ".env")

def load_environment(env_file: str = DEFAULT_ENV_PATH) -> LoadEnvResult:
    """
    Load and validate environment variables
    
    Args:
        env_file: Path to .env file
    
    Returns:
        LoadEnvResult with detailed status
    """
    
    # Load .env file
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        if LOG_KEY_VALIDATION:
            print(f"⚠️  Warning: {env_file} not found, using system environment variables only")
    
    # Check all keys
    all_keys = CRITICAL_API_KEYS + OPTIONAL_API_KEYS
    key_statuses = {}
    critical_missing = []
    optional_missing = []
    warnings = []
    
    for key_name in all_keys:
        key_value = os.getenv(key_name)
        is_critical = key_name in CRITICAL_API_KEYS
        
        # Validate key
        is_present = key_value is not None and key_value != ""
        is_valid, error = validate_api_key(key_name, key_value) if is_present else (False, "Not set")
        
        # Create status
        status = APIKeyStatus(
            key_name=key_name,
            is_present=is_present,
            is_valid=is_valid,
            value_preview=get_key_preview(key_value),
            is_critical=is_critical,
            error=error
        )
        
        key_statuses[key_name] = status
        
        # Track missing keys
        if not is_present or not is_valid:
            if is_critical:
                critical_missing.append(key_name)
                warnings.append(f"CRITICAL: {key_name} is missing or invalid ({error})")
            else:
                optional_missing.append(key_name)
                if LOG_KEY_VALIDATION:
                    warnings.append(f"OPTIONAL: {key_name} is missing or invalid ({error})")
    
    # Calculate stats
    total_keys = len(all_keys)
    loaded_keys = sum(1 for s in key_statuses.values() if s.is_valid)
    missing_keys = total_keys - loaded_keys
    
    # Determine if we can use REALTIME mode
    can_use_realtime = len(critical_missing) == 0
    
    # Create result
    result = LoadEnvResult(
        total_keys=total_keys,
        loaded_keys=loaded_keys,
        missing_keys=missing_keys,
        critical_missing=critical_missing,
        optional_missing=optional_missing,
        can_use_realtime=can_use_realtime,
        key_statuses=key_statuses,
        warnings=warnings
    )
    
    return result


# ============================================================================
# AUTOMATIC MODE SWITCHING
# ============================================================================

def check_and_switch_mode(load_result: LoadEnvResult) -> str:
    """
    Check if REALTIME mode can be used, auto-switch to MOCK if needed
    
    Args:
        load_result: Result from load_environment()
    
    Returns:
        Current mode after check ("REALTIME" or "MOCK")
    """
    
    from config import LOG_MODE_SWITCHES

    # FORCE_REALTIME_OVERRIDE always wins
    if FORCE_REALTIME_OVERRIDE:
        if LOG_MODE_SWITCHES:
            print("✅ REALTIME MODE: ENABLED (forced by FORCE_REALTIME_OVERRIDE=true)")
            if load_result.critical_missing:
                print(f"⚠️  Critical keys missing even though realtime is forced: {', '.join(load_result.critical_missing)}")
            if load_result.optional_missing:
                print(f"⚠️  Optional keys missing: {', '.join(load_result.optional_missing)}")
        return "REALTIME"

    # If USE_REALTIME resolved to False in config, stay in MOCK
    if not USE_REALTIME:
        if LOG_MODE_SWITCHES:
            if not REALTIME_MODE:
                print("ℹ️  Mode: MOCK (configured in .env REALTIME_MODE=false)")
            else:
                print("ℹ️  Mode: MOCK (USE_REALTIME resolved to false)")
        return "MOCK"

    # USE_REALTIME is True and no force override – respect critical key presence
    if load_result.critical_missing:
        if LOG_MODE_SWITCHES:
            print(f"⚠️  Mode: MOCK (forced - missing critical keys: {', '.join(load_result.critical_missing)})")
            print("   Add missing critical keys to safely enable REALTIME mode")
        return "MOCK"

    # REALTIME mode is enabled and all critical keys present
    if LOG_MODE_SWITCHES:
        print("✅ Mode: REALTIME (all critical keys present)")
        if load_result.optional_missing:
            print(f"   Optional keys missing: {', '.join(load_result.optional_missing)}")
            print("   These services will use mock data")

    return "REALTIME"


# ============================================================================
# SECURE KEY RETRIEVAL
# ============================================================================

def get_api_key(key_name: str, encrypted: bool = False) -> Optional[str]:
    """
    Securely retrieve an API key
    
    Args:
        key_name: Name of the environment variable
        encrypted: If True, decrypt using AES (placeholder)
    
    Returns:
        API key value or None if not found
    """
    
    value = os.getenv(key_name)
    
    if value is None:
        return None
    
    # If encrypted, decrypt it (placeholder implementation)
    if encrypted:
        value = decrypt_value(value)
    
    return value


def decrypt_value(encrypted_value: str) -> str:
    """
    Decrypt AES-encrypted value (PLACEHOLDER)
    
    In production, implement actual AES decryption:
    - Use cryptography.fernet or AES-256-GCM
    - Store encryption key in secure vault (AWS KMS, Azure Key Vault)
    - Never hardcode encryption keys
    
    Args:
        encrypted_value: Base64-encoded encrypted value
    
    Returns:
        Decrypted plaintext value
    """
    
    # PLACEHOLDER: Just return the value as-is
    # In production, implement:
    # from cryptography.fernet import Fernet
    # cipher = Fernet(ENCRYPTION_KEY)
    # return cipher.decrypt(encrypted_value.encode()).decode()
    
    print("⚠️  Warning: decrypt_value() is a placeholder - implement actual AES decryption")
    return encrypted_value


def encrypt_value(plaintext_value: str) -> str:
    """
    Encrypt value using AES (PLACEHOLDER)
    
    Args:
        plaintext_value: Value to encrypt
    
    Returns:
        Base64-encoded encrypted value
    """
    
    # PLACEHOLDER: Just return the value as-is
    print("⚠️  Warning: encrypt_value() is a placeholder - implement actual AES encryption")
    return plaintext_value


# ============================================================================
# REPORTING
# ============================================================================

def print_key_status(load_result: LoadEnvResult, show_previews: bool = False):
    """
    Print detailed API key status report
    
    Args:
        load_result: Result from load_environment()
        show_previews: If True, show key previews (first 8 chars)
    """
    
    print("\n" + "=" * 70)
    print("🔑 API Key Status Report")
    print("=" * 70)
    
    print(f"Total Keys:    {load_result.total_keys}")
    print(f"Loaded:        {load_result.loaded_keys} ✅")
    print(f"Missing:       {load_result.missing_keys} ⚠️")
    print(f"Can Use REALTIME: {'Yes ✅' if load_result.can_use_realtime else 'No ❌'}")
    
    # Critical keys
    if load_result.critical_missing:
        print(f"\n❌ CRITICAL KEYS MISSING ({len(load_result.critical_missing)}):")
        for key in load_result.critical_missing:
            status = load_result.key_statuses[key]
            print(f"   - {key}: {status.error}")
    else:
        print(f"\n✅ All critical keys present")
    
    # Optional keys
    if load_result.optional_missing:
        print(f"\n⚠️  OPTIONAL KEYS MISSING ({len(load_result.optional_missing)}):")
        for key in load_result.optional_missing[:5]:  # Show first 5
            status = load_result.key_statuses[key]
            print(f"   - {key}: {status.error}")
        if len(load_result.optional_missing) > 5:
            print(f"   ... and {len(load_result.optional_missing) - 5} more")
    
    # Show key previews if requested
    if show_previews:
        print(f"\n🔍 Key Previews:")
        for key_name, status in load_result.key_statuses.items():
            if status.is_valid and status.value_preview:
                icon = "✅" if status.is_critical else "⚪"
                print(f"   {icon} {key_name}: {status.value_preview}")
    
    print("=" * 70 + "\n")


def get_key_status_dict(load_result: LoadEnvResult) -> Dict[str, str]:
    """
    Get key status as dictionary (for API endpoints)
    
    Args:
        load_result: Result from load_environment()
    
    Returns:
        Dictionary of key_name -> status ("loaded", "missing", "invalid")
    """
    
    status_dict = {}
    
    for key_name, status in load_result.key_statuses.items():
        if status.is_valid:
            status_dict[key_name] = "loaded"
        elif status.is_present:
            status_dict[key_name] = "invalid"
        else:
            status_dict[key_name] = "missing"
    
    return status_dict


# ============================================================================
# INITIALIZATION
# ============================================================================

# Load environment on module import
_load_result = load_environment()
_current_mode = check_and_switch_mode(_load_result)

# Print status if validation logging is enabled
if LOG_KEY_VALIDATION:
    print_key_status(_load_result, show_previews=False)


# ============================================================================
# PUBLIC API
# ============================================================================

def get_load_result() -> LoadEnvResult:
    """Get the environment loading result"""
    return _load_result


def get_current_runtime_mode() -> str:
    """Get current runtime mode after auto-switching"""
    return _current_mode


def is_key_available(key_name: str) -> bool:
    """Check if a specific API key is available and valid"""
    status = _load_result.key_statuses.get(key_name)
    return status.is_valid if status else False


def require_key(key_name: str) -> str:
    """
    Require an API key - raises error if not available
    
    Args:
        key_name: Name of required API key
    
    Returns:
        API key value
    
    Raises:
        ValueError: If key is not available
    """
    
    if not is_key_available(key_name):
        status = _load_result.key_statuses.get(key_name)
        error = status.error if status else "Key not configured"
        raise ValueError(f"Required API key '{key_name}' is not available: {error}")
    
    return get_api_key(key_name)


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    # Data structures
    "APIKeyStatus",
    "LoadEnvResult",
    
    # Key management
    "load_environment",
    "get_api_key",
    "is_key_available",
    "require_key",
    
    # Mode switching
    "check_and_switch_mode",
    "get_current_runtime_mode",
    
    # Encryption (placeholder)
    "decrypt_value",
    "encrypt_value",
    
    # Reporting
    "print_key_status",
    "get_key_status_dict",
    "get_load_result",
]
