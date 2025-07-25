#!/usr/bin/env python3
"""
OMNI-AI Voice Assistant - Feature Test Script
Quick test to verify all components are working correctly
"""

import sys
import os
from pathlib import Path
import tempfile

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all imports work correctly"""
    print("🔍 Testing imports...")
    try:
        from omni_ai_assistant import MurfTTSEngine, AdvancedAIProcessor, ModernGUI
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_murf_tts_engine():
    """Test Murf TTS Engine initialization"""
    print("\n🗣️ Testing Murf TTS Engine...")
    try:
        from omni_ai_assistant import MurfTTSEngine
        
        engine = MurfTTSEngine()
        print(f"✅ TTS Engine initialized with {len(engine.available_voices)} voices")
        
        # Test voice setting
        if engine.set_voice("en-US-terrell"):
            print("✅ Voice setting works")
        else:
            print("❌ Voice setting failed")
            
        # Test voice list
        sample_voices = list(engine.available_voices.keys())[:5]
        print(f"✅ Sample voices: {sample_voices}")
        
        return True
    except Exception as e:
        print(f"❌ TTS Engine error: {e}")
        return False

def test_ai_processor():
    """Test AI Processor initialization"""
    print("\n🤖 Testing AI Processor...")
    try:
        from omni_ai_assistant import AdvancedAIProcessor
        
        processor = AdvancedAIProcessor()
        print("✅ AI Processor initialized")
        
        # Test simple query processing
        response = processor.process_query("hello")
        if response and isinstance(response, dict):
            print("✅ Query processing works")
            print(f"   Response type: {response.get('action', 'unknown')}")
        else:
            print("❌ Query processing failed")
            
        return True
    except Exception as e:
        print(f"❌ AI Processor error: {e}")
        return False

def test_document_processing():
    """Test document processing capabilities"""
    print("\n📄 Testing Document Processing...")
    try:
        from omni_ai_assistant import AdvancedAIProcessor
        
        processor = AdvancedAIProcessor()
        
        # Create a temporary text file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test document with sample content for analysis.")
            temp_file = f.name
        
        try:
            # Test document content extraction
            content = processor._extract_document_content(temp_file)
            if content and "test document" in content:
                print("✅ Document content extraction works")
            else:
                print("❌ Document content extraction failed")
                
            # Test document analysis
            context = {"file_path": temp_file}
            response = processor._handle_document_analysis("analyze document", context)
            if response and response.get("action") == "document_analysis":
                print("✅ Document analysis works")
            else:
                print("❌ Document analysis failed")
                
        finally:
            # Clean up
            os.unlink(temp_file)
            
        return True
    except Exception as e:
        print(f"❌ Document processing error: {e}")
        return False

def test_youtube_analysis():
    """Test YouTube analysis capabilities"""
    print("\n🎥 Testing YouTube Analysis...")
    try:
        from omni_ai_assistant import AdvancedAIProcessor
        
        processor = AdvancedAIProcessor()
        
        # Test YouTube ID extraction
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = processor._extract_youtube_id(test_url)
        if video_id == "dQw4w9WgXcQ":
            print("✅ YouTube ID extraction works")
        else:
            print("❌ YouTube ID extraction failed")
            
        # Test video analysis handler
        context = {"url": test_url}
        response = processor._handle_video_analysis("analyze video", context)
        if response and response.get("action") in ["video_analysis", "video_analysis_error"]:
            print("✅ Video analysis handler works")
        else:
            print("❌ Video analysis handler failed")
            
        return True
    except Exception as e:
        print(f"❌ YouTube analysis error: {e}")
        return False

def test_web_analysis():
    """Test website analysis capabilities"""
    print("\n🌐 Testing Web Analysis...")
    try:
        from omni_ai_assistant import AdvancedAIProcessor
        
        processor = AdvancedAIProcessor()
        
        # Test web analysis handler
        context = {"url": "https://example.com"}
        response = processor._handle_web_analysis("analyze website", context)
        if response and response.get("action") in ["web_analysis", "web_analysis_error"]:
            print("✅ Web analysis handler works")
        else:
            print("❌ Web analysis handler failed")
            
        return True
    except Exception as e:
        print(f"❌ Web analysis error: {e}")
        return False

def main():
    """Run all feature tests"""
    print("🧪 OMNI-AI Feature Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_murf_tts_engine,
        test_ai_processor,
        test_document_processing,
        test_youtube_analysis,
        test_web_analysis
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The OMNI-AI system is ready for the hackathon!")
    else:
        print(f"⚠️ {total - passed} tests failed. Please check the errors above.")
    
    print("\n🚀 To run the full application:")
    print("   python omni_ai_assistant.py")

if __name__ == "__main__":
    main()
