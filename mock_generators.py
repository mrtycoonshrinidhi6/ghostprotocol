"""
Ghost Protocol - Mock Data Generators
Realistic mock data generators for all tools when REALTIME_MODE=False

Features:
- Schema-compliant responses matching real API structure
- Artificial latency simulation
- Randomized realistic data
- Configurable return values
"""

import random
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from config import get_mock_latency, LOG_MOCK_GENERATION


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

async def add_mock_latency():
    """Add artificial latency to simulate real API calls"""
    min_latency, max_latency = get_mock_latency()
    latency = random.uniform(min_latency, max_latency)
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Simulating latency: {latency:.2f}s")
    
    await asyncio.sleep(latency)


def random_date(days_back: int = 30) -> str:
    """Generate random date within last N days"""
    date = datetime.now() - timedelta(days=random.randint(0, days_back))
    return date.isoformat()


# ============================================================================
# OBITUARY MOCK GENERATOR
# ============================================================================

async def mock_obituary(full_name: str, location: str = "CA") -> Dict:
    """
    Generate realistic obituary lookup results
    
    Args:
        full_name: Name to search for
        location: Location filter
    
    Returns:
        Mock obituary response matching real API schema
    """
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating obituary data for {full_name}")
    
    await add_mock_latency()
    
    # Generate 1-3 obituary results
    num_results = random.randint(1, 3)
    obituaries = []
    
    for i in range(num_results):
        obituaries.append({
            "source": random.choice(["legacy.com", "tributes.com", "local_newspaper"]),
            "url": f"https://www.legacy.com/obituaries/name/{random.randint(10000, 99999)}",
            "full_name": full_name,
            "date_of_death": random_date(days_back=60),
            "date_of_birth": f"{random.randint(1940, 1990)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            "age": random.randint(50, 95),
            "location": location,
            "funeral_home": random.choice([
                "Smith Family Funeral Home",
                "Johnson Memorial Services",
                "Williams & Sons Funeral Directors"
            ]),
            "confidence": round(random.uniform(0.75, 0.98), 2),
            "snippet": f"Beloved {random.choice(['father', 'mother', 'husband', 'wife'])} passed away peacefully...",
            "relatives": random.randint(3, 8)
        })
    
    return {
        "obituaries": obituaries,
        "total_found": num_results,
        "search_query": full_name,
        "location_filter": location,
        "confidence_avg": round(sum(o["confidence"] for o in obituaries) / num_results, 2),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# BLOCKCHAIN BALANCE MOCK GENERATOR
# ============================================================================

async def mock_blockchain_balance(address: str, chains: List[str]) -> Dict:
    """
    Generate realistic blockchain balance data
    
    Args:
        address: Wallet address
        chains: List of blockchain networks
    
    Returns:
        Mock blockchain response matching real API schema
    """
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating blockchain balance for {address[:10]}...")
    
    await add_mock_latency()
    
    balances = []
    total_usd = 0.0
    
    for chain in chains:
        # Generate realistic balance
        if chain == "ETH":
            balance = round(random.uniform(0.1, 5.0), 4)
            price_usd = 3200.00
        elif chain == "BTC":
            balance = round(random.uniform(0.01, 0.5), 6)
            price_usd = 42000.00
        elif chain == "MATIC":
            balance = round(random.uniform(100, 5000), 2)
            price_usd = 0.85
        else:
            balance = round(random.uniform(1, 1000), 2)
            price_usd = 1.00
        
        balance_usd = balance * price_usd
        total_usd += balance_usd
        
        # Generate token holdings
        tokens = []
        if random.random() > 0.3:  # 70% chance of having tokens
            num_tokens = random.randint(1, 3)
            for _ in range(num_tokens):
                token_balance = round(random.uniform(100, 10000), 2)
                tokens.append({
                    "symbol": random.choice(["USDC", "USDT", "DAI", "LINK", "UNI"]),
                    "balance": token_balance,
                    "balance_usd": token_balance  # Stablecoins assumed ~$1
                })
        
        balances.append({
            "chain": chain,
            "address": address,
            "balance": balance,
            "balance_usd": round(balance_usd, 2),
            "tokens": tokens
        })
    
    return {
        "balances": balances,
        "total_usd": round(total_usd, 2),
        "chains_scanned": len(chains),
        "block_height": random.randint(18000000, 19000000),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# EMAIL ACTIVITY MOCK GENERATOR
# ============================================================================

async def mock_email_activity(days_back: int = 7, filter_keywords: List[str] = None) -> Dict:
    """
    Generate realistic email activity data
    
    Args:
        days_back: How many days back to scan
        filter_keywords: Keywords to filter emails
    
    Returns:
        Mock email response matching real API schema
    """
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating email activity for last {days_back} days")
    
    await add_mock_latency()
    
    # Generate 5-20 emails
    num_emails = random.randint(5, 20)
    emails = []
    condolence_count = 0
    
    filter_keywords = filter_keywords or ["funeral", "condolence", "sympathy", "passed away"]
    
    for i in range(num_emails):
        # Randomly decide if this is a condolence email
        is_condolence = random.random() > 0.6
        
        if is_condolence:
            condolence_count += 1
            subject = random.choice([
                "Our deepest condolences",
                "Thinking of you during this difficult time",
                "So sorry for your loss",
                "With sympathy and love",
                "Funeral service information"
            ])
            sentiment = "sad"
            matched_keywords = random.sample(filter_keywords, k=random.randint(1, 2))
        else:
            subject = random.choice([
                "Weekly newsletter",
                "Account update",
                "Meeting reminder",
                "Project status",
                "Invoice attached"
            ])
            sentiment = "neutral"
            matched_keywords = []
        
        emails.append({
            "from": f"{random.choice(['john', 'mary', 'david', 'sarah'])}@example.com",
            "subject": subject,
            "date": random_date(days_back=days_back),
            "snippet": f"Email preview text for {subject[:30]}...",
            "sentiment": sentiment,
            "keywords_matched": matched_keywords,
            "has_attachments": random.random() > 0.7
        })
    
    return {
        "emails": emails,
        "total_count": num_emails,
        "condolence_email_count": condolence_count,
        "days_scanned": days_back,
        "unread_count": random.randint(0, num_emails // 2),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# CLOUD ACTIVITY MOCK GENERATOR
# ============================================================================

async def mock_cloud_activity(services: List[str] = None) -> Dict:
    """
    Generate realistic cloud storage activity data
    
    Args:
        services: List of cloud services to scan
    
    Returns:
        Mock cloud activity response matching real API schema
    """
    
    services = services or ["google_drive", "dropbox"]
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating cloud activity for {len(services)} services")
    
    await add_mock_latency()
    
    activity = []
    total_files = 0
    total_storage_gb = 0.0
    
    for service in services:
        file_count = random.randint(100, 5000)
        storage_gb = round(random.uniform(5.0, 100.0), 2)
        
        total_files += file_count
        total_storage_gb += storage_gb
        
        # Generate recent files
        recent_files = []
        for i in range(random.randint(5, 10)):
            recent_files.append({
                "name": random.choice([
                    "Important_Documents.pdf",
                    "Family_Photos_2024.zip",
                    "Tax_Returns_2024.xlsx",
                    "Medical_Records.pdf",
                    "Will_and_Testament.docx",
                    "Insurance_Policy.pdf"
                ]),
                "modified": random_date(days_back=30),
                "size_mb": round(random.uniform(0.1, 50.0), 2),
                "type": random.choice(["pdf", "docx", "xlsx", "jpg", "zip"])
            })
        
        activity.append({
            "service": service,
            "last_modified": random_date(days_back=7),
            "file_count": file_count,
            "storage_used_gb": storage_gb,
            "recent_files": recent_files,
            "shared_items": random.randint(0, 20),
            "account_type": random.choice(["free", "premium"])
        })
    
    return {
        "activity": activity,
        "total_files": total_files,
        "total_storage_gb": round(total_storage_gb, 2),
        "services_scanned": len(services),
        "last_sync": random_date(days_back=1),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# CRYPTO PRICES MOCK GENERATOR
# ============================================================================

async def mock_crypto_prices(symbols: str) -> Dict:
    """
    Generate realistic crypto price data
    
    Args:
        symbols: Comma-separated crypto symbols
    
    Returns:
        Mock crypto price response
    """
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating crypto prices for {symbols}")
    
    await add_mock_latency()
    
    symbol_list = [s.strip() for s in symbols.split(",")]
    
    # Realistic base prices
    base_prices = {
        "BTC": 42000.00,
        "ETH": 3200.00,
        "MATIC": 0.85,
        "BNB": 320.00,
        "SOL": 95.00,
        "ADA": 0.45
    }
    
    prices = []
    for symbol in symbol_list:
        base_price = base_prices.get(symbol, 100.00)
        # Add random variation ±5%
        price = round(base_price * random.uniform(0.95, 1.05), 2)
        change_24h = round(random.uniform(-8.0, 8.0), 2)
        
        prices.append({
            "symbol": symbol,
            "price_usd": price,
            "change_24h": change_24h,
            "volume_24h": round(random.uniform(1e9, 5e10), 2),
            "market_cap": round(price * random.uniform(1e8, 1e11), 2)
        })
    
    return {
        "prices": prices,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# GAS PRICE MOCK GENERATOR
# ============================================================================

async def mock_gas_price(chain: str = "ethereum") -> Dict:
    """
    Generate realistic gas price data
    
    Args:
        chain: Blockchain network
    
    Returns:
        Mock gas price response
    """
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating gas prices for {chain}")
    
    await add_mock_latency()
    
    # Realistic gas prices based on network
    if chain == "ethereum":
        base_gas = 30
    elif chain == "polygon":
        base_gas = 50
    else:
        base_gas = 20
    
    # Add random variation
    safe = base_gas + random.randint(-5, 5)
    standard = safe + random.randint(5, 15)
    fast = standard + random.randint(10, 25)
    
    return {
        "chain": chain,
        "safe": max(1, safe),
        "standard": standard,
        "fast": fast,
        "block_number": random.randint(18000000, 19000000),
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# DEATH REGISTRY MOCK GENERATOR
# ============================================================================

async def mock_death_registry(full_name: str, date_of_birth: str = None) -> Dict:
    """
    Generate realistic death registry verification
    
    Args:
        full_name: Name to verify
        date_of_birth: DOB for verification
    
    Returns:
        Mock death registry response
    """
    
    if LOG_MOCK_GENERATION:
        print(f"  [MOCK] Generating death registry for {full_name}")
    
    await add_mock_latency()
    
    # 80% chance of verification
    verified = random.random() > 0.2
    
    if verified:
        return {
            "verified": True,
            "certificate_number": f"2025-{random.choice(['CA', 'NY', 'TX'])}-{random.randint(10000, 99999)}",
            "date_of_death": random_date(days_back=30),
            "issuing_authority": random.choice([
                "California Department of Public Health",
                "New York State Department of Health",
                "Texas Department of State Health Services"
            ]),
            "confidence": round(random.uniform(0.90, 0.99), 2),
            "timestamp": datetime.now().isoformat()
        }
    else:
        return {
            "verified": False,
            "error": "No matching record found",
            "confidence": 0.0,
            "timestamp": datetime.now().isoformat()
        }


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "mock_obituary",
    "mock_blockchain_balance",
    "mock_email_activity",
    "mock_cloud_activity",
    "mock_crypto_prices",
    "mock_gas_price",
    "mock_death_registry",
]
