# Documentation for AI Agents

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a UK tax optimization calculator that determines the optimal split between wages and dividends for a given total income. The calculator handles different UK regions (England, Wales, Northern Ireland, and Scotland) with their distinct tax bands and rates.

## Key Commands

### Development Setup
```bash
# Install dependencies
uv sync

# Install development dependencies (includes PyInstaller and Ruff)
uv sync --dev
```

### Running the Application
```bash
# Run directly with uv
uv run optimise_tax.py 40000

# With options
uv run optimise_tax.py 40000 --country sco --graph

# After activating virtual environment
source .venv/bin/activate
./optimise_tax.py 40000 --graph
```

### Code Quality
```bash
# Format and lint code
uv run ruff format
uv run ruff check
# Run tests
uv run pytest
```

## Architecture

### Core Components

- **Tax Calculation Engine** (`optimise_tax.py`): Single-file application containing all tax calculation logic
- **Tax Band Definitions**: Functions `get_tax_bands()` and `get_dividend_bands()` define region-specific tax structures
- **Optimization Algorithm**: `total_tax_split()` uses critical point analysis to find optimal wage/dividend splits
- **Visualization**: Optional graph generation using matplotlib

### Tax Calculation Logic

The system implements UK tax rules for 2025/26:

1. **Personal Allowance**: £12,570 (tapers above £100,000)
2. **Wage Tax**: Different bands for Scotland vs England/Wales/NI
3. **Dividend Tax**: 8.75%/33.75%/39.35% rates with £500 allowance
4. **Optimization**: Evaluates critical points (band boundaries) to find minimum total tax

### Key Functions

- `calc_wage_tax(wage, country)`: Calculates income tax on wages
- `calc_div_tax(div, wage, country)`: Calculates tax on dividends considering total income
- `total_tax_split(amount, country)`: Finds optimal split using critical point method
- `generate_graph()`: Creates visualization of tax across different splits

## Code Style

- Uses Ruff for formatting and linting
- Uses pytest functional-style for testing
- Line length: 79 characters
- Quote style: single quotes
- Requires Python >=3.13
