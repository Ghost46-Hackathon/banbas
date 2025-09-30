from django.core.management.base import BaseCommand
from django.utils import timezone
import json
import os
from decimal import Decimal


class Command(BaseCommand):
    help = 'Update currency exchange rates in the currency_rates.py file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--currency',
            type=str,
            help='Currency code to update (e.g., USD, EUR, INR)'
        )
        parser.add_argument(
            '--rate',
            type=float,
            help='New exchange rate relative to NRS'
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List current exchange rates'
        )
        parser.add_argument(
            '--auto',
            action='store_true',
            help='Auto-update rates from external API (not implemented yet)'
        )

    def handle(self, *args, **options):
        currency_file = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            '..', 
            'currency_rates.py'
        )
        
        # Import current rates
        try:
            import sys
            sys.path.insert(0, os.path.dirname(currency_file))
            from currency_rates import EXCHANGE_RATES, RATE_UPDATE_HISTORY
        except ImportError:
            self.stdout.write(
                self.style.ERROR('Could not import currency_rates.py')
            )
            return

        if options['list']:
            self.list_current_rates(EXCHANGE_RATES)
            return

        if options['currency'] and options['rate']:
            self.update_single_rate(
                currency_file, 
                options['currency'], 
                options['rate'],
                EXCHANGE_RATES,
                RATE_UPDATE_HISTORY
            )
            return

        if options['auto']:
            self.stdout.write(
                self.style.WARNING('Auto-update not implemented yet. Use --currency and --rate for manual updates.')
            )
            return

        self.stdout.write(
            self.style.WARNING('Please specify --list, --currency with --rate, or --auto')
        )

    def list_current_rates(self, rates):
        self.stdout.write(self.style.SUCCESS('Current Exchange Rates (Base: NRS)'))
        self.stdout.write('-' * 40)
        for currency, rate in rates.items():
            if currency == 'NRS':
                self.stdout.write(f'{currency}: {rate} (Base Currency)')
            else:
                # Show both directions
                nrs_to_currency = rate
                currency_to_nrs = 1 / rate
                self.stdout.write(
                    f'{currency}: 1 NRS = {nrs_to_currency:.4f} {currency} | 1 {currency} = {currency_to_nrs:.2f} NRS'
                )

    def update_single_rate(self, file_path, currency, rate, current_rates, history):
        currency = currency.upper()
        
        if currency == 'NRS':
            self.stdout.write(
                self.style.ERROR('Cannot update NRS rate as it is the base currency')
            )
            return

        if currency not in current_rates:
            self.stdout.write(
                self.style.ERROR(f'Currency {currency} not supported. Supported currencies: {list(current_rates.keys())}')
            )
            return

        old_rate = current_rates[currency]
        
        # Read current file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the rate in the file content
        old_line = f"    '{currency}': {old_rate},"
        new_line = f"    '{currency}': {rate},"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
        else:
            # Try different formatting
            for possible_old in [
                f"    '{currency}': {old_rate:.4f},",
                f"    '{currency}': {old_rate:.3f},",
                f"    '{currency}': {old_rate:.6f},",
            ]:
                if possible_old in content:
                    content = content.replace(possible_old, new_line)
                    break

        # Update the history section
        today = timezone.now().strftime('%Y-%m-%d')
        new_history_entry = f"""    {{
        'date': '{today}',
        'updated_by': 'management_command',
        'note': 'Updated {currency} rate from {old_rate} to {rate}',
        'rates': EXCHANGE_RATES.copy()
    }}"""

        # Add to history
        history_marker = "RATE_UPDATE_HISTORY = ["
        history_insert_point = content.find(history_marker) + len(history_marker)
        content = content[:history_insert_point] + "\n" + new_history_entry + "," + content[history_insert_point:]

        # Update the last updated comment at the top
        import re
        content = re.sub(
            r'# Last updated: \d{4}-\d{2}-\d{2}',
            f'# Last updated: {today}',
            content
        )

        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {currency} rate from {old_rate} to {rate}'
            )
        )
        self.stdout.write(
            f'1 NRS = {rate:.4f} {currency} | 1 {currency} = {1/rate:.2f} NRS'
        )