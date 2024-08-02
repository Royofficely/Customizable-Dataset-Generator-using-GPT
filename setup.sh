#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status

# Function to print in green
print_green() {
    echo -e "\033[0;32m$1\033[0m"
}

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
    print_green "Using $PYTHON_CMD"
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

# Set execute permissions for run.sh
run_script_path="$(pwd)/run.sh"
if [ ! -x "$run_script_path" ]; then
    echo "Setting execute permissions for run.sh..."
    chmod +x "$run_script_path"
fi

# Function to create alias and source config
create_alias_and_source() {
    local shell_config="$1"
    local alias_line="alias run='$(pwd)/run.sh'"
    
    if grep -Fxq "$alias_line" "$shell_config"; then
        echo "Alias already exists in $shell_config"
    else
        echo "$alias_line" >> "$shell_config"
        echo "Alias added to $shell_config"
    fi
    
    # Export OPENAI_API_KEY in the shell config
    local export_line="export OPENAI_API_KEY=\"$api_key\""
    if grep -Fxq "$export_line" "$shell_config"; then
        echo "OPENAI_API_KEY export already exists in $shell_config"
    else
        echo "$export_line" >> "$shell_config"
        echo "OPENAI_API_KEY export added to $shell_config"
    fi
    
    # Source the shell config file
    if [ -f "$shell_config" ]; then
        echo "Attempting to source $shell_config..."
        if (source "$shell_config") 2>/dev/null; then
            print_green "Successfully sourced $shell_config"
        else
            echo "Warning: Encountered an error while sourcing $shell_config"
            echo "You may need to manually fix any syntax errors in your $shell_config file"
            echo "After fixing, please run: source $shell_config"
        fi
        
        # Verify if the alias is now available
        if type run > /dev/null 2>&1; then
            print_green "Alias 'run' is now active and ready to use."
        else
            echo "Alias 'run' was added but is not active. You may need to restart your terminal or manually run: source $shell_config"
        fi
    else
        echo "Could not find $shell_config to source."
    fi
}

# Determine shell and create alias
if [[ "$SHELL" == */zsh ]]; then
    create_alias_and_source "$HOME/.zshrc"
    print_green "Added OPENAI_API_KEY and 'run' alias to ~/.zshrc"
elif [[ "$SHELL" == */bash ]]; then
    create_alias_and_source "$HOME/.bashrc"
    print_green "Added OPENAI_API_KEY and 'run' alias to ~/.bashrc"
else
    echo "Could not determine shell type. Please manually add the following lines to your shell configuration file:"
    echo "export OPENAI_API_KEY=\"$api_key\""
    echo "alias run='$(pwd)/run.sh'"
fi

print_green "Setup complete. The sanitized API key has been exported for the current session."
echo "An alias 'run' has been created for easy execution of the script."
echo "These changes have been applied to your current session."
echo "If you encounter any issues, you may need to restart your terminal or manually run:"
echo "source ~/.$(basename "$SHELL")rc"

# Check if both config files exist
if [ ! -f "config.yaml" ] || [ ! -f "prompts.yaml" ]; then
    echo "Warning: config.yaml or prompts.yaml not found in the current directory."
    echo "Please ensure both files exist before running the main script."
fi

print_green "\nYou can now run the main script from any directory by simply typing:"
echo "run"
