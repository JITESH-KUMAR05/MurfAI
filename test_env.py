#!/usr/bin/env python3
"""
Quick test to verify the environment is working
"""

import sys
import os

print("🧪 Testing MurfAI Environment...")
print(f"🐍 Python: {sys.version}")
print(f"📁 Working directory: {os.getcwd()}")

# Test imports
try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
except ImportError as e:
    print(f"❌ python-dotenv import failed: {e}")

try:
    import httpx
    print("✅ httpx imported successfully")
except ImportError as e:
    print(f"❌ httpx import failed: {e}")

try:
    import requests
    print("✅ requests imported successfully")
except ImportError as e:
    print(f"❌ requests import failed: {e}")

try:
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 imported successfully")
except ImportError as e:
    print(f"❌ PyQt6 import failed: {e}")

# Test environment file
env_file = ".env"
if os.path.exists(env_file):
    print("✅ .env file exists")
else:
    print("⚠️  .env file not found")

print("\n🚀 Environment test completed!")
print("🎯 Ready to run MurfAI Assistant!")
