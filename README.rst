========
tax_calc
========

optimise_tax
------------

This script calculates the optimum split between wages and dividends for
a given total income.


Usage
-----

.. tab-set::

   .. tab-item:: Linux/Mac

      .. code-block:: shell

         $ ./optimise_tax.py [-h] [--country {eng,sco,wal,ni}] [--graph] income

      **Positional arguments:**

      :income: Total income (GBP)

      **Options:**

      :-h, --help: Show help message and exit
      :--country {eng,sco,wal,ni}: Country code (default: eng)
      :--graph: Render and save a graph in PNG showing the intersection of tax
                on wages and dividends

      **Examples:**

      .. code-block:: shell

         # Calculate optimal split for £60,000 income in England
         $ ./optimise_tax.py 60000

         # Calculate for Scotland and generate a graph
         $ ./optimise_tax.py 100000 --country sco --graph

         # Using uv
         $ uv run optimise_tax.py 75000 --graph


   .. tab-item:: Windows

      If you have the standalone executable (``optimise_tax.exe``):

      .. code-block:: shell

         > optimise_tax.exe 60000

         > optimise_tax.exe 100000 --country sco --graph

      **To obtain the Windows executable:**

      1. Download from GitHub Actions (see `Building via GitHub Actions`_)
      2. Or build it yourself locally (see `Building Locally`_)

      No Python installation required.


Building a Windows Executable
------------------------------

You can create a standalone Windows executable that doesn't require Python
to be installed.


Building Locally
~~~~~~~~~~~~~~~~

1. Install development dependencies:

   .. code-block:: shell

      uv sync --dev

2. Build the executable:

   .. code-block:: shell

      uv run pyinstaller --onefile --name optimise_tax --console optimise_tax.py

   Or use the build script:

   .. code-block:: shell

      uv run build_exe.py

3. The executable will be created in ``dist/optimise_tax.exe``


Building via GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The repository includes a GitHub Actions workflow that automatically builds
a Windows executable on every push to the master branch.

1. Push your changes to GitHub
2. Navigate to the Actions tab in your repository
3. Find the "Build Windows Executable" workflow
4. Download the ``optimise-tax-windows-exe`` artifact

You can also manually trigger the build:

1. Go to Actions > Build Windows Executable
2. Click "Run workflow"
3. Download the artifact once complete
