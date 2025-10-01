# Currency Conversion Feature

## Overview

The Banbas Resort Management System now includes automatic currency conversion functionality for reservation pricing. This feature allows users to seamlessly convert prices between different currencies when creating or editing reservations.

## Supported Currencies

- **NRS** (Nepali Rupee) - Base currency
- **INR** (Indian Rupee) 
- **USD** (US Dollar)
- **EUR** (Euro)

## Features

### 1. Automatic Currency Symbol Update
When you select a currency, the input field symbol automatically updates to show the correct currency symbol:
- NRS: रु
- INR: ₹
- USD: $
- EUR: €

### 2. Smart Price Conversion
When you change the currency selection, the system:
1. Detects if there's an existing price in the field
2. Shows a conversion prompt with the calculated equivalent
3. Allows you to choose whether to convert or keep the current value
4. Provides visual feedback on successful conversion

### 3. Manual Conversion Button
A convert button (⇄) is available next to the price field for manual conversion at any time.

## How It Works

### For Users

1. **Enter a price** in any supported currency
2. **Select a different currency** from the dropdown
3. **Choose conversion option** from the popup:
   - "Yes, Convert" - automatically converts the price
   - "Keep Current" - keeps the original price value
4. **Visual confirmation** shows the conversion details

### Example Conversion Flow

1. Enter `10000` NRS
2. Change currency to USD
3. System shows: "Convert रु10000.00 (NRS) to $75.00 (USD)?"
4. Click "Yes, Convert"
5. Price field updates to `75.00`
6. Success message confirms the conversion

## Exchange Rates

### Current Rates (Base: NRS)
- 1 NRS = 0.625 INR
- 1 NRS = 0.0075 USD  
- 1 NRS = 0.0069 EUR

### Updating Exchange Rates

#### Method 1: Management Command
```bash
# List current rates
python manage.py update_currency_rates --list

# Update a specific rate
python manage.py update_currency_rates --currency USD --rate 0.0076

# Future: Auto-update (not yet implemented)
python manage.py update_currency_rates --auto
```

#### Method 2: Edit Configuration File
Edit `backoffice/currency_rates.py` and update the `EXCHANGE_RATES` dictionary:

```python
EXCHANGE_RATES = {
    'NRS': 1.0,        # Base currency
    'INR': 0.625,      # Updated rate
    'USD': 0.0076,     # Updated rate
    'EUR': 0.0069,     # Updated rate
}
```

## Technical Implementation

### JavaScript Functions
- `convertCurrency(amount, fromCurrency, toCurrency)` - Core conversion logic
- `updateCurrencySymbol(currency)` - Updates display symbols
- `showConversionOption()` - Shows conversion prompts
- `showConversionSuccess()` - Shows success feedback

### Backend Configuration
- `backoffice/currency_rates.py` - Exchange rates configuration
- `backoffice/management/commands/update_currency_rates.py` - Rate update utility

### Rate Update History
The system maintains a history of rate updates for audit purposes:

```python
RATE_UPDATE_HISTORY = [
    {
        'date': '2025-09-30',
        'updated_by': 'management_command',
        'note': 'Updated USD rate from 0.0075 to 0.0076',
        'rates': {...}
    }
]
```

## User Interface

### Visual Elements
- **Currency symbol** updates automatically in the input group
- **Conversion button** (⇄) for manual conversions  
- **Toast notifications** for conversion prompts and confirmations
- **Animated slide-in** notifications from the right side
- **Color-coded alerts** (blue for prompts, green for success)

### Accessibility
- Clear visual feedback for all currency changes
- Non-intrusive popup notifications
- Option to dismiss or ignore conversion suggestions
- Keyboard-friendly interface

## Best Practices

### For Administrators
1. **Update rates regularly** to maintain accuracy
2. **Use management commands** for rate updates to maintain history
3. **Test conversions** after rate updates
4. **Monitor rate history** for audit trails

### For Users
1. **Double-check converted prices** before saving reservations
2. **Use appropriate currency** for the guest's region
3. **Consider exchange rate fluctuations** for future-dated reservations

## Troubleshooting

### Common Issues

**Problem**: Conversion not working
- **Solution**: Check JavaScript console for errors, ensure currency rates are loaded

**Problem**: Wrong conversion amounts
- **Solution**: Verify exchange rates in `currency_rates.py`

**Problem**: Currency symbol not updating
- **Solution**: Clear browser cache and reload the page

### Error Handling
- Invalid currency codes are handled gracefully
- Missing exchange rates show appropriate error messages  
- Network issues don't break the form functionality

## Future Enhancements

1. **Live exchange rate API** integration
2. **Additional currency support**
3. **Rate change notifications** for administrators
4. **Conversion history** tracking per reservation
5. **Bulk rate updates** from external sources

## Support

For technical issues with currency conversion:
1. Check the browser console for JavaScript errors
2. Verify exchange rates configuration
3. Test with different currencies
4. Contact system administrator for rate updates

---

*Last updated: 2025-09-30*  
*Feature implemented as part of Banbas Resort Management System v1.1*