tax_calc
========

optimise_tax
------------

This script calculates the optimum split between wages and dividends for
a given total income.

Install
-------

<details open>
<summary><b>Windows</b></summary>

Download the Windows executable, `optimise_tax.exe`:

1. Open https://github.com/kaapstorm/tax_calc in your browser.
2. Navigate to the "Actions" tab.
3. Open the latest workflow run. If no workflow runs are listed, select
   "Build Windows Executable" and click "Run workflow".
4. Download the `optimise-tax-windows-exe` artifact.
5. Unzip `optimise-tax-windows-exe.zip` and extract `optimise_tax.exe`.

</details>

<details>
<summary><b>Linux/Mac</b></summary>

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/).

2. Clone this repository:
   ```shell
   $ git clone https://github.com/kaapstorm/tax_calc.git
   $ cd tax_calc/
   ```

3. Install dependencies:
   ```shell
   $ uv sync
   ```

</details>


Usage
-----

<details open>
<summary><b>Windows</b></summary>

Run `optimise_tax.exe` from the command line. e.g.

```shell
> optimise_tax.exe 40000

> optimise_tax.exe 40000 --country sco --graph
```

Positional arguments:
- `income` - Total income (GBP)

Options:
- `-h, --help` - Show help message and exit

- `--country {eng,sco,wal,ni}` - Country code (default: eng)

- `--graph` - Render and save a graph in PNG showing the intersection
  of tax on wages and dividends

</details>

<details>
<summary><b>Linux/Mac</b></summary>

```shell
$ ./optimise_tax.py [-h] [--country {eng,sco,wal,ni}] [--graph] income
```

**Examples:**

```shell
# Calculate optimal split for £40,000 income in England
$ uv run optimise_tax.py 40000

# Calculate for Scotland and generate a graph
$ uv run optimise_tax.py 40000 --country sco --graph

# Activating the virtual environment
$ source .venv/bin/activate
$ ./optimise_tax.py 40000 --graph
```

</details>


How to build a Windows executable locally
-----------------------------------------

1. In Windows, follow the installation instructions for Linux/Mac
   above.

2. Install development dependencies:
   ```shell
   > uv sync --dev
   ```

3. Build the executable:
   ```shell
   > uv run pyinstaller --onefile --name optimise_tax --console optimise_tax.py
   ```

4. The executable will be created in `dist/optimise_tax.exe`
