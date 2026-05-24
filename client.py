"""
Start the Habitron Streamlit frontend client.

Usage: streamlit run run_client.py

This is the entry point for the frontend Streamlit application.
Make sure the backend API is running on http://localhost:5000
before starting the client.
"""

import sys
import os

# Ensure the project root is in the path
sys.path.insert(0, os.path.dirname(__file__))

from src.ui.app import main


if __name__ == '__main__':
    main()
