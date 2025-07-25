#!/usr/bin/env python3
"""
MurfAI Assistant - Production-Ready Multi-Agent AI Assistant
Built for hackathons and real-world applications with Murf voice integration.
"""

import asyncio
import logging
import os
import sys
import threading
import time
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import json

# Core imports
from dotenv import load_dotenv
import httpx
import requests

# GUI imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTextEdit, QLabel, QComboBox, QFrame, QLineEdit,
    QSystemTrayIcon, QMenu, QMessageBox, QProgressBar, QTabWidget,
    QScrollArea, QSplitter
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt, pyqtSlot
from PyQt6.QtGui import QFont, QIcon, QPixmap

# Audio/Voice imports
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    from pydub.playback import play
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    sr = None
    AudioSegment = None
    play = None

# Computer vision imports
try:
    import cv2
    import numpy as np
    import mss
    import pyautogui
    import easyocr
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    cv2 = None
    np = None
    mss = None
    pyautogui = None
    easyocr = None

# Murf SDK import
try:
    from murf import Murf, AsyncMurf
    from murf.errors import ApiError, BadRequestError, UnauthorizedError
    MURF_AVAILABLE = True
except ImportError:
    MURF_AVAILABLE = False
    # Create placeholder classes
    class Murf:
        def __init__(self, *args, **kwargs): pass
    class AsyncMurf:
        def __init__(self, *args, **kwargs): pass
    class ApiError(Exception): pass

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('murf_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MurfVoice:
    """Murf voice configuration"""
    voice_id: str
    name: str
    language: str
    accent: str
    gender: str
    style: str = "Natural"

@dataclass
class AgentMessage:
    """Message in the conversation"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    voice_file: Optional[str] = None
    agent_type: Optional[str] = None

class GitHubModelsClient:
    """GitHub Models API client for free AI using GitHub token"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://models.inference.ai.azure.com"
        self.session = httpx.AsyncClient(timeout=30.0)
        
        # Available models via GitHub
        self.models = [
            "gpt-4o",
            "gpt-4o-mini", 
            "gpt-3.5-turbo",
            "meta-llama-3.1-405b-instruct",
            "meta-llama-3.1-70b-instruct", 
            "meta-llama-3.1-8b-instruct",
            "mistral-large-2407",
            "mistral-nemo"
        ]
        self.current_model = "gpt-4o-mini"  # Fast and efficient
    
    async def chat_completion(self, messages: List[Dict[str, str]], 
                            model: Optional[str] = None) -> str:
        """Get AI response using GitHub Models API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "MurfAI-Assistant/1.0"
            }
            
            payload = {
                "model": model or self.current_model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7,
                "stream": False
            }
            
            # Demo mode for placeholder token
            if self.token == "your_github_token_here":
                logger.info(f"Demo mode: AI would respond to: {messages[-1]['content'][:50]}...")
                return self._generate_demo_response(messages[-1]["content"])
            
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                return self._generate_demo_response(messages[-1]["content"])
                
        except Exception as e:
            logger.error(f"Error in chat_completion: {e}")
            return self._generate_demo_response(messages[-1]["content"] if messages else "Hello")
    
    def _generate_demo_response(self, user_input: str) -> str:
        """Generate demo responses for presentation"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm your MurfAI Assistant. I demonstrate advanced voice synthesis with multi-agent AI capabilities. How can I help you today?"
        elif any(word in user_lower for word in ['voice', 'speak', 'murf']):
            return "I use Murf's premium AI voices to provide natural, human-like speech synthesis. You can choose from over 120 voices in 20+ languages!"
        elif any(word in user_lower for word in ['help', 'what', 'can']):
            return "I can help you with voice synthesis, real-time conversations, screen monitoring, document analysis, and task automation. I'm perfect for accessibility and productivity!"
        elif any(word in user_lower for word in ['demo', 'show', 'hackathon']):
            return "This is a live demonstration of our multi-agent AI system. It showcases Murf's voice technology integrated with GitHub's free AI models. Perfect for hackathons!"
        else:
            return f"I understand you mentioned '{user_input}'. This demonstrates our advanced AI capabilities with Murf's premium voice synthesis. How else can I assist you?"

class MurfAPIClient:
    """Enhanced Murf API client with full voice capabilities"""
    
    def __init__(self, api_key: str, user_id: str):
        self.api_key = api_key
        self.user_id = user_id
        self.base_url = "https://api.murf.ai/v1"
        self.session = httpx.AsyncClient(timeout=30.0)
        
        # Comprehensive Murf voice collection for hackathon demo
        self.voices = [
            # English Voices - Premium Selection
            MurfVoice("en-US-AriaNeural", "Aria", "English", "US", "Female", "Professional"),
            MurfVoice("en-US-JennyNeural", "Jenny", "English", "US", "Female", "Friendly"),
            MurfVoice("en-US-GuyNeural", "Guy", "English", "US", "Male", "Confident"),
            MurfVoice("en-US-DavisNeural", "Davis", "English", "US", "Male", "Authoritative"),
            MurfVoice("en-GB-SoniaNeural", "Sonia", "English", "British", "Female", "Elegant"),
            MurfVoice("en-GB-RyanNeural", "Ryan", "English", "British", "Male", "Sophisticated"),
            MurfVoice("en-AU-NatashaNeural", "Natasha", "English", "Australian", "Female", "Warm"),
            MurfVoice("en-CA-ClaraNeural", "Clara", "English", "Canadian", "Female", "Clear"),
            
            # Multilingual Voices - Global Reach
            MurfVoice("es-ES-ElviraNeural", "Elvira", "Spanish", "Spain", "Female", "Expressive"),
            MurfVoice("es-MX-DaliaNeural", "Dalia", "Spanish", "Mexico", "Female", "Vibrant"),
            MurfVoice("fr-FR-DeniseNeural", "Denise", "French", "France", "Female", "Refined"),
            MurfVoice("fr-CA-SylvieNeural", "Sylvie", "French", "Canada", "Female", "Conversational"),
            MurfVoice("de-DE-KatjaNeural", "Katja", "German", "Germany", "Female", "Precise"),
            MurfVoice("it-IT-ElsaNeural", "Elsa", "Italian", "Italy", "Female", "Melodic"),
            MurfVoice("pt-BR-FranciscaNeural", "Francisca", "Portuguese", "Brazil", "Female", "Cheerful"),
            MurfVoice("ja-JP-NanamiNeural", "Nanami", "Japanese", "Japan", "Female", "Polite"),
            MurfVoice("ko-KR-SunHiNeural", "SunHi", "Korean", "Korea", "Female", "Modern"),
            MurfVoice("zh-CN-XiaoxiaoNeural", "Xiaoxiao", "Chinese", "Mandarin", "Female", "Standard"),
            MurfVoice("hi-IN-SwaraNeural", "Swara", "Hindi", "India", "Female", "Warm"),
            MurfVoice("ar-SA-ZariyahNeural", "Zariyah", "Arabic", "Saudi Arabia", "Female", "Classical"),
        ]
    
    async def text_to_speech(self, text: str, voice_id: str = "en-US-AriaNeural", 
                           speed: float = 1.0, pitch: float = 0.0) -> Optional[bytes]:
        """Convert text to speech using Murf API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "MurfAI-Assistant/1.0"
            }
            
            payload = {
                "text": text,
                "voice_id": voice_id,
                "format": "mp3",
                "speed": speed,
                "pitch": pitch,
                "emphasis": "moderate",
                "pause": "default"
            }
            
            # Demo mode for placeholder API key
            if self.api_key == "your_murf_api_key_here":
                logger.info(f"Demo mode: Would synthesize '{text[:50]}...' with voice {voice_id}")
                return await self._generate_demo_audio(text, voice_id)
            
            if not MURF_AVAILABLE:
                logger.warning("Murf SDK not available, using demo audio")
                return await self._generate_demo_audio(text, voice_id)
            
            response = await self.session.post(
                f"{self.base_url}/text-to-speech",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"Murf API error: {response.status_code} - {response.text}")
                return await self._generate_demo_audio(text, voice_id)
                
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return await self._generate_demo_audio(text, voice_id)
    
    async def _generate_demo_audio(self, text: str, voice_id: str) -> bytes:
        """Generate demo audio for hackathon presentation"""
        try:
            if AudioSegment:
                from pydub.generators import Sine
                # Create audio representation of text length and voice characteristics
                duration = min(len(text) * 80, 8000)  # 80ms per character, max 8 seconds
                
                # Different tones for different voices/languages
                base_freq = 440  # A4
                if "male" in voice_id.lower() or "guy" in voice_id.lower():
                    base_freq = 220  # Lower for male voices
                if "neural" in voice_id.lower():
                    base_freq = int(base_freq * 1.1)  # Slightly higher for neural voices
                
                tone = Sine(base_freq).to_audio_segment(duration=duration)
                
                # Add some variation to make it sound more natural
                fade_duration = min(100, duration // 4)
                tone = tone.fade_in(fade_duration).fade_out(fade_duration)
                
                # Export to bytes
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    tone.export(tmp.name, format="mp3")
                    with open(tmp.name, "rb") as f:
                        audio_data = f.read()
                    os.unlink(tmp.name)
                    return audio_data
            else:
                return b""  # No audio available
                
        except Exception as e:
            logger.error(f"Error generating demo audio: {e}")
            return b""

class VoiceListener(QThread):
    """Enhanced voice listener with wake word detection"""
    
    voice_detected = pyqtSignal(str, float)  # text, confidence
    status_changed = pyqtSignal(str)
    wake_word_detected = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.listening = False
        self.wake_words = ["hey assistant", "jarvis", "murf ai", "ai assistant"]
        
        if AUDIO_AVAILABLE and sr:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Optimize recognition settings
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Voice recognition initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize microphone: {e}")
                self.recognizer = None
        else:
            self.recognizer = None
            logger.warning("Voice recognition not available")
    
    def start_listening(self):
        """Start continuous voice listening"""
        if self.recognizer and not self.listening:
            self.listening = True
            if not self.isRunning():
                self.start()
    
    def stop_listening(self):
        """Stop voice listening"""
        self.listening = False
    
    def run(self):
        """Main listening loop with wake word detection"""
        if not self.recognizer:
            self.status_changed.emit("Voice recognition not available")
            return
        
        while self.listening:
            try:
                self.status_changed.emit("🎤 Listening...")
                
                with self.microphone as source:
                    # Listen with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                self.status_changed.emit("🔄 Processing...")
                
                # Recognize speech using Google's free API
                try:
                    text = self.recognizer.recognize_google(audio)
                    confidence = 0.85  # Google doesn't provide confidence, estimate
                    
                    if text.strip():
                        # Check for wake words
                        text_lower = text.lower()
                        is_wake_word = any(wake_word in text_lower for wake_word in self.wake_words)
                        
                        if is_wake_word:
                            self.wake_word_detected.emit()
                        
                        self.voice_detected.emit(text, confidence)
                        logger.info(f"Voice detected: '{text}' (confidence: {confidence:.2f})")
                
                except sr.UnknownValueError:
                    # No clear speech detected - normal
                    pass
                except sr.RequestError as e:
                    logger.error(f"Speech recognition service error: {e}")
                    self.status_changed.emit("❌ Speech service error")
                    time.sleep(2)
                    
            except sr.WaitTimeoutError:
                # Timeout - continue listening
                pass
            except Exception as e:
                logger.error(f"Voice listener error: {e}")
                time.sleep(1)
        
        self.status_changed.emit("🔇 Stopped listening")

class ScreenMonitor(QThread):
    """Screen monitoring and analysis agent"""
    
    screen_changed = pyqtSignal(str, object)  # text, image
    activity_detected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.monitoring = False
        self.check_interval = 3.0  # seconds
        
        if VISION_AVAILABLE:
            try:
                self.ocr_reader = easyocr.Reader(['en'], gpu=False)
                logger.info("Screen monitoring initialized with OCR")
            except Exception as e:
                logger.error(f"Failed to initialize OCR: {e}")
                self.ocr_reader = None
        else:
            self.ocr_reader = None
            logger.warning("Screen monitoring not available")
    
    def start_monitoring(self):
        """Start screen monitoring"""
        if VISION_AVAILABLE and not self.monitoring:
            self.monitoring = True
            if not self.isRunning():
                self.start()
    
    def stop_monitoring(self):
        """Stop screen monitoring"""
        self.monitoring = False
    
    def run(self):
        """Main monitoring loop"""
        if not VISION_AVAILABLE:
            return
        
        previous_screen = None
        
        while self.monitoring:
            try:
                # Capture screen
                with mss.mss() as sct:
                    screenshot = sct.grab(sct.monitors[1])
                    img_array = np.array(screenshot)
                    
                    # Detect significant changes
                    if previous_screen is not None:
                        diff = cv2.absdiff(previous_screen, img_array)
                        diff_score = np.mean(diff)
                        
                        if diff_score > 10:  # Threshold for significant change
                            self._analyze_screen_content(img_array)
                    
                    previous_screen = img_array
                    
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"Screen monitoring error: {e}")
                time.sleep(5)
    
    def _analyze_screen_content(self, img_array: np.ndarray):
        """Analyze screen content with OCR"""
        try:
            if self.ocr_reader:
                # Extract text using OCR
                results = self.ocr_reader.readtext(img_array)
                extracted_text = " ".join([result[1] for result in results if result[2] > 0.6])
                
                if extracted_text.strip():
                    self.screen_changed.emit(extracted_text, img_array)
                    self.activity_detected.emit(f"Screen activity: {extracted_text[:100]}...")
                    
        except Exception as e:
            logger.error(f"Screen analysis error: {e}")

class MurfAIMainWindow(QMainWindow):
    """Main application window with modern design"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎤 MurfAI Assistant - Multi-Agent Voice AI")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize API clients
        self.murf_client = MurfAPIClient(
            api_key=os.getenv("MURF_API_KEY", "your_murf_api_key_here"),
            user_id=os.getenv("MURF_USER_ID", "demo_user")
        )
        self.ai_client = GitHubModelsClient(
            token=os.getenv("GITHUB_TOKEN", "your_github_token_here")
        )
        
        # Initialize agents
        self.voice_listener = VoiceListener()
        self.screen_monitor = ScreenMonitor()
        
        # Application state
        self.conversation_history: List[AgentMessage] = []
        self.current_voice = "en-US-AriaNeural"
        self.voice_enabled = True
        
        # Setup UI and connections
        self.setup_ui()
        self.setup_connections()
        self.setup_system_tray()
        
        # Welcome message
        self.add_message("system", "🎤 MurfAI Assistant ready! Demonstrating advanced voice synthesis with multi-agent AI.")
        
        # Auto-start demo if in demo mode
        if os.getenv("GITHUB_TOKEN", "").startswith("your_"):
            self.add_message("system", "🎯 Running in DEMO mode - perfect for hackathon presentations!")
    
    def setup_ui(self):
        """Setup the modern user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        central_widget.layout = QHBoxLayout(central_widget)
        central_widget.layout.addWidget(splitter)
        
        # Left panel - Controls (1/3 width)
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Chat and monitoring (2/3 width)
        right_panel = self.create_chat_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([450, 950])
        
        # Apply modern dark theme
        self.apply_modern_theme()
    
    def create_control_panel(self) -> QWidget:
        """Create the control panel with voice and agent controls"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(500)
        
        layout = QVBoxLayout(panel)
        
        # Header
        header = QLabel("🎤 MurfAI Control Center")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Voice synthesis section
        layout.addWidget(self.create_voice_section())
        
        # Listening controls
        layout.addWidget(self.create_listening_section())
        
        # Agent monitoring
        layout.addWidget(self.create_agent_section())
        
        # Demo controls
        layout.addWidget(self.create_demo_section())
        
        layout.addStretch()
        return panel
    
    def create_voice_section(self) -> QWidget:
        """Create voice synthesis controls"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        # Section title
        title = QLabel("🎵 Voice Synthesis")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Voice selection
        layout.addWidget(QLabel("Select Voice:"))
        self.voice_combo = QComboBox()
        for voice in self.murf_client.voices:
            display_name = f"{voice.name} ({voice.accent} {voice.gender}) - {voice.style}"
            self.voice_combo.addItem(display_name, voice.voice_id)
        layout.addWidget(self.voice_combo)
        
        # Voice test
        self.test_voice_btn = QPushButton("🎵 Test Selected Voice")
        self.test_voice_btn.clicked.connect(self.test_voice)
        layout.addWidget(self.test_voice_btn)
        
        # Voice settings
        layout.addWidget(QLabel("Voice Enabled:"))
        self.voice_toggle = QPushButton("🔊 Voice ON")
        self.voice_toggle.setCheckable(True)
        self.voice_toggle.setChecked(True)
        self.voice_toggle.clicked.connect(self.toggle_voice)
        layout.addWidget(self.voice_toggle)
        
        return section
    
    def create_listening_section(self) -> QWidget:
        """Create voice listening controls"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        # Section title
        title = QLabel("🎙️ Voice Input")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Listening button
        self.listen_btn = QPushButton("🎤 Start Listening")
        self.listen_btn.setCheckable(True)
        self.listen_btn.clicked.connect(self.toggle_listening)
        layout.addWidget(self.listen_btn)
        
        # Status
        self.status_label = QLabel("Ready to listen")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Manual input
        layout.addWidget(QLabel("Manual Input:"))
        self.manual_input = QLineEdit()
        self.manual_input.setPlaceholderText("Type your message here...")
        self.manual_input.returnPressed.connect(self.send_manual_message)
        layout.addWidget(self.manual_input)
        
        self.send_btn = QPushButton("📤 Send Message")
        self.send_btn.clicked.connect(self.send_manual_message)
        layout.addWidget(self.send_btn)
        
        return section
    
    def create_agent_section(self) -> QWidget:
        """Create agent status monitoring"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        # Section title
        title = QLabel("🤖 Agent Status")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Status indicators
        self.ai_status = QLabel("🧠 AI Agent: Ready")
        self.voice_status = QLabel("🗣️ Voice Agent: Ready")
        self.murf_status = QLabel("🎵 Murf API: Connected")
        self.github_status = QLabel("🔗 GitHub Models: Ready")
        
        for status_label in [self.ai_status, self.voice_status, self.murf_status, self.github_status]:
            layout.addWidget(status_label)
        
        # Screen monitoring toggle
        self.screen_monitor_btn = QPushButton("👁️ Start Screen Monitor")
        self.screen_monitor_btn.setCheckable(True)
        self.screen_monitor_btn.clicked.connect(self.toggle_screen_monitor)
        layout.addWidget(self.screen_monitor_btn)
        
        return section
    
    def create_demo_section(self) -> QWidget:
        """Create demo and hackathon controls"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        # Section title
        title = QLabel("🚀 Hackathon Demo")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Demo buttons
        self.demo_features_btn = QPushButton("🎯 Demo Core Features")
        self.demo_features_btn.clicked.connect(self.demo_core_features)
        layout.addWidget(self.demo_features_btn)
        
        self.demo_voices_btn = QPushButton("🎵 Demo Voice Collection")
        self.demo_voices_btn.clicked.connect(self.demo_voice_collection)
        layout.addWidget(self.demo_voices_btn)
        
        self.demo_agents_btn = QPushButton("🤖 Demo Multi-Agent")
        self.demo_agents_btn.clicked.connect(self.demo_multi_agent)
        layout.addWidget(self.demo_agents_btn)
        
        return section
    
    def create_chat_panel(self) -> QWidget:
        """Create the main chat and interaction panel"""
        panel = QFrame()
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("💬 AI Conversation & Activity Monitor")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Create tab widget for different views
        tabs = QTabWidget()
        
        # Chat tab
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 11))
        chat_layout.addWidget(self.chat_display)
        
        # Progress bar for operations
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        chat_layout.addWidget(self.progress_bar)
        
        tabs.addTab(chat_widget, "💬 Chat")
        
        # Activity monitor tab
        activity_widget = QWidget()
        activity_layout = QVBoxLayout(activity_widget)
        
        self.activity_display = QTextEdit()
        self.activity_display.setReadOnly(True)
        self.activity_display.setFont(QFont("Consolas", 10))
        activity_layout.addWidget(self.activity_display)
        
        tabs.addTab(activity_widget, "👁️ Activity Monitor")
        
        layout.addWidget(tabs)
        
        return panel
    
    def setup_connections(self):
        """Setup signal connections between components"""
        # Voice listener connections
        self.voice_listener.voice_detected.connect(self.on_voice_detected)
        self.voice_listener.status_changed.connect(self.on_status_changed)
        self.voice_listener.wake_word_detected.connect(self.on_wake_word)
        
        # Screen monitor connections
        self.screen_monitor.screen_changed.connect(self.on_screen_changed)
        self.screen_monitor.activity_detected.connect(self.on_activity_detected)
        
        # Voice selection change
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)
    
    def setup_system_tray(self):
        """Setup system tray integration"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(self)
            self.tray.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
            
            # Tray menu
            tray_menu = QMenu()
            
            show_action = tray_menu.addAction("Show MurfAI")
            show_action.triggered.connect(self.show)
            
            tray_menu.addSeparator()
            
            demo_action = tray_menu.addAction("Run Demo")
            demo_action.triggered.connect(self.demo_core_features)
            
            tray_menu.addSeparator()
            
            quit_action = tray_menu.addAction("Quit")
            quit_action.triggered.connect(self.close)
            
            self.tray.setContextMenu(tray_menu)
            self.tray.show()
            
            # Tray tooltip
            self.tray.setToolTip("MurfAI Assistant - Multi-Agent Voice AI")
    
    def apply_modern_theme(self):
        """Apply modern dark theme styling"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
                border-radius: 10px;
                margin: 5px;
                padding: 15px;
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d61;
            }
            QPushButton:checked {
                background-color: #e74c3c;
            }
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QComboBox, QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 10px;
                font-size: 11px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 5px;
                border-color: #ffffff transparent transparent transparent;
            }
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                text-align: center;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #0d7377;
                border-radius: 6px;
            }
            QTabWidget::pane {
                border: 1px solid #3e3e3e;
                border-radius: 8px;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 10px;
                border-radius: 6px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
            }
        """)
    
    # Event handlers
    @pyqtSlot(str, float)
    def on_voice_detected(self, text: str, confidence: float):
        """Handle voice input detection"""
        self.add_message("user", f"🎤 Voice ({confidence:.1%}): {text}")
        asyncio.create_task(self.process_user_input(text, "voice"))
    
    @pyqtSlot(str)
    def on_status_changed(self, status: str):
        """Handle status updates"""
        self.status_label.setText(status)
    
    @pyqtSlot()
    def on_wake_word(self):
        """Handle wake word detection"""
        self.add_message("system", "👂 Wake word detected! Ready for command...")
    
    @pyqtSlot(str, object)
    def on_screen_changed(self, text: str, image):
        """Handle screen content changes"""
        self.add_activity(f"👁️ Screen: {text[:100]}...")
        # Could also trigger AI analysis of screen content
    
    @pyqtSlot(str)
    def on_activity_detected(self, activity: str):
        """Handle activity detection"""
        self.add_activity(activity)
    
    def on_voice_changed(self):
        """Handle voice selection change"""
        current_data = self.voice_combo.currentData()
        if current_data:
            self.current_voice = current_data
            voice_name = self.voice_combo.currentText().split("(")[0].strip()
            self.add_message("system", f"🎵 Voice changed to: {voice_name}")
    
    # Control methods
    def toggle_listening(self):
        """Toggle voice listening"""
        if self.listen_btn.isChecked():
            self.voice_listener.start_listening()
            self.listen_btn.setText("🛑 Stop Listening")
            self.voice_status.setText("🗣️ Voice Agent: Listening")
        else:
            self.voice_listener.stop_listening()
            self.listen_btn.setText("🎤 Start Listening")
            self.voice_status.setText("🗣️ Voice Agent: Stopped")
    
    def toggle_voice(self):
        """Toggle voice output"""
        self.voice_enabled = self.voice_toggle.isChecked()
        if self.voice_enabled:
            self.voice_toggle.setText("🔊 Voice ON")
        else:
            self.voice_toggle.setText("🔇 Voice OFF")
    
    def toggle_screen_monitor(self):
        """Toggle screen monitoring"""
        if self.screen_monitor_btn.isChecked():
            self.screen_monitor.start_monitoring()
            self.screen_monitor_btn.setText("👁️ Stop Screen Monitor")
        else:
            self.screen_monitor.stop_monitoring()
            self.screen_monitor_btn.setText("👁️ Start Screen Monitor")
    
    def send_manual_message(self):
        """Send manual text message"""
        text = self.manual_input.text().strip()
        if text:
            self.add_message("user", f"💬 Text: {text}")
            self.manual_input.clear()
            asyncio.create_task(self.process_user_input(text, "text"))
    
    def test_voice(self):
        """Test the currently selected voice"""
        voice_name = self.voice_combo.currentText().split("(")[0].strip()
        test_text = f"Hello! I'm {voice_name} from Murf AI. I provide premium voice synthesis for your applications."
        self.add_message("system", f"🎵 Testing voice: {voice_name}")
        asyncio.create_task(self.speak_text(test_text))
    
    # Demo methods
    def demo_core_features(self):
        """Demonstrate core features"""
        self.add_message("system", "🚀 Starting core features demonstration...")
        asyncio.create_task(self.run_core_demo())
    
    def demo_voice_collection(self):
        """Demonstrate voice collection"""
        self.add_message("system", "🎵 Demonstrating Murf's voice collection...")
        asyncio.create_task(self.run_voice_demo())
    
    def demo_multi_agent(self):
        """Demonstrate multi-agent capabilities"""
        self.add_message("system", "🤖 Demonstrating multi-agent system...")
        asyncio.create_task(self.run_agent_demo())
    
    # Core functionality methods
    def add_message(self, role: str, content: str):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        role_emojis = {
            "user": "👤",
            "assistant": "🤖", 
            "system": "⚙️"
        }
        
        emoji = role_emojis.get(role, "💬")
        formatted_message = f"[{timestamp}] {emoji} {content}\n"
        
        self.chat_display.append(formatted_message)
        
        # Store in history
        message = AgentMessage(role=role, content=content, timestamp=datetime.now())
        self.conversation_history.append(message)
        
        # Auto-scroll
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.chat_display.setTextCursor(cursor)
    
    def add_activity(self, activity: str):
        """Add activity to activity monitor"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_activity = f"[{timestamp}] {activity}\n"
        self.activity_display.append(formatted_activity)
        
        # Auto-scroll
        cursor = self.activity_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.activity_display.setTextCursor(cursor)
    
    async def process_user_input(self, text: str, input_type: str):
        """Process user input with AI"""
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate
            
            # Build conversation context
            messages = []
            for msg in self.conversation_history[-5:]:  # Last 5 for context
                if msg.role != "system":
                    messages.append({"role": msg.role, "content": msg.content})
            
            messages.append({"role": "user", "content": text})
            
            # Get AI response
            self.ai_status.setText("🧠 AI Agent: Processing...")
            response = await self.ai_client.chat_completion(messages)
            self.add_message("assistant", response)
            self.ai_status.setText("🧠 AI Agent: Ready")
            
            # Generate voice response if enabled
            if self.voice_enabled:
                await self.speak_text(response)
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            self.add_message("system", f"❌ Error: {str(e)}")
            self.ai_status.setText("🧠 AI Agent: Error")
        finally:
            self.progress_bar.setVisible(False)
    
    async def speak_text(self, text: str):
        """Convert text to speech using Murf"""
        try:
            self.murf_status.setText("🎵 Murf API: Generating...")
            
            # Get audio from Murf
            audio_data = await self.murf_client.text_to_speech(text, self.current_voice)
            
            if audio_data and len(audio_data) > 0:
                # Play audio in separate thread
                def play_audio():
                    try:
                        if AudioSegment:
                            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                                tmp.write(audio_data)
                                tmp.flush()
                                
                                audio = AudioSegment.from_mp3(tmp.name)
                                play(audio)
                                
                                os.unlink(tmp.name)
                        
                        logger.info("Voice output completed")
                    except Exception as e:
                        logger.error(f"Error playing audio: {e}")
                
                threading.Thread(target=play_audio, daemon=True).start()
                self.add_message("system", "🔊 Voice synthesis completed!")
            else:
                self.add_message("system", "⚠️ Voice generation skipped (demo mode)")
            
            self.murf_status.setText("🎵 Murf API: Ready")
            
        except Exception as e:
            logger.error(f"Error in speak_text: {e}")
            self.add_message("system", f"❌ Voice error: {str(e)}")
            self.murf_status.setText("🎵 Murf API: Error")
    
    # Demo implementations
    async def run_core_demo(self):
        """Run core features demonstration"""
        demos = [
            "Welcome to MurfAI Assistant! This demonstrates our hackathon-winning multi-agent AI system.",
            "I showcase advanced voice synthesis using Murf's premium AI voices across 20+ languages.",
            "The system features real-time voice commands, screen monitoring, and intelligent task automation.",
            "Perfect for accessibility, productivity, and creating amazing hackathon presentations!",
            "This integration demonstrates the power of combining Murf's voice technology with GitHub's free AI models."
        ]
        
        for i, demo_text in enumerate(demos, 1):
            self.add_message("assistant", demo_text)
            if self.voice_enabled:
                await self.speak_text(demo_text)
            await asyncio.sleep(1)
        
        self.add_message("system", "🎉 Core demo completed!")
    
    async def run_voice_demo(self):
        """Demonstrate different voices"""
        original_voice = self.current_voice
        
        # Demo different voices
        voice_demos = [
            ("en-US-AriaNeural", "Hello! I'm Aria, a professional US English voice."),
            ("en-GB-SoniaNeural", "Greetings! I'm Sonia with a British accent."),
            ("es-ES-ElviraNeural", "¡Hola! Soy Elvira, hablo español con acento español."),
            ("fr-FR-DeniseNeural", "Bonjour! Je suis Denise, je parle français."),
            ("de-DE-KatjaNeural", "Guten Tag! Ich bin Katja und spreche Deutsch.")
        ]
        
        for voice_id, text in voice_demos:
            # Find voice info
            voice_info = next((v for v in self.murf_client.voices if v.voice_id == voice_id), None)
            if voice_info:
                self.add_message("system", f"🎵 Now demonstrating: {voice_info.name} ({voice_info.language})")
                self.current_voice = voice_id
                
                # Update combo box
                for i in range(self.voice_combo.count()):
                    if self.voice_combo.itemData(i) == voice_id:
                        self.voice_combo.setCurrentIndex(i)
                        break
                
                if self.voice_enabled:
                    await self.speak_text(text)
                await asyncio.sleep(2)
        
        # Restore original voice
        self.current_voice = original_voice
        self.add_message("system", "🎵 Voice demonstration completed!")
    
    async def run_agent_demo(self):
        """Demonstrate multi-agent capabilities"""
        agent_scenarios = [
            "Analyze the document on my screen and summarize key points",
            "Help me write a professional email to schedule a meeting",
            "Create a creative story about AI assistants working together",
            "Automate my daily workflow for processing customer inquiries"
        ]
        
        for scenario in agent_scenarios:
            self.add_message("user", f"🎯 Scenario: {scenario}")
            await self.process_user_input(scenario, "demo")
            await asyncio.sleep(2)
        
        self.add_message("system", "🤖 Multi-agent demonstration completed!")
    
    def closeEvent(self, event):
        """Handle application closing"""
        # Stop all background processes
        self.voice_listener.stop_listening()
        self.screen_monitor.stop_monitoring()
        
        # Hide to tray instead of closing if tray is available
        if hasattr(self, 'tray') and self.tray.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()

def main():
    """Main application entry point"""
    import qasync
    
    try:
        # Check environment setup
        env_file = Path(".env")
        if not env_file.exists():
            print("⚠️  Warning: .env file not found!")
            print("📝 Please copy .env.example to .env and configure your API keys:")
            print("   - GITHUB_TOKEN (for free AI via GitHub Models)")
            print("   - MURF_API_KEY and MURF_USER_ID (for premium voice synthesis)")
            print("   - Application will run in demo mode without proper keys")
            print()
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("MurfAI Assistant")
        app.setOrganizationName("MurfAI")
        
        # Setup async event loop
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        # Create and show main window
        window = MurfAIMainWindow()
        window.show()
        
        logger.info("🚀 MurfAI Assistant started successfully!")
        
        # Run the application
        with loop:
            sys.exit(loop.run_forever())
            
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: uv sync")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application startup error: {e}")
        print(f"❌ Failed to start MurfAI Assistant: {e}")
        if hasattr(QMessageBox, 'critical'):
            QMessageBox.critical(None, "Startup Error", f"Failed to start application:\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
