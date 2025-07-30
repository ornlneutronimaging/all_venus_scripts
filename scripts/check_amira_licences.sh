#!/bin/bash

# Function to check Amira license status
check_amira_license() {
    echo "Checking Amira license status..."
    echo "================================"
    
    # Check if license-status-amira command exists
    if ! command -v license-status-amira &> /dev/null; then
        echo "Error: license-status-amira command not found"
        return 1
    fi
    
    # Retrieve and display license status
    local output
    output=$(license-status-amira 2>&1)
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "License Status Output:"
        echo "$output"
    else
        echo "Error retrieving license status (exit code: $exit_code):"
        echo "$output"
    fi
    
    return $exit_code
}

# Function to parse and summarize license information
parse_license_info() {
    local license_output="$1"
    
    echo ""
    echo "License Summary:"
    echo "==============="
    
    # Extract available licenses (customize based on actual output format)
    echo "$license_output" | grep -i "available\|in use\|total" || echo "No license information found"
}

# Main execution
main() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "Amira License Check - $timestamp"
    echo ""
    
    # Get license status
    local license_output
    license_output=$(license-status-amira 2>&1)
    local status=$?
    
    if [ $status -eq 0 ]; then

        # only display the lines after "Users of AvizoSubMains" and before the next section
        echo "License status retrieved successfully."
        echo "$license_output" | sed -n '/Users of AvizoSubMains/,/Users of /p'
    else
        echo "Failed to retrieve Amira license status"
        echo "Output: $license_output"
        exit 1
    fi
}

# Run the main function
main "$@"
