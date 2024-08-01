#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

# Function to check Python version
check_python_version() {
    if command -v "$1" >/dev/null 2>&1; then
        if "$1" -c "import sys; exit(0 if sys.version_info >= (3,6) else 1)" >/dev/null 2>&1; then
            echo "$1"
            return 0
        fi
    fi
    return 1
}

# Check for Python 3.6+
if PYTHON_CMD=$(check_python_version python3) || PYTHON_CMD=$(check_python_version python); then
    echo "Using $PYTHON_CMD"
else
    echo "Python 3.6 or later is required but not found. Please install Python 3.6+ and try again."
    exit 1
fi

# Remove the old venv directory if it exists
echo "Removing old virtual environment..."
rm -rf venv

# Create a new virtual environment
echo "Creating new virtual environment..."
"$PYTHON_CMD" -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Verify installation of openai package
if ! python -c "import openai" 2>/dev/null; then
    echo "Error: openai package not installed correctly. Attempting to install directly..."
    pip install openai
fi

# Prompt user for OpenAI API key
echo "Please enter your OpenAI API key:"
read -rs api_key_input # -s flag hides the input

# Sanitize the API key: remove spaces and special characters
api_key=$(echo "$api_key_input" | tr -dc '[:alnum:]-_')

# Validate API key is not empty
if [ -z "$api_key" ]; then
    echo "Error: API key is empty after removing special characters. Please provide a valid API key."
    exit 1
fi

# Create .env file with sanitized API key
echo "OPENAI_API_KEY=$api_key" > .env

# Export the sanitized API key for the current session
export OPENAI_API_KEY="$api_key"

# Add export command to shell configuration file
if [[ "$SHELL" == */zsh ]]; then
    echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.zshrc
    echo "Added OPENAI_API_KEY to ~/.zshrc"
elif [[ "$SHELL" == */bash ]]; then
    echo "export OPENAI_API_KEY=\"$api_key\"" >> ~/.bashrc
    echo "Added OPENAI_API_KEY to ~/.bashrc"
else
    echo "Could not determine shell type. Please manually add the following line to your shell configuration file:"
    echo "export OPENAI_API_KEY=\"$api_key\""
fi

echo "Setup complete. The sanitized API key has been exported for the current session."
echo "To make it available in new terminal sessions, please run:"
echo "source ~/.bashrc (for Bash) or source ~/.zshrc (for Zsh)"

# Check if both config files exist
if [ ! -f "config.yaml" ] || [ ! -f "prompts.yaml" ]; then
    echo "Warning: config.yaml or prompts.yaml not found in the current directory."
    echo "Please ensure both files exist before running the main script."
fi

echo ""
echo "To run the main script, use the following command:"
echo "./venv/bin/python main.py config.yaml prompts.yaml"
echo ""
echo "Make sure both config.yaml and prompts.yaml are in the same directory as main.py before running the command."
