#!/bin/bash

set -e

if ! command -v uv &> /dev/null; then
  echo "uv not found. Installing..."
  curl -sSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.cargo/bin:$PATH"
else
  echo "uv is already installed. Skipping installation"
fi

VENV_DIR=".venv"
BIN_NAME="genai"

if ! command -v uv &> /dev/null; then
    echo "Error: Failed to install uv."
    echo "Please install uv manually before proceeding. See: https://github.com/astral-sh/uv"
    exit 1
fi

# Check if the directory does NOT exist using the -d test operator
# The ! negates the test, so the 'if' block runs if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
  if uv venv "$VENV_DIR"; then
    echo "$VENV_DIR created successfully."
    uv sync
    $VENV_DIR/bin/pyinstaller --add-data "src/jinja/templates:src/jinja/templates" --onefile --name "$BIN_NAME" cli.py
  else
    # Handle potential errors during uv venv execution
    echo "Error: Failed to create $VENV_DIR using uv."
    exit 1
  fi
else
  echo "$VENV_DIR already exists. Skipping creation."
  uv sync
  $VENV_DIR/bin/pyinstaller --add-data "src/jinja/templates:src/jinja/templates" --onefile --name "$BIN_NAME" cli.py
fi

 sudo cp dist/$BIN_NAME /usr/local/bin
 sudo chmod +x /usr/local/bin/genai

# Exit successfully
exit 0