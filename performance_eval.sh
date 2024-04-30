#!/bin/bash

# Install psrecord if not already installed
if ! command -v psrecord &> /dev/null; then
    echo "Installing psrecord..."
    pip install psrecord
fi

# Find the process ID of the running streamlit application
streamlit_pid=$(ps -A | grep "streamlit run" | grep -v "grep" | awk '{print $1}')

if [[ -z $streamlit_pid ]]; then
    echo "No running streamlit application found."
    exit 1
fi

# Record the process using psrecord
echo "Recording process $streamlit_pid..."
psrecord $streamlit_pid --plot plot.png

echo "Process recorded successfully."
