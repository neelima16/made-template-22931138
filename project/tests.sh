#!/bin/bash

# Ensure pipeline script is executable (if not already)
chmod +x pipeline.py

# Run the data pipeline
python3 pipeline.py

# Check if the output files exist
if [[ -f "data/database1.db" && -f "data/database2.db" ]]; then
    echo "Test Passed: Output files exist."
    exit 0
else
    echo "Test Failed: Output files do not exist."
    exit 1
fi
