#!/usr/bin/env python3
"""
MurfAI Conversational Assistant Launcher
Simple launcher script with error handling and setup validation
"""

import sys
import os
import subprocess
from pathlib import Path

def check_requirements():
    """Check if requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required. Current version:", sys.version)
        return False
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found!")
        print("💡 Copy .env.example to .env and add your API keys")
        if Path(".env.example").exists():
            print("📋 You can run: cp .env.example .env")
        return True  # Continue anyway for demo mode
    
    # Check if uv is available
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        print("✅ uv package manager found")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ uv package manager not found!")
        print("💡 Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    
    print("✅ All requirements met!")
    return True

def main():
    """Main launcher function"""
    print("🎤 MurfAI Conversational Assistant Launcher")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements not met. Please fix the issues above.")
        sys.exit(1)
    
    print("\n🚀 Starting MurfAI Conversational Assistant...")
    print("💬 Ready for voice conversations with AI!")
    print("\n📋 Features available:")
    print("  • Voice input/output")
    print("  • 15+ premium voices including Indian voices")
    print("  • Real-time AI conversations")
    print("  • Responsive UI with fullscreen support")
    print("  • Export conversations")
    print("\n⌨️  Keyboard shortcuts:")
    print("  • F11: Toggle fullscreen")
    print("  • Escape: Exit fullscreen")
    
    try:
        # Run the main application
        result = subprocess.run([
            "uv", "run", "python", "conversational_murf_ai.py"
        ], check=False)
        
        if result.returncode != 0:
            print(f"\n❌ Application exited with code {result.returncode}")
            print("💡 Check the logs for more details")
        else:
            print("\n✅ Application closed successfully")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        print("💡 Try running directly: uv run python conversational_murf_ai.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
