#!/bin/bash
# setup_display.sh - Fix X11 display authorization for MurfAI automation features

echo "🔧 Setting up X11 Display for MurfAI Automation Features"
echo "=================================================="

# Check if DISPLAY is set
if [ -z "$DISPLAY" ]; then
    echo "⚠️  DISPLAY environment variable not set"
    echo "Setting DISPLAY=:0"
    export DISPLAY=:0
else
    echo "✅ DISPLAY is set to: $DISPLAY"
fi

# Check if we can connect to X server
if xhost &>/dev/null; then
    echo "✅ X server is running"
    
    # Add local user to X access control list
    echo "🔐 Adding local user to X access control..."
    xhost +local: 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ X access control updated successfully"
        echo "🚀 You can now run MurfAI with full automation features!"
        echo ""
        echo "Run: uv run conversational_murf_ai.py"
        echo ""
        echo "Available automation commands:"
        echo "• 'Chrome kholo' - Opens Chrome browser"
        echo "• 'Gmail kholo' - Opens Gmail"
        echo "• 'Screenshot lo' - Takes screenshot"
        echo "• 'Type hello world' - Types text"
    else
        echo "⚠️  Could not update X access control"
        echo "💡 Try running: sudo xhost +local:"
    fi
else
    echo "❌ X server not running or not accessible"
    echo "💡 Solutions:"
    echo "   1. Make sure you're running in a graphical session"
    echo "   2. Try: export DISPLAY=:0"
    echo "   3. For SSH: ssh -X username@hostname"
    echo "   4. The app will still work without automation features"
fi

echo ""
echo "🎤 MurfAI will work in all cases - automation is optional!"
echo "   • Voice synthesis ✅"
echo "   • AI conversations ✅" 
echo "   • Web browser actions ✅"
echo "   • System automation (if display works) ✅/⚠️"
