# Installation Guide

## Quick Install (Recommended)

### Step 1: Create a Virtual Environment (Recommended)

```bash
cd mmWave-python

# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 2: Install the Package

```bash
# Install in editable/development mode
pip install -e .

# Or install normally
pip install .
```

### Step 3: Verify Installation

```bash
python -c "from seeed_mr60bha2 import SEEED_MR60BHA2; print('✓ Installation successful!')"
```

### Step 4: Test with Port Detector

```bash
python examples/port_detector.py --list
```

## Alternative: System-Wide Installation

If you prefer to install system-wide (not recommended):

```bash
# macOS/Linux
pip3 install -e .

# Or with sudo (if needed)
sudo pip3 install -e .
```

## Verify Your Setup

After installation, you should be able to:

1. Import the library:
   ```python
   from seeed_mr60bha2 import SEEED_MR60BHA2
   ```

2. Run examples:
   ```bash
   python examples/port_detector.py --list
   python examples/basic_usage.py
   ```

## Troubleshooting

### "ModuleNotFoundError: No module named 'seeed_mr60bha2'"

**Cause**: The package is not installed in the current Python environment.

**Solution 1** - Using venv (recommended):
```bash
# Make sure venv is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Then install
pip install -e .
```

**Solution 2** - Check your Python:
```bash
# Check which Python you're using
which python
python --version

# Make sure you install to the same Python
pip install -e .
```

**Solution 3** - Use python -m pip:
```bash
# This ensures you're installing to the correct Python
python -m pip install -e .
```

### "Permission denied" when installing

**On macOS/Linux**:
```bash
# Option 1: Use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Option 2: User installation
pip install --user -e .
```

### Package installed but import still fails

**Check your PYTHONPATH**:
```bash
python -c "import sys; print('\n'.join(sys.path))"
```

**Reinstall in current environment**:
```bash
pip uninstall seeed-mr60bha2
pip install -e .
```

## Development Installation

For development work with all tools:

```bash
# Create and activate venv
python3 -m venv venv
source venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Or manually install dev tools
pip install pytest pytest-cov black flake8 mypy
```

## Running Examples

Once installed, you can run examples from anywhere:

```bash
# Make sure venv is activated!
source venv/bin/activate

# Run examples
python examples/basic_usage.py
python examples/port_detector.py
python examples/real_time_display.py
```

## Checking Installation

```bash
# Check if package is installed
pip list | grep seeed

# Should show:
# seeed-mr60bha2    1.0.0    /Users/your-path/mmWave-python

# Check import
python -c "from seeed_mr60bha2 import SEEED_MR60BHA2; print('OK')"
```

## Uninstallation

```bash
pip uninstall seeed-mr60bha2
```

## Common Workflows

### Daily Development

```bash
# Activate venv
source venv/bin/activate

# Your code here
python my_script.py

# Deactivate when done
deactivate
```

### Running Examples

```bash
cd mmWave-python
source venv/bin/activate
python examples/basic_usage.py
```

### Making Changes

Since you installed with `-e` (editable mode), any changes to the source code are immediately reflected - no need to reinstall!

```bash
# Edit files
nano seeed_mr60bha2/mr60bha2.py

# Changes are live immediately
python test_script.py
```
