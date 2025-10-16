#!/bin/bash

# Navigate to the correct folder (update path if needed)
cd "$(dirname "$0")"

# Activate conda or virtual environment if needed here (optional)

# Run the Streamlit app
python3 -m streamlit run api_integrated_app/api_integrated_app.py
