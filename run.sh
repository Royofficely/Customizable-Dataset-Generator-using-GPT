#!/bin/bash

# Set strict mode
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color="$1"
    local message="$2"
    echo -e "${color}${message}${NC}"
}

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_color "$RED" "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if required files exist
required_files=("main.py" "config.yaml" "prompts.yaml")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        print_color "$RED" "Error: Required file $file not found."
        exit 1
    fi
done

# Activate the virtual environment if not already activated
if [[ "$VIRTUAL_ENV" != *"/venv" ]]; then
    print_color "$GREEN" "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the main Python script
print_color "$GREEN" "Running main.py..."
if python main.py config.yaml prompts.yaml; then
    print_color "$GREEN" "Script executed successfully."
else
    print_color "$RED" "Error: Script execution failed."
    exit 1
fi

print_color "$GREEN" "Done."
# Note: We're not deactivating the virtual environment here to keep the user in the correct environment
