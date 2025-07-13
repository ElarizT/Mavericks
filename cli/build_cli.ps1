# build_cli.ps1

$python = "python"
$venvPath = ".\.venv"
$venvPython = "$venvPath\Scripts\python.exe"
$scriptToCompile = "cli.py"

# Check if python3.12 is available
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    Write-Error "python3.12 not found. Please install it and make sure it's in your PATH."
    exit 1
}

# Install uv if not already installed
& $python -m pip install uv

# Create the virtual environment using uv
& $python -m uv venv

# Sync dependencies from pyproject.toml
& $python -m uv sync

# Compile with Nuitka
if (-not (Test-Path $venvPython)) {
    Write-Error "Virtual environment Python executable not found."
    exit 1
}

& $venvPython -m nuitka --output-filename=genai.exe --no-pyi-file --standalone $scriptToCompile
