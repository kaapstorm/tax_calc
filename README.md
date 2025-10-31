# tax_calc

## optimise_tax

This script calculates the optimum split between wages and dividends for
a given total income.

## Usage

<details open>
<summary><b>Windows</b></summary>

If you have the standalone executable (`optimise_tax.exe`):

```shell
> optimise_tax.exe 40000

> optimise_tax.exe 40000 --country sco --graph
```

**Positional arguments:**
- `income` - Total income (GBP)

**Options:**
- `-h, --help` - Show help message and exit
- `--country {eng,sco,wal,ni}` - Country code (default: eng)
- `--graph` - Render and save a graph in PNG showing the intersection of tax on wages and dividends

**To obtain the Windows executable:**

1. Open https://github.com/kaapstorm/tax_calc/ in your browser.
2. Navigate to the "Actions" tab.
3. Open the latest workflow run.
4. Download the `optimise-tax-windows-exe` artifact.
5. Unzip `optimise-tax-windows-exe.zip` and extract `optimise_tax.exe`.

No Python installation required.

</details>

<details>
<summary><b>Linux/Mac</b></summary>

```shell
$ ./optimise_tax.py [-h] [--country {eng,sco,wal,ni}] [--graph] income
```

**Examples:**

```shell
# Calculate optimal split for £40,000 income in England
$ ./optimise_tax.py 40000

# Calculate for Scotland and generate a graph
$ ./optimise_tax.py 40000 --country sco --graph

# Using uv
$ uv run optimise_tax.py 40000 --graph
```

</details>

## Building a Windows Executable Locally

1. Install development dependencies:
   ```shell
   uv sync --dev
   ```

2. Build the executable:
   ```shell
   uv run pyinstaller --onefile --name optimise_tax --console optimise_tax.py
   ```

   Or use the build script:
   ```shell
   uv run build_exe.py
   ```

3. The executable will be created in `dist/optimise_tax.exe`
