#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting RooFlow config setup (with ConPort strategy update) ---"

# Check for Git command
if ! command -v git &> /dev/null; then
    echo "Error: git is not found in your PATH."
    echo "Please install Git using your distribution's package manager (e.g., sudo apt install git, sudo yum install git)."
    exit 1
else
    echo "Found git executable."
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not found in your PATH."
    echo "Please install Python 3 (https://www.python.org/downloads/)."
    exit 1
else
    echo "Found python3 executable."
fi

# Check for PyYAML library
if ! python3 -c "import yaml" &> /dev/null; then
    echo "Error: PyYAML library is not found for Python 3."
    echo "Please install it using: pip install pyyaml"
    exit 1
else
    echo "Found PyYAML library."
fi

# Define a temporary directory name for clarity
CLONE_DIR="RooFlow_temp_$$" # Using $$ for process ID to add uniqueness

# Clone the repository (shallow clone for efficiency)
echo "Cloning RooFlow repository into $CLONE_DIR..."
git clone --depth 1 https://github.com/GreatScottyMac/RooFlow "$CLONE_DIR"

# --- MODIFIED COPY SECTION START ---
echo "Copying specific configuration items..."

# 1. Copy .roo directory (recursively)
echo "Copying .roo directory..."
cp -r "$CLONE_DIR/config/.roo" ./

# 2. Copy specific config files
echo "Copying .roomodes, Python script, and ConPort strategy..."
cp "$CLONE_DIR/config/.roomodes" ./
cp "$CLONE_DIR/config/generate_mcp_yaml.py" ./
cp "$CLONE_DIR/config/roo_code_conport_strategy" ./ # Added copy for ConPort strategy

# --- MODIFIED COPY SECTION END ---

# Check if essential files exist before running Python script
if [ ! -d ".roo" ]; then
    echo "Error: .roo directory not found after specific copy. Setup failed."
    rm -rf "$CLONE_DIR" # Clean up clone dir before exiting
    exit 1
fi
if [ ! -f "generate_mcp_yaml.py" ]; then
     echo "Error: generate_mcp_yaml.py not found after specific copy. Setup failed."
     rm -rf "$CLONE_DIR" # Clean up clone dir before exiting
     exit 1
fi
if [ ! -f "roo_code_conport_strategy" ]; then # Check for strategy file
     echo "Error: roo_code_conport_strategy not found after specific copy. Setup failed."
     rm -rf "$CLONE_DIR" # Clean up clone dir before exiting
     exit 1
fi

# Run the Python script to process templates
echo "Running Python script to process templates..."
if [[ "$(uname)" == "Darwin" ]]; then OS_VAL="macOS $(sw_vers -productVersion)"; else OS_VAL=$(uname -s -r); fi
SHELL_VAL="bash"
HOME_VAL=$(echo "$HOME")
WORKSPACE_VAL=$(pwd)

python3 generate_mcp_yaml.py --os "$OS_VAL" --shell "$SHELL_VAL" --home "$HOME_VAL" --workspace "$WORKSPACE_VAL"

# --- EMBEDDED PROMPT UPDATE LOGIC ---
echo "--- Starting Roo prompt update with ConPort strategy ---"

# Define paths for update logic (relative to current dir, which is workspace root)
UPD_ROO_DIR=".roo"
UPD_STRATEGY_FILE="roo_code_conport_strategy" # This was copied to CWD

# Target prompt files for update logic (relative to UPD_ROO_DIR)
UPD_ARCHITECT_PROMPT="system-prompt-flow-architect"
UPD_ASK_PROMPT="system-prompt-flow-ask"
UPD_CODE_PROMPT="system-prompt-flow-code"
UPD_DEBUG_PROMPT="system-prompt-flow-debug"
UPD_ORCHESTRATOR_PROMPT="system-prompt-flow-orchestrator"

# Error check for update logic's required files
if [ ! -d "$UPD_ROO_DIR" ]; then
  echo "Error (Update Logic): Directory '$UPD_ROO_DIR' not found."
  # Main script already checks for .roo, but good to be defensive if this part is ever isolated
  rm -rf "$CLONE_DIR"
  exit 1
fi

if [ ! -f "$UPD_STRATEGY_FILE" ]; then
  echo "Error (Update Logic): Strategy file '$UPD_STRATEGY_FILE' not found in current path."
  rm -rf "$CLONE_DIR"
  exit 1
fi

# Function to process files that need replacement (from update_roo_prompts.sh)
process_replacement() {
  local target_file_path="$1"
  local temp_file=$(mktemp)

  if [ ! -f "$target_file_path" ]; then
    echo "Warning (Update Logic): Target file '$target_file_path' not found. Skipping."
    rm "$temp_file" # Clean up temp file if target doesn't exist
    return
  fi

  echo "Processing (Update Logic) $target_file_path for replacement..."
  line_num=$(grep -n "^memory_bank_strategy:" "$target_file_path" | cut -d: -f1)

  if [ -z "$line_num" ]; then
    echo "Warning (Update Logic): 'memory_bank_strategy:' not found in '$target_file_path'. Skipping replacement."
    rm "$temp_file"
    return
  fi

  head -n $((line_num - 1)) "$target_file_path" > "$temp_file"
  cat "$UPD_STRATEGY_FILE" >> "$temp_file"
  mv "$temp_file" "$target_file_path"
  echo "Updated (Update Logic) '$target_file_path'."
}

