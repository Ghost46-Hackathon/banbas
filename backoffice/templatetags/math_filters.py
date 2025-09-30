"""
Mathematical template filters for Django templates.

These filters provide mathematical operations that can be used throughout
the Django template system for calculations, formatting, and data manipulation.

Usage in templates:
    {% load math_filters %}
    
    {{ value|multiply:2 }}
    {{ total|divide:count }}
    {{ price|percentage:tax_rate }}
    {{ amount|round_to:2 }}

"""

from django import template
from django.template.defaultfilters import floatformat
from decimal import Decimal, ROUND_HALF_UP
import math

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the argument.
    
    Usage: {{ value|multiply:2 }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """
    Divides the value by the argument.
    
    Usage: {{ value|divide:2 }}
    Returns 0 if division by zero is attempted.
    """
    try:
        divisor = float(arg)
        if divisor == 0:
            return 0
        return float(value) / divisor
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, arg):
    """
    Calculates percentage of value.
    
    Usage: {{ amount|percentage:15 }} (calculates 15% of amount)
    """
    try:
        return float(value) * (float(arg) / 100)
    except (ValueError, TypeError):
        return 0


@register.filter
def add_percentage(value, arg):
    """
    Adds percentage to the value.
    
    Usage: {{ price|add_percentage:tax_rate }} (price + tax_rate% of price)
    """
    try:
        base = float(value)
        percent = float(arg) / 100
        return base + (base * percent)
    except (ValueError, TypeError):
        return 0


@register.filter
def subtract_percentage(value, arg):
    """
    Subtracts percentage from the value.
    
    Usage: {{ price|subtract_percentage:discount_rate }}
    """
    try:
        base = float(value)
        percent = float(arg) / 100
        return base - (base * percent)
    except (ValueError, TypeError):
        return 0


@register.filter
def power(value, arg):
    """
    Raises value to the power of arg.
    
    Usage: {{ value|power:2 }}
    """
    try:
        return math.pow(float(value), float(arg))
    except (ValueError, TypeError):
        return 0


@register.filter
def modulo(value, arg):
    """
    Returns the remainder of value divided by arg.
    
    Usage: {{ value|modulo:3 }}
    """
    try:
        return float(value) % float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def round_to(value, decimal_places):
    """
    Rounds value to specified number of decimal places.
    
    Usage: {{ value|round_to:2 }}
    """
    try:
        decimal_value = Decimal(str(value))
        decimal_places = int(decimal_places)
        
        # Create the quantize pattern (e.g., '0.01' for 2 decimal places)
        quantize_pattern = '0.' + '0' * decimal_places if decimal_places > 0 else '1'
        
        return float(decimal_value.quantize(
            Decimal(quantize_pattern), 
            rounding=ROUND_HALF_UP
        ))
    except (ValueError, TypeError):
        return 0


@register.filter
def absolute(value):
    """
    Returns the absolute value.
    
    Usage: {{ value|absolute }}
    """
    try:
        return abs(float(value))
    except (ValueError, TypeError):
        return 0


@register.filter
def floor(value):
    """
    Returns the floor of the value (largest integer less than or equal to value).
    
    Usage: {{ value|floor }}
    """
    try:
        return math.floor(float(value))
    except (ValueError, TypeError):
        return 0


@register.filter
def ceiling(value):
    """
    Returns the ceiling of the value (smallest integer greater than or equal to value).
    
    Usage: {{ value|ceiling }}
    """
    try:
        return math.ceil(float(value))
    except (ValueError, TypeError):
        return 0


@register.filter
def square_root(value):
    """
    Returns the square root of the value.
    
    Usage: {{ value|square_root }}
    """
    try:
        num = float(value)
        if num < 0:
            return 0  # Return 0 for negative numbers instead of error
        return math.sqrt(num)
    except (ValueError, TypeError):
        return 0


@register.filter
def min_value(value, arg):
    """
    Returns the minimum of value and arg.
    
    Usage: {{ value|min_value:100 }}
    """
    try:
        return min(float(value), float(arg))
    except (ValueError, TypeError):
        return 0


@register.filter
def max_value(value, arg):
    """
    Returns the maximum of value and arg.
    
    Usage: {{ value|max_value:100 }}
    """
    try:
        return max(float(value), float(arg))
    except (ValueError, TypeError):
        return 0


@register.filter
def currency_multiply(value, arg):
    """
    Multiplies and formats as currency with 2 decimal places.
    Useful for price calculations in templates.
    
    Usage: {{ base_price|currency_multiply:quantity }}
    """
    try:
        result = float(value) * float(arg)
        return f"{result:.2f}"
    except (ValueError, TypeError):
        return "0.00"


@register.filter
def currency_divide(value, arg):
    """
    Divides and formats as currency with 2 decimal places.
    
    Usage: {{ total_amount|currency_divide:installments }}
    """
    try:
        divisor = float(arg)
        if divisor == 0:
            return "0.00"
        result = float(value) / divisor
        return f"{result:.2f}"
    except (ValueError, TypeError):
        return "0.00"


@register.filter
def calculate_tax(value, tax_rate):
    """
    Calculates tax amount from a base value and tax rate.
    
    Usage: {{ subtotal|calculate_tax:tax_rate }}
    """
    try:
        base = float(value)
        rate = float(tax_rate) / 100
        return base * rate
    except (ValueError, TypeError):
        return 0


@register.filter
def calculate_discount(value, discount_rate):
    """
    Calculates discount amount from a base value and discount rate.
    
    Usage: {{ original_price|calculate_discount:discount_rate }}
    """
    try:
        base = float(value)
        rate = float(discount_rate) / 100
        return base * rate
    except (ValueError, TypeError):
        return 0


@register.filter
def is_even(value):
    """
    Returns True if the value is even, False otherwise.
    
    Usage: {% if forloop.counter0|is_even %}even{% else %}odd{% endif %}
    """
    try:
        return int(value) % 2 == 0
    except (ValueError, TypeError):
        return False


@register.filter
def is_odd(value):
    """
    Returns True if the value is odd, False otherwise.
    
    Usage: {% if forloop.counter0|is_odd %}odd{% else %}even{% endif %}
    """
    try:
        return int(value) % 2 != 0
    except (ValueError, TypeError):
        return False