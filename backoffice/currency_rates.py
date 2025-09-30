# Currency Exchange Rates Configuration
# Last updated: 2025-09-30
# Base currency: NRS (Nepali Rupee)

"""
Currency exchange rates for automatic price conversion in the reservation system.

The rates are based on NRS (Nepali Rupee) as the base currency.
Update these rates periodically to maintain accuracy.

Example usage:
- 1000 NRS = 625 INR (1000 * 0.625)
- 1000 NRS = 7.5 USD (1000 * 0.0075)
- 1000 NRS = 6.9 EUR (1000 * 0.0069)
"""

EXCHANGE_RATES = {
    'NRS': 1.0,        # Nepali Rupee (base currency)
    'INR': 0.625,      # Indian Rupee (1 NRS = 0.625 INR)
    'USD': 0.0075,     # US Dollar (1 NRS = 0.0075 USD)
    'EUR': 0.0069,     # Euro (1 NRS = 0.0069 EUR)
}

# Currency display symbols
CURRENCY_SYMBOLS = {
    'NRS': 'रु',        # Nepali Rupee symbol
    'INR': '₹',         # Indian Rupee symbol
    'USD': '$',         # US Dollar symbol
    'EUR': '€',         # Euro symbol
}

# Currency full names
CURRENCY_NAMES = {
    'NRS': 'Nepali Rupee',
    'INR': 'Indian Rupee',
    'USD': 'US Dollar',
    'EUR': 'Euro',
}

def convert_currency(amount, from_currency, to_currency):
    """
    Convert amount from one currency to another.
    
    Args:
        amount (float): Amount to convert
        from_currency (str): Source currency code
        to_currency (str): Target currency code
    
    Returns:
        float: Converted amount
    
    Example:
        convert_currency(1000, 'NRS', 'USD')  # Returns 7.5
        convert_currency(100, 'USD', 'NRS')   # Returns 13333.33
    """
    if from_currency == to_currency:
        return amount
    
    if from_currency not in EXCHANGE_RATES or to_currency not in EXCHANGE_RATES:
        raise ValueError(f"Unsupported currency. Supported: {list(EXCHANGE_RATES.keys())}")
    
    # Convert to NRS first, then to target currency
    amount_in_nrs = amount / EXCHANGE_RATES[from_currency]
    return amount_in_nrs * EXCHANGE_RATES[to_currency]

def get_currency_symbol(currency_code):
    """Get the display symbol for a currency code."""
    return CURRENCY_SYMBOLS.get(currency_code, currency_code)

def get_currency_name(currency_code):
    """Get the full name for a currency code."""
    return CURRENCY_NAMES.get(currency_code, currency_code)

def get_supported_currencies():
    """Get list of supported currency codes."""
    return list(EXCHANGE_RATES.keys())

# Rate update history for tracking
RATE_UPDATE_HISTORY = [
    {
        'date': '2025-09-30',
        'updated_by': 'system',
        'note': 'Initial rates setup',
        'rates': EXCHANGE_RATES.copy()
    }
]