# Function to process the file that needs deletion (from update_roo_prompts.sh)
process_deletion() {
  local target_file_path="$1"
  local temp_file=$(mktemp)

  if [ ! -f "$target_file_path" ]; then
    echo "Warning (Update Logic): Target file '$target_file_path' not found. Skipping."
    rm "$temp_file" # Clean up temp file
    return
  fi

  echo "Processing (Update Logic) $target_file_path for deletion..."
  line_num=$(grep -n "^memory_bank_strategy:" "$target_file_path" | cut -d: -f1)

  if [ -z "$line_num" ]; then
    echo "Warning (Update Logic): 'memory_bank_strategy:' not found in '$target_file_path'. Skipping deletion."
    rm "$temp_file"
    return
  fi

  head -n $((line_num - 1)) "$target_file_path" > "$temp_file"
  mv "$temp_file" "$target_file_path"
  echo "Updated (Update Logic) '$target_file_path' (section deleted)."
}

# Main processing for prompt updates
process_replacement "$UPD_ROO_DIR/$UPD_ARCHITECT_PROMPT"
process_replacement "$UPD_ROO_DIR/$UPD_CODE_PROMPT"
process_replacement "$UPD_ROO_DIR/$UPD_DEBUG_PROMPT"
process_deletion "$UPD_ROO_DIR/$UPD_ASK_PROMPT"
process_replacement "$UPD_ROO_DIR/$UPD_ORCHESTRATOR_PROMPT"

echo "--- Roo prompt update with ConPort strategy completed ---"
# --- END EMBEDDED PROMPT UPDATE LOGIC ---

# Clean up the strategy file from the workspace root
if [ -f "$UPD_STRATEGY_FILE" ]; then
  echo "Cleaning up $UPD_STRATEGY_FILE from workspace root..."
  rm -f "$UPD_STRATEGY_FILE"
fi

# --- MEMORY BANK INITIALIZATION ---
echo "--- Initializing Memory Bank ---"

if [ ! -d "memory-bank" ]; then
    if [ -d "memory-bank-template" ]; then
        echo "Copying memory-bank-template to memory-bank..."
        cp -r memory-bank-template memory-bank
        
        # Remove .template extensions from files
        echo "Converting template files..."
        for template_file in memory-bank/*.template; do
            if [ -f "$template_file" ]; then
                base_name="${template_file%.template}"
                mv "$template_file" "$base_name"
                echo "  - Converted $(basename $template_file) to $(basename $base_name)"
            fi
        done
        
        echo "Memory Bank initialized successfully!"
    else
        echo "Warning: memory-bank-template directory not found. Skipping Memory Bank initialization."
    fi
else
    echo "Memory Bank already exists. Skipping initialization."
fi

# --- PROJECT CONFIGURATION ---
echo "--- Checking project configuration ---"

if [ ! -f "pyproject.toml" ]; then
    if [ -f "pyproject.toml.example" ]; then
        echo ""
        read -p "Create pyproject.toml from example? (y/n): " create_pyproject
        if [ "$create_pyproject" = "y" ] || [ "$create_pyproject" = "Y" ]; then
            cp pyproject.toml.example pyproject.toml
            echo "Created pyproject.toml from example."
            echo "Remember to customize project name, dependencies, and metadata!"
        fi
    fi
fi

# --- INFRASTRUCTURE SETUP ---
if [ -d "infrastructure" ]; then
    echo ""
    read -p "Start development infrastructure (Docker)? (y/n): " start_infra
    if [ "$start_infra" = "y" ] || [ "$start_infra" = "Y" ]; then
        if [ -f "scripts/dev/start-infra.sh" ]; then
            echo "Starting infrastructure..."
            bash scripts/dev/start-infra.sh
        else
            echo "Warning: scripts/dev/start-infra.sh not found. Manually start with:"
            echo "  cd infrastructure && docker compose up -d"
        fi
    fi
fi

# --- MODIFIED CLEANUP SECTION START ---
echo "Cleaning up temporary clone directory ($CLONE_DIR)..."
rm -rf "$CLONE_DIR" # Remove the cloned repo directory
# --- MODIFIED CLEANUP SECTION END ---

echo ""
echo "======================================================================"
echo "  RooFlow config setup (with ConPort strategy) complete!"
echo "======================================================================"
echo ""
echo "Next steps:"
echo "  1. Review memory-bank/*.md files and customize for your project"
echo "  2. If you created pyproject.toml, customize it for your project"
echo "  3. Check .vscode/settings.json for editor configuration"
echo "  4. Review infrastructure/ for observability stack setup"
echo "  5. Read TEMPLATE_USAGE.md for complete template documentation"
echo ""
echo "Happy coding with RooFlow! 🚀"
echo ""
exit 0