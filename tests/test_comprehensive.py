"""
Comprehensive test cases covering edge cases, all countries, and optimization verification
"""
from optimise_tax import (
    get_tax_bands, calc_wage_tax, calc_div_tax, 
    find_optimal_split, get_critical_wage_points
)


def test_personal_allowance_tapering():
    """Test personal allowance reduction for high earners"""
    
    # Below £100k - full personal allowance
    pa_low, _ = get_tax_bands('eng', 99999)
    assert pa_low == 12570, f'Expected full PA, got £{pa_low}'
    
    # At £100k - still full personal allowance
    pa_100k, _ = get_tax_bands('eng', 100000)
    assert pa_100k == 12570, f'Expected full PA at £100k, got £{pa_100k}'
    
    # At £110k - reduced by £5k (£10k income excess / 2)
    pa_110k, _ = get_tax_bands('eng', 110000)
    assert pa_110k == 7570, f'Expected £7,570 PA at £110k, got £{pa_110k}'
    
    # At £125,140 - personal allowance completely gone
    pa_125k, _ = get_tax_bands('eng', 125140)
    assert pa_125k == 0, f'Expected £0 PA at £125,140, got £{pa_125k}'
    
    # Above £125,140 - still zero
    pa_high, _ = get_tax_bands('eng', 150000)
    assert pa_high == 0, f'Expected £0 PA above £125k, got £{pa_high}'


def test_scotland_vs_england_differences():
    """Test that Scotland's tax bands differ from England's"""
    income = 50000
    
    eng_wage_tax = calc_wage_tax(income, 'eng')
    sco_wage_tax = calc_wage_tax(income, 'sco')
    
    # Scotland should have different (typically higher) tax
    assert eng_wage_tax != sco_wage_tax, (
        f'England and Scotland should have different tax rates. '
        f'England: £{eng_wage_tax:.2f}, Scotland: £{sco_wage_tax:.2f}'
    )
    
    # Verify Scotland has more tax bands
    _, eng_bands = get_tax_bands('eng', income)
    _, sco_bands = get_tax_bands('sco', income)
    
    assert len(sco_bands) > len(eng_bands), (
        f'Scotland should have more tax bands. '
        f'England: {len(eng_bands)}, Scotland: {len(sco_bands)}'
    )


def test_all_countries():
    """Test that all four UK countries work"""
    income = 40000
    countries = ['eng', 'sco', 'wal', 'ni']
    
    for country in countries:
        # Should not raise exceptions
        wage_tax = calc_wage_tax(income, country)
        div_tax = calc_div_tax(10000, income - 10000, country)
        optimal = find_optimal_split(income, country)
        
        assert wage_tax >= 0, f'{country}: wage tax should be non-negative'
        assert div_tax >= 0, f'{country}: dividend tax should be non-negative'
        assert len(optimal) == 3, f'{country}: should return wage, div, tax tuple'
        
    # Wales and NI should match England
    eng_tax = calc_wage_tax(income, 'eng')
    wal_tax = calc_wage_tax(income, 'wal')
    ni_tax = calc_wage_tax(income, 'ni')
    
    assert eng_tax == wal_tax == ni_tax, (
        f'England, Wales, NI should have same tax. '
        f'Eng: £{eng_tax:.2f}, Wal: £{wal_tax:.2f}, NI: £{ni_tax:.2f}'
    )


def test_edge_cases():
    """Test edge cases like zero income and exact boundaries"""
    
    # Zero income
    zero_wage_tax = calc_wage_tax(0, 'eng')
    zero_div_tax = calc_div_tax(0, 0, 'eng')
    assert zero_wage_tax == 0, 'Zero income should have zero wage tax'
    assert zero_div_tax == 0, 'Zero dividends should have zero dividend tax'
    
    # Very low income (below personal allowance)
    low_income = 5000
    low_wage_tax = calc_wage_tax(low_income, 'eng')
    assert low_wage_tax == 0, 'Income below PA should have zero tax'
    
    # Income exactly at personal allowance
    pa_income = 12570
    pa_wage_tax = calc_wage_tax(pa_income, 'eng')
    assert pa_wage_tax == 0, 'Income exactly at PA should have zero tax'
    
    # Income just above personal allowance
    above_pa = 12571
    above_pa_tax = calc_wage_tax(above_pa, 'eng')
    assert above_pa_tax == 0.20, f'£1 above PA should be 20p tax, got £{above_pa_tax:.2f}'


def test_critical_points_function():
    """Test the get_critical_wage_points function directly"""
    income = 100000
    country = 'eng'
    
    critical_points = get_critical_wage_points(income, country)
    
    # Should include 0 and income
    assert 0 in critical_points, 'Should include 0'
    assert income in critical_points, 'Should include total income'
    
    # Should include personal allowance
    pa, _ = get_tax_bands(country, income)
    assert pa in critical_points, f'Should include personal allowance £{pa}'
    
    # Should be sorted
    assert critical_points == sorted(critical_points), 'Should be sorted'
    
    # Should have reasonable number of points (not too many, not too few)
    assert 3 <= len(critical_points) <= 10, (
        f'Expected 3-10 critical points, got {len(critical_points)}'
    )


def test_optimization_correctness():
    """Verify that optimization actually finds the minimum tax point"""
    income = 60000
    country = 'eng'
    
    optimal_wage, optimal_div, min_tax = find_optimal_split(income, country)
    
    # Test that this is actually better than some obvious alternatives
    alternatives = [
        (0, income),  # All dividends
        (income, 0),  # All wages
        (income // 2, income // 2),  # 50/50 split
        (12570, income - 12570),  # Wage up to personal allowance
    ]
    
    for alt_wage, alt_div in alternatives:
        alt_wage_tax = calc_wage_tax(alt_wage, country)
        alt_div_tax = calc_div_tax(alt_div, alt_wage, country)
        alt_total = alt_wage_tax + alt_div_tax
        
        assert min_tax <= alt_total, (
            f'Optimal split (£{min_tax:.2f}) should be ≤ alternative '
            f'£{alt_wage}/{alt_div} (£{alt_total:.2f})'
        )
    
    # Verify the optimal split adds up to total income
    assert abs(optimal_wage + optimal_div - income) < 0.01, (
        f'Optimal split should add to income: '
        f'£{optimal_wage:.2f} + £{optimal_div:.2f} = £{optimal_wage + optimal_div:.2f}'
    )


def test_high_income_scenarios():
    """Test very high income scenarios"""
    
    # Test income where personal allowance is fully tapered away
    high_income = 200000
    high_wage_tax = calc_wage_tax(high_income, 'eng')
    
    # Should be substantial tax for £200k income
    assert high_wage_tax > 50000, (
        f'£200k income should have substantial tax, got £{high_wage_tax:.2f}'
    )
    
    # Test optimization for high earners
    optimal_wage, optimal_div, min_tax = find_optimal_split(high_income, 'eng')
    
    # Should find a reasonable split
    assert 0 <= optimal_wage <= high_income
    assert 0 <= optimal_div <= high_income
    assert min_tax > 0


def test_dividend_vs_wage_tax_rates():
    """Test that dividend and wage tax rates behave as expected"""
    
    # For basic rate taxpayers, dividends should often be more tax-efficient
    income = 40000
    
    # All wages
    all_wage_tax = calc_wage_tax(income, 'eng')
    all_wage_div_tax = calc_div_tax(0, income, 'eng')
    all_wage_total = all_wage_tax + all_wage_div_tax
    
    # All dividends
    all_div_wage_tax = calc_wage_tax(0, 'eng')
    all_div_div_tax = calc_div_tax(income, 0, 'eng')
    all_div_total = all_div_wage_tax + all_div_div_tax
    
    # For this income level, all dividends should be more efficient
    assert all_div_total < all_wage_total, (
        f'All dividends (£{all_div_total:.2f}) should be more efficient than '
        f'all wages (£{all_wage_total:.2f}) for £{income} income'
    )


def test_tax_band_boundaries():
    """Test behavior exactly at tax band boundaries"""
    
    # Test at basic rate band boundary for England (£50,270 total income)
    boundary_income = 50270
    
    # Split right at the boundary
    wage = 25000
    dividend = boundary_income - wage
    
    div_tax = calc_div_tax(dividend, wage, 'eng')
    
    # Should handle boundary correctly without errors
    assert div_tax >= 0, 'Tax at boundary should be non-negative'
    
    # Test optimization doesn't break at boundaries
    optimal = find_optimal_split(boundary_income, 'eng')
    assert len(optimal) == 3, 'Should return valid optimization result'