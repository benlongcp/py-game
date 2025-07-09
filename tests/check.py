#!/usr/bin/env python3
"""
Quick organization check - run this anytime to verify project organization.
"""

import sys
import os

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Run the organization checker
os.system("python tests/check_organization.py")
