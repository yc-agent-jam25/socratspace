#!/bin/bash

# Simple test runner for VC Council
cd "/Users/michaelabouzeid/Desktop/Agent Jam"
source backend/venv/bin/activate
export PYTHONPATH="/Users/michaelabouzeid/Desktop/Agent Jam"
python test_end_to_end.py
