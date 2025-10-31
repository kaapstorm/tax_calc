#!/usr/bin/env python3
import argparse


def get_tax_bands(country):
    # Personal allowance and relevant bands
    allowance = 12570

    if country == 'sco':
        bands = [
            (2827, 0.19),  # Starter Rate
            (14921, 0.20),  # Basic Rate
            (31092, 0.21),  # Intermediate Rate
            (62430, 0.42),  # Higher Rate
            (125140, 0.45),  # Top Rate
            (float('inf'), 0.48),  # Additional Rate
        ]
    else:  # 'eng', 'wal', 'ni'
        bands = [
            (37700, 0.20),  # Basic Rate
            (125140, 0.40),  # Higher Rate
            (float('inf'), 0.45),  # Additional Rate
        ]
    return allowance, bands


def get_dividend_bands(country):
    allowance = 500
    if country in ['eng', 'wal', 'ni']:
        bands = [(50270, 0.0875), (125140, 0.3375), (float('inf'), 0.3935)]
    else:  # 'sco'
        bands = [(14999, 0.0875), (43662, 0.3375), (float('inf'), 0.3935)]
    return allowance, bands


def personal_allowance(income):
    # Allowance is removed £1 for every £2 over £100,000 (UK-wide)
    pa = 12570
    if income > 100000:
        reduction = (income - 100000) // 2
        pa = max(0, pa - reduction)
    return pa


def calc_wage_tax(wage, country):
    pa, bands = get_tax_bands(country)
    taxable = max(0, wage - personal_allowance(wage))
    owed = 0
    last = 0
    for band_limit, rate in bands:
        band_amt = min(taxable, band_limit) - last
        if band_amt > 0:
            owed += band_amt * rate
        last = band_limit
        if last >= taxable:
            break
    return owed


def calc_div_tax(div, wage, country):
    allowance, bands = get_dividend_bands(country)
    taxable = max(0, div - allowance)
    # Tax band depends on wage + dividend total
    total = wage + div
    owed = 0
    last = wage
    for band_limit, rate in bands:
        band_amt = min(total, band_limit) - last
        div_band = min(taxable, band_amt)
        if div_band > 0:
            owed += div_band * rate
            taxable -= div_band
        last = band_limit
        if taxable <= 0:
            break
    return owed


def total_tax_split(amount, country):
    best_wage = 0
    best_dividend = 0
    min_tax = None
    # Try every possible split in steps of £1,000 (hundreds for fine tuning)
    step = 100
    for wage in range(0, int(amount) + 1, step):
        dividend = amount - wage
        wage_tax = calc_wage_tax(wage, country)
        div_tax = calc_div_tax(dividend, wage, country)
        total_tax = wage_tax + div_tax
        if (min_tax is None) or (total_tax < min_tax):
            min_tax = total_tax
            best_wage = wage
            best_dividend = dividend
    return best_wage, best_dividend, min_tax


def main():
    parser = argparse.ArgumentParser(
        description='Compute optimum split between wages and dividends for a '
                    'given total income.'
    )
    parser.add_argument(
        '--country', choices=['eng', 'sco', 'wal', 'ni'], default='eng'
    )
    parser.add_argument('income', type=float, help='Total income (GBP)')
    args = parser.parse_args()
    wage, dividend, tax = total_tax_split(args.income, args.country)
    print(f'For £{args.income:.2f} in {args.country.upper()}, optimum split:')
    print(f'Wages: £{wage:.2f}')
    print(f'Dividends: £{dividend:.2f}')
    print(f'Estimated combined tax: £{tax:.2f}')


if __name__ == '__main__':
    main()
