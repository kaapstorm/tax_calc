"""
Test cases that verify the worked examples from DESIGN.md
"""

from optimise_tax import calc_div_tax, calc_wage_tax


def test_design_worked_example():
    """
    Test the worked example from DESIGN.md:

    "Suppose you earn £32,570 in total income, including £3,000 in dividends.
    - Subtract the Personal Allowance (£12,570): £32,570 - £12,570 = £20,000 (taxable income).
    - The first £500 of dividend income is tax-free.
    - The remaining £2,500 is taxed at 8.75%, because the total taxable income falls within the basic rate band."
    """
    total_income = 32570
    dividends = 3000
    wages = total_income - dividends  # £29,570

    # Calculate dividend tax
    dividend_tax = calc_div_tax(dividends, wages, 'eng')

    # Expected calculation:
    # - £500 dividend allowance is tax-free
    # - Remaining £2,500 taxed at 8.75% (basic rate)
    # - Expected tax: £2,500 * 0.0875 = £218.75
    expected_dividend_tax = 2500 * 0.0875

    assert abs(dividend_tax - expected_dividend_tax) < 0.01, (
        f'Expected dividend tax £{expected_dividend_tax:.2f}, '
        f'got £{dividend_tax:.2f}'
    )

    # Verify the total taxable income calculation
    # Total income £32,570 - Personal Allowance £12,570 = £20,000 taxable
    # This should place the dividends in the basic rate band (8.75%)
    taxable_income = total_income - 12570
    assert taxable_income == 20000, (
        f'Expected taxable income £20,000, got £{taxable_income}'
    )

    # Also verify wage tax calculation for completeness
    wage_tax = calc_wage_tax(wages, 'eng')

    # Expected wage tax calculation:
    # Wages £29,570 - Personal Allowance £12,570 = £17,000 taxable
    # £17,000 * 20% (basic rate) = £3,400
    expected_wage_tax = 17000 * 0.20

    assert abs(wage_tax - expected_wage_tax) < 0.01, (
        f'Expected wage tax £{expected_wage_tax:.2f}, got £{wage_tax:.2f}'
    )


def test_dividend_allowance_boundary():
    """Test that the £500 dividend allowance is applied correctly"""
    wages = 20000

    # Test with dividends exactly at allowance
    dividend_tax_500 = calc_div_tax(500, wages, 'eng')
    assert dividend_tax_500 == 0, 'First £500 should be tax-free'

    # Test with dividends just above allowance
    dividend_tax_501 = calc_div_tax(501, wages, 'eng')
    expected_tax = 1 * 0.0875  # £1 at 8.75%
    assert abs(dividend_tax_501 - expected_tax) < 0.01


def test_basic_rate_band_boundary():
    """Test dividend tax at basic rate band boundary"""
    # Test scenario where total income is at basic rate band limit
    # Basic rate band ends at £50,270 total income
    wages = 47270  # £47,270 wages
    dividends = 3000  # + £3,000 dividends = £50,270 total

    dividend_tax = calc_div_tax(dividends, wages, 'eng')

    # All dividends (minus £500 allowance) should be at 8.75% rate
    expected_tax = (dividends - 500) * 0.0875
    assert abs(dividend_tax - expected_tax) < 0.01
