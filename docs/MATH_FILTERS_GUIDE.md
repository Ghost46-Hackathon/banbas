# Mathematical Template Filters Guide

This document provides a comprehensive guide to using the mathematical template filters available in the Banbas Resort system.

## Setup

To use these filters in any Django template, add this line at the top of your template:

```django
{% load math_filters %}
```

## Basic Mathematical Operations

### Multiplication
```django
{{ room_price|multiply:nights }}
{{ base_rate|multiply:1.15 }}  <!-- Add 15% markup -->
```

### Division
```django
{{ total_cost|divide:guests }}
{{ annual_revenue|divide:12 }}  <!-- Monthly average -->
```

## Percentage Calculations

### Calculate Percentage Amount
```django
{{ room_price|percentage:10 }}  <!-- 10% of room price -->
{{ total|percentage:tax_rate }}
```

### Add Percentage
```django
{{ subtotal|add_percentage:tax_rate }}  <!-- subtotal + tax -->
{{ base_price|add_percentage:15 }}      <!-- base price + 15% -->
```

### Subtract Percentage
```django
{{ original_price|subtract_percentage:discount }}  <!-- Apply discount -->
{{ list_price|subtract_percentage:20 }}           <!-- 20% off -->
```

## Currency Operations

### Currency Multiplication (with formatting)
```django
{{ room_rate|currency_multiply:nights }}  <!-- Returns formatted string like "450.00" -->
{{ unit_price|currency_multiply:quantity }}
```

### Currency Division (with formatting)
```django
{{ total_amount|currency_divide:installments }}  <!-- Monthly payment -->
{{ group_cost|currency_divide:group_size }}      <!-- Per person cost -->
```

## Tax and Discount Calculations

### Calculate Tax Amount
```django
{{ subtotal|calculate_tax:8.5 }}  <!-- Calculate 8.5% tax -->
Tax: ${{ subtotal|calculate_tax:tax_rate|floatformat:2 }}
```

### Calculate Discount Amount
```django
{{ original_price|calculate_discount:member_discount }}
You Save: ${{ price|calculate_discount:20|floatformat:2 }}
```

## Rounding and Formatting

### Round to Decimal Places
```django
{{ price|round_to:2 }}    <!-- Round to 2 decimal places -->
{{ average|round_to:0 }}  <!-- Round to nearest integer -->
```

### Floor and Ceiling
```django
{{ rating|floor }}    <!-- Round down -->
{{ guests|ceiling }}  <!-- Round up for capacity planning -->
```

## Advanced Mathematical Functions

### Power
```django
{{ base|power:2 }}  <!-- Square -->
{{ growth_rate|power:years }}
```

### Square Root
```django
{{ area|square_root }}  <!-- Calculate side length -->
```

### Absolute Value
```django
{{ temperature_diff|absolute }}
{{ balance|absolute }}  <!-- Always positive -->
```

### Modulo (Remainder)
```django
{{ day_number|modulo:7 }}      <!-- Day of week -->
{{ item_count|modulo:items_per_page }}
```

## Comparison Operations

### Minimum/Maximum
```django
{{ user_budget|min_value:room_price }}  <!-- Don't exceed budget -->
{{ occupancy|max_value:1 }}             <!-- Cap at 100% -->
```

## Utility Filters

### Even/Odd Detection
```django
{% if forloop.counter0|is_even %}
    <div class="even-row">{{ item }}</div>
{% else %}
    <div class="odd-row">{{ item }}</div>
{% endif %}
```

## Real-World Examples

### Room Booking Calculation
```django
<!-- Calculate total cost -->
{% load math_filters %}

<div class="booking-summary">
    <h3>Booking Summary</h3>
    
    <div class="line-item">
        <span>Room Rate ({{ nights }} nights):</span>
        <span>${{ room.price|currency_multiply:nights }}</span>
    </div>
    
    {% if taxes %}
    <div class="line-item">
        <span>Taxes ({{ tax_rate }}%):</span>
        <span>${{ room.price|multiply:nights|calculate_tax:tax_rate|round_to:2 }}</span>
    </div>
    {% endif %}
    
    {% if discount_rate %}
    <div class="line-item discount">
        <span>Discount ({{ discount_rate }}%):</span>
        <span>-${{ room.price|multiply:nights|calculate_discount:discount_rate|round_to:2 }}</span>
    </div>
    {% endif %}
    
    <div class="total">
        {% with subtotal=room.price|multiply:nights %}
        {% with tax_amount=subtotal|calculate_tax:tax_rate %}
        {% with discount_amount=subtotal|calculate_discount:discount_rate %}
        <span>Total:</span>
        <span>${{ subtotal|add:tax_amount|subtract:discount_amount|round_to:2 }}</span>
        {% endwith %}
        {% endwith %}
        {% endwith %}
    </div>
</div>
```

### Revenue Analytics
```django
<!-- Monthly revenue breakdown -->
{% load math_filters %}

<div class="revenue-stats">
    <h3>Revenue Analytics</h3>
    
    <div class="metric">
        <span>Average Daily Revenue:</span>
        <span>${{ total_revenue|currency_divide:days_in_period }}</span>
    </div>
    
    <div class="metric">
        <span>Revenue per Available Room:</span>
        <span>${{ total_revenue|currency_divide:total_room_nights }}</span>
    </div>
    
    <div class="metric">
        <span>Growth vs Last Period:</span>
        <span>{{ current_revenue|subtract:previous_revenue|divide:previous_revenue|multiply:100|round_to:1 }}%</span>
    </div>
</div>
```

### Group Booking Calculator
```django
<!-- Calculate per-person costs -->
{% load math_filters %}

<div class="group-booking">
    <h3>Group Booking ({{ group_size }} people)</h3>
    
    <div class="cost-breakdown">
        <div>Total Cost: ${{ total_cost }}</div>
        <div>Per Person: ${{ total_cost|currency_divide:group_size }}</div>
        
        {% if group_size|is_even %}
        <div class="note">Even number of guests - perfect for double occupancy</div>
        {% else %}
        <div class="note">Odd number of guests - one single supplement may apply</div>
        {% endif %}
        
        <div>Rooms needed: {{ group_size|add:1|divide:2|floor }}</div>
    </div>
</div>
```

## Error Handling

All filters include robust error handling:
- Invalid inputs return sensible defaults (usually 0 or "0.00")
- Division by zero returns 0
- Negative square roots return 0
- Type conversion errors are handled gracefully

## Performance Notes

- Filters perform calculations in Python, so avoid complex chains in loops
- For heavy calculations, consider doing them in views instead
- Currency formatting filters return strings, not numbers
- Use `round_to` for precise decimal control instead of `floatformat`

## Best Practices

1. **Use currency filters for money**: `currency_multiply` and `currency_divide`
2. **Chain filters logically**: `{{ value|multiply:rate|round_to:2 }}`
3. **Handle edge cases**: Check for zero values when dividing
4. **Use with template variables**: Store complex calculations in variables
5. **Document your usage**: Add comments for complex filter chains