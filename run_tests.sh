#!/bin/bash


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ -d "venv" ]; then
    source venv/bin/activate
    PYTHON_CMD="python"
else
    # Try to find python or python3
    if command -v python &> /dev/null; then
        PYTHON_CMD="python"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        echo "Neither python nor python3 found. Please install Python."
        read -p "Press enter to exit"
        exit 1
    fi
fi


# Ensure pytest is installed
if ! $PYTHON_CMD -m pytest --version &> /dev/null; then
    echo "pytest not found. Installing..."
    $PYTHON_CMD -m pip install --user pytest
fi

# Run pytest
$PYTHON_CMD -m pytest
RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "All tests passed!"
else
    echo "Some tests failed. See output above."
fi
