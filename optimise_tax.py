#!/usr/bin/env python3
import argparse
from pathlib import Path


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


def get_critical_wage_points(income, country):
    """
    Calculate all critical wage points where tax rates change.

    Returns sorted list of wages where the marginal tax rate changes
    for either wage tax or dividend tax calculations.
    """
    critical_wages = {0, income}

    # Add personal allowance boundary
    pa = personal_allowance(income)
    if 0 < pa < income:
        critical_wages.add(pa)

    # Add wage band boundaries
    _, wage_bands = get_tax_bands(country)
    for band_limit, _ in wage_bands:
        if band_limit != float('inf'):
            wage_at_boundary = band_limit + pa
            if 0 < wage_at_boundary < income:
                critical_wages.add(wage_at_boundary)

    # Add dividend band boundaries
    _, div_bands = get_dividend_bands(country)
    for band_limit, _ in div_bands:
        if band_limit != float('inf') and 0 < band_limit < income:
            critical_wages.add(band_limit)

    # For high earners, add £100k boundary
    if income > 100000:
        critical_wages.add(100000)

    return sorted(critical_wages)


def find_optimal_split(amount, country):
    """
    Find optimal wage/dividend split using intersection method.

    The optimal split occurs at critical points where marginal tax
    rates change (band boundaries). We evaluate all critical points
    and return the split with minimum total tax.
    """
    # Get all critical wage points
    critical_wages = get_critical_wage_points(amount, country)

    # Evaluate tax at each critical point
    best_wage = 0
    best_dividend = amount
    min_tax = float('inf')

    for wage in critical_wages:
        dividend = amount - wage
        wage_tax = calc_wage_tax(wage, country)
        div_tax = calc_div_tax(dividend, wage, country)
        total_tax = wage_tax + div_tax

        if total_tax < min_tax:
            min_tax = total_tax
            best_wage = wage
            best_dividend = dividend

    return best_wage, best_dividend, min_tax


def generate_graph(income, country, best_wage, best_dividend, min_tax):
    """
    Generate and save a graph showing total tax across wage/dividend splits.

    Uses line segments at critical points (tax band boundaries) for
    mathematical precision and computational efficiency.
    """
    import matplotlib.pyplot as plt

    # Get all critical wage points
    critical_wages = get_critical_wage_points(income, country)

    # Calculate tax at each critical point
    wages = []
    wage_taxes = []
    div_taxes = []
    total_taxes = []

    for wage in critical_wages:
        dividend = income - wage
        wage_tax = calc_wage_tax(wage, country)
        div_tax = calc_div_tax(dividend, wage, country)
        total_tax = wage_tax + div_tax

        wages.append(wage)
        wage_taxes.append(wage_tax)
        div_taxes.append(div_tax)
        total_taxes.append(total_tax)

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot as connected line segments
    ax.plot(wages, total_taxes, label='Total Tax', linewidth=2, color='red')
    ax.plot(
        wages,
        wage_taxes,
        label='Tax on Wages',
        linewidth=1.5,
        color='blue',
        linestyle='--',
    )
    ax.plot(
        wages,
        div_taxes,
        label='Tax on Dividends',
        linewidth=1.5,
        color='green',
        linestyle='--',
    )

    # Mark the optimal point
    ax.plot(
        best_wage,
        min_tax,
        'o',
        markersize=10,
        color='black',
        label=f'Optimal: £{best_wage:,.0f} wage, £{best_dividend:,.0f} div',
    )

    # Add labels and formatting
    ax.set_xlabel('Wage (£)', fontsize=12)
    ax.set_ylabel('Tax (£)', fontsize=12)
    ax.set_title(
        f'Tax Optimization for £{income:,.0f} Income ({country.upper()})',
        fontsize=14,
        fontweight='bold',
    )
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.ticklabel_format(style='plain', axis='both')

    # Save the figure
    filename = f'tax_optimization_{country}_{int(income)}.png'
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

    return Path(filename)


def main():
    parser = argparse.ArgumentParser(
        description='Compute optimum split between wages and dividends for a '
        'given total income.'
    )
    parser.add_argument(
        '--country', choices=['eng', 'sco', 'wal', 'ni'], default='eng'
    )
    parser.add_argument(
        '--graph',
        action='store_true',
        help='Render and save a graph in PNG showing the intersection of tax '
        'on wages and dividends',
    )
    parser.add_argument('income', type=float, help='Total income (GBP)')
    args = parser.parse_args()

    wage, dividend, tax = find_optimal_split(args.income, args.country)

    print(f'For £{args.income:.2f} in {args.country.upper()}, optimum split:')
    print(f'Wages: £{wage:.2f}')
    print(f'Dividends: £{dividend:.2f}')
    print(f'Estimated combined tax: £{tax:.2f}')

    if args.graph:
        graph_path = generate_graph(
            args.income, args.country, wage, dividend, tax
        )
        print(f'\nGraph saved to: {graph_path}')


if __name__ == '__main__':
    main()
