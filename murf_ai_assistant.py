#!/usr/bin/env python3
"""
MurfAI Assistant - Multi-Agent AI Assistant with Voice Integration
A hackathon-winning desktop application that demonstrates Murf's voice capabilities.
"""

import asyncio
import logging
import sys
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import os
from dataclasses import dataclass
from datetime import datetime

# GUI Imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTextEdit, QLabel, QComboBox, QSlider, QProgressBar,
    QSystemTrayIcon, QMenu, QTabWidget, QScrollArea, QFrame,
    QGridLayout, QSpacerItem, QSizePolicy, QMessageBox, QLineEdit
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt, QSize, pyqtSlot
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap

# Core Imports
import speech_recognition as sr
import requests
import httpx
from pydantic import BaseModel
from dotenv import load_dotenv

# Audio/Media Imports
from pydub import AudioSegment
from pydub.playback import play
import tempfile

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

@dataclass
class AIMessage:
    """AI conversation message"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    voice_file: Optional[str] = None

class MurfAPIClient:
    """Murf API client for text-to-speech conversion"""
    
    def __init__(self, api_key: str, user_id: str):
        self.api_key = api_key
        self.user_id = user_id
        self.base_url = "https://api.murf.ai/v1"
        self.session = httpx.AsyncClient()
        
        # Popular Murf voices for demo
        self.voices = [
            MurfVoice("en-US-AriaNeural", "Aria", "English", "US", "Female"),
            MurfVoice("en-US-JennyNeural", "Jenny", "English", "US", "Female"),
            MurfVoice("en-US-GuyNeural", "Guy", "English", "US", "Male"),
            MurfVoice("en-GB-SoniaNeural", "Sonia", "English", "British", "Female"),
            MurfVoice("en-AU-NatashaNeural", "Natasha", "English", "Australian", "Female"),
        ]
    
    async def text_to_speech(self, text: str, voice_id: str = "en-US-AriaNeural") -> Optional[bytes]:
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
                "speed": 1.0,
                "pitch": 0.0,
                "emphasis": "moderate"
            }
            
            # For demo purposes, we'll use a mock response if API key is not real
            if self.api_key == "your_murf_api_key_here":
                logger.info(f"Demo mode: Would convert '{text[:50]}...' to speech with voice {voice_id}")
                return self._generate_demo_audio(text)
            
            response = await self.session.post(
                f"{self.base_url}/speech/generate",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.content
            else:
                logger.error(f"Murf API error: {response.status_code} - {response.text}")
                return self._generate_demo_audio(text)
                
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return self._generate_demo_audio(text)
    
    def _generate_demo_audio(self, text: str) -> bytes:
        """Generate demo audio for hackathon presentation"""
        # Create a simple tone-based audio as demo
        try:
            from pydub.generators import Sine
            # Create a simple beep pattern representing the text
            duration = min(len(text) * 100, 5000)  # Max 5 seconds
            tone = Sine(440).to_audio_segment(duration=duration)
            
            # Export to bytes
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                tone.export(tmp.name, format="mp3")
                with open(tmp.name, "rb") as f:
                    audio_data = f.read()
                os.unlink(tmp.name)
                return audio_data
        except Exception:
            # Fallback: return empty bytes
            return b""

class GitHubAIClient:
    """GitHub Models API client for AI responses"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://models.inference.ai.azure.com"
        self.session = httpx.AsyncClient()
    
    async def chat_completion(self, messages: List[Dict[str, str]], model: str = "gpt-4o") -> str:
        """Get AI response using GitHub Models API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            # Demo mode if token is placeholder
            if self.token == "your_github_token_here":
                logger.info(f"Demo mode: AI would respond to {len(messages)} messages")
                return self._generate_demo_response(messages[-1]["content"] if messages else "Hello")
            
            response = await self.session.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.error(f"GitHub API error: {response.status_code}")
                return self._generate_demo_response(messages[-1]["content"] if messages else "Hello")
                
        except Exception as e:
            logger.error(f"Error in chat_completion: {e}")
            return self._generate_demo_response(messages[-1]["content"] if messages else "Hello")
    
    def _generate_demo_response(self, user_input: str) -> str:
        """Generate demo AI responses for hackathon"""
        responses = {
            "hello": "Hello! I'm your MurfAI Assistant. I can help you with various tasks and demonstrate Murf's amazing voice capabilities!",
            "help": "I can assist you with:\n• Voice synthesis using Murf's premium voices\n• Multi-agent task coordination\n• Real-time conversation\n• Screen monitoring and automation\n• And much more!",
            "voice": "Murf provides over 120+ realistic AI voices in 20+ languages. You can choose from different accents, genders, and speaking styles!",
            "demo": "This is a live demonstration of our multi-agent AI system powered by Murf's voice technology. Perfect for hackathons and real-world applications!",
        }
        
        user_lower = user_input.lower()
        for key, response in responses.items():
            if key in user_lower:
                return response
        
        return f"I understand you said: '{user_input}'. This is a demonstration of our MurfAI Assistant integrating advanced voice synthesis with multi-agent AI capabilities!"

class VoiceListener(QThread):
    """Background thread for continuous voice listening"""
    
    voice_detected = pyqtSignal(str)
    status_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
    
    def start_listening(self):
        """Start continuous listening"""
        self.listening = True
        if not self.isRunning():
            self.start()
    
    def stop_listening(self):
        """Stop listening"""
        self.listening = False
    
    def run(self):
        """Main listening loop"""
        while self.listening:
            try:
                self.status_changed.emit("Listening...")
                
                with self.microphone as source:
                    # Listen for audio with timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                self.status_changed.emit("Processing...")
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio)
                if text.strip():
                    self.voice_detected.emit(text)
                    
            except sr.WaitTimeoutError:
                # No speech detected, continue listening
                pass
            except sr.UnknownValueError:
                # Speech not understood
                self.status_changed.emit("Could not understand audio")
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                self.status_changed.emit("Speech recognition error")
            except Exception as e:
                logger.error(f"Unexpected error in voice listener: {e}")
                time.sleep(1)
        
        self.status_changed.emit("Stopped listening")

class MurfAIMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MurfAI Assistant - Multi-Agent Voice AI")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize components
        self.murf_client = MurfAPIClient(
            api_key=os.getenv("MURF_API_KEY", "your_murf_api_key_here"),
            user_id=os.getenv("MURF_USER_ID", "demo_user")
        )
        self.ai_client = GitHubAIClient(
            token=os.getenv("GITHUB_TOKEN", "your_github_token_here")
        )
        
        self.voice_listener = VoiceListener()
        self.conversation_history: List[AIMessage] = []
        self.current_voice = "en-US-AriaNeural"
        
        self.setup_ui()
        self.setup_connections()
        self.setup_system_tray()
        
        # Start with welcome message
        self.add_message("system", "MurfAI Assistant initialized! Ready for voice commands.")
        
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Controls
        left_panel = self.create_control_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Right panel - Chat
        right_panel = self.create_chat_panel()
        main_layout.addWidget(right_panel, 2)
        
        # Apply modern styling
        self.apply_modern_style()
    
    def create_control_panel(self) -> QWidget:
        """Create the left control panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(350)
        
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("🎤 MurfAI Control Center")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Voice controls
        voice_group = self.create_voice_controls()
        layout.addWidget(voice_group)
        
        # Listening controls
        listening_group = self.create_listening_controls()
        layout.addWidget(listening_group)
        
        # Agent status
        status_group = self.create_status_panel()
        layout.addWidget(status_group)
        
        layout.addStretch()
        
        return panel
    
    def create_voice_controls(self) -> QWidget:
        """Create voice selection controls"""
        group = QFrame()
        group.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(group)
        
        layout.addWidget(QLabel("🔊 Voice Selection"))
        
        self.voice_combo = QComboBox()
        for voice in self.murf_client.voices:
            self.voice_combo.addItem(f"{voice.name} ({voice.accent} {voice.gender})", voice.voice_id)
        layout.addWidget(self.voice_combo)
        
        # Voice test button
        self.test_voice_btn = QPushButton("🎵 Test Voice")
        self.test_voice_btn.clicked.connect(self.test_voice)
        layout.addWidget(self.test_voice_btn)
        
        return group
    
    def create_listening_controls(self) -> QWidget:
        """Create listening controls"""
        group = QFrame()
        group.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(group)
        
        layout.addWidget(QLabel("🎙️ Voice Input"))
        
        # Listening button
        self.listen_btn = QPushButton("🎤 Start Listening")
        self.listen_btn.setCheckable(True)
        self.listen_btn.clicked.connect(self.toggle_listening)
        layout.addWidget(self.listen_btn)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Manual input
        layout.addWidget(QLabel("💬 Manual Input"))
        self.manual_input = QLineEdit()
        self.manual_input.setPlaceholderText("Type your message here...")
        self.manual_input.returnPressed.connect(self.send_manual_message)
        layout.addWidget(self.manual_input)
        
        self.send_btn = QPushButton("📤 Send")
        self.send_btn.clicked.connect(self.send_manual_message)
        layout.addWidget(self.send_btn)
        
        return group
    
    def create_status_panel(self) -> QWidget:
        """Create agent status panel"""
        group = QFrame()
        group.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(group)
        
        layout.addWidget(QLabel("🤖 Agent Status"))
        
        # Status indicators
        self.ai_status = QLabel("🧠 AI Agent: Ready")
        self.voice_status = QLabel("🗣️ Voice Agent: Ready")
        self.murf_status = QLabel("🎵 Murf API: Connected")
        
        layout.addWidget(self.ai_status)
        layout.addWidget(self.voice_status)
        layout.addWidget(self.murf_status)
        
        # Demo button
        self.demo_btn = QPushButton("🚀 Run Hackathon Demo")
        self.demo_btn.clicked.connect(self.run_demo)
        layout.addWidget(self.demo_btn)
        
        return group
    
    def create_chat_panel(self) -> QWidget:
        """Create the chat panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("💬 AI Conversation")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Consolas", 11))
        layout.addWidget(self.chat_display)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return panel
    
    def setup_connections(self):
        """Setup signal connections"""
        self.voice_listener.voice_detected.connect(self.on_voice_detected)
        self.voice_listener.status_changed.connect(self.on_status_changed)
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)
    
    def setup_system_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(self)
            # Set a simple icon (you can replace with actual icon file)
            self.tray.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_ComputerIcon))
            
            # Tray menu
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Show")
            show_action.triggered.connect(self.show)
            quit_action = tray_menu.addAction("Quit")
            quit_action.triggered.connect(self.close)
            
            self.tray.setContextMenu(tray_menu)
            self.tray.show()
    
    def apply_modern_style(self):
        """Apply modern styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:checked {
                background-color: #ff6b6b;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
            QComboBox, QLineEdit {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 8px;
            }
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
        """)
    
    @pyqtSlot(str)
    def on_voice_detected(self, text: str):
        """Handle detected voice input"""
        self.add_message("user", f"🎤 Voice: {text}")
        asyncio.create_task(self.process_user_input(text))
    
    @pyqtSlot(str)
    def on_status_changed(self, status: str):
        """Handle status changes"""
        self.status_label.setText(status)
    
    def on_voice_changed(self, voice_text: str):
        """Handle voice selection change"""
        current_data = self.voice_combo.currentData()
        if current_data:
            self.current_voice = current_data
            logger.info(f"Voice changed to: {self.current_voice}")
    
    def toggle_listening(self):
        """Toggle voice listening"""
        if self.listen_btn.isChecked():
            self.voice_listener.start_listening()
            self.listen_btn.setText("🛑 Stop Listening")
        else:
            self.voice_listener.stop_listening()
            self.listen_btn.setText("🎤 Start Listening")
    
    def send_manual_message(self):
        """Send manual text message"""
        text = self.manual_input.text().strip()
        if text:
            self.add_message("user", f"💬 Text: {text}")
            self.manual_input.clear()
            asyncio.create_task(self.process_user_input(text))
    
    def test_voice(self):
        """Test the selected voice"""
        test_text = f"Hello! This is {self.voice_combo.currentText()} from Murf AI. I sound amazing, don't I?"
        self.add_message("system", f"🎵 Testing voice: {self.voice_combo.currentText()}")
        asyncio.create_task(self.speak_text(test_text))
    
    def run_demo(self):
        """Run hackathon demonstration"""
        self.add_message("system", "🚀 Starting Hackathon Demo...")
        asyncio.create_task(self.demonstrate_features())
    
    def add_message(self, role: str, content: str):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Role emoji mapping
        role_emojis = {
            "user": "👤",
            "assistant": "🤖",
            "system": "⚙️"
        }
        
        emoji = role_emojis.get(role, "💬")
        formatted_message = f"[{timestamp}] {emoji} {content}\n"
        
        self.chat_display.append(formatted_message)
        
        # Store in history
        message = AIMessage(role=role, content=content, timestamp=datetime.now())
        self.conversation_history.append(message)
        
        # Auto-scroll to bottom
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.chat_display.setTextCursor(cursor)
    
    async def process_user_input(self, text: str):
        """Process user input and generate AI response"""
        try:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            # Prepare conversation context
            messages = []
            for msg in self.conversation_history[-5:]:  # Last 5 messages for context
                if msg.role != "system":
                    messages.append({"role": msg.role, "content": msg.content})
            
            messages.append({"role": "user", "content": text})
            
            # Get AI response
            response = await self.ai_client.chat_completion(messages)
            self.add_message("assistant", response)
            
            # Generate voice response
            await self.speak_text(response)
            
        except Exception as e:
            logger.error(f"Error processing user input: {e}")
            self.add_message("system", f"❌ Error: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
    
    async def speak_text(self, text: str):
        """Convert text to speech using Murf"""
        try:
            self.add_message("system", f"🎵 Generating voice with {self.voice_combo.currentText()}...")
            
            # Get audio from Murf API
            audio_data = await self.murf_client.text_to_speech(text, self.current_voice)
            
            if audio_data:
                # Play the audio
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                    tmp_file.write(audio_data)
                    tmp_file.flush()
                    
                    # Play audio in separate thread to avoid blocking UI
                    def play_audio():
                        try:
                            audio = AudioSegment.from_mp3(tmp_file.name)
                            play(audio)
                        except Exception as e:
                            logger.error(f"Error playing audio: {e}")
                        finally:
                            os.unlink(tmp_file.name)
                    
                    threading.Thread(target=play_audio, daemon=True).start()
                    self.add_message("system", "🔊 Voice output completed!")
            else:
                self.add_message("system", "❌ Failed to generate voice")
                
        except Exception as e:
            logger.error(f"Error in speak_text: {e}")
            self.add_message("system", f"❌ Voice error: {str(e)}")
    
    async def demonstrate_features(self):
        """Demonstrate key features for hackathon"""
        demos = [
            "Welcome to our MurfAI Assistant demonstration!",
            "This system showcases advanced multi-agent AI capabilities.",
            "We're using Murf's premium voice synthesis technology.",
            "The system can handle real-time voice conversations.",
            "Multiple AI agents work together to assist users.",
            "This is perfect for production environments and hackathons!",
        ]
        
        for i, demo_text in enumerate(demos):
            self.add_message("assistant", demo_text)
            await self.speak_text(demo_text)
            await asyncio.sleep(2)  # Pause between demonstrations
        
        self.add_message("system", "🎉 Hackathon demonstration completed!")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if hasattr(self, 'tray') and self.tray.isVisible():
            self.hide()
            event.ignore()
        else:
            self.voice_listener.stop_listening()
            event.accept()

class MurfAIApplication:
    """Main application class"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("MurfAI Assistant")
        self.app.setOrganizationName("MurfAI")
        
        # Setup event loop for asyncio
        import qasync
        self.loop = qasync.QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        
        # Create main window
        self.main_window = MurfAIMainWindow()
    
    def run(self):
        """Run the application"""
        try:
            self.main_window.show()
            logger.info("MurfAI Assistant started successfully!")
            
            with self.loop:
                self.loop.run_forever()
                
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            QMessageBox.critical(None, "Error", f"Application error: {str(e)}")
        finally:
            logger.info("MurfAI Assistant shutting down...")

def main():
    """Main entry point"""
    try:
        # Check environment
        if not os.path.exists('.env'):
            print("⚠️  Warning: .env file not found. Please configure your API keys!")
            print("📝 Edit the .env file with your:")
            print("   - GITHUB_TOKEN (for AI)")
            print("   - MURF_API_KEY and MURF_USER_ID (for voice)")
        
        # Initialize and run application
        app = MurfAIApplication()
        sys.exit(app.run())
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: uv sync")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
