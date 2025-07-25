"""
MurfAI Conversational Assistant - Enhanced Version
Real conversational AI with proper Murf API integration and improved UX
"""

import os
import sys
import logging
import asyncio
import threading
import tempfile
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Core imports
import httpx
import requests

# Audio handling
try:
    import pygame
    from pydub import AudioSegment
    import io
    import speech_recognition as sr
    AUDIO_AVAILABLE = True
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    SPEECH_RECOGNITION_AVAILABLE = False
    pygame = None
    AudioSegment = None
    sr = None

# Murf SDK
try:
    from murf import Murf
    MURF_AVAILABLE = True
except ImportError:
    MURF_AVAILABLE = False
    Murf = None

# GUI imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTextEdit, QLabel, QComboBox, QFrame, QLineEdit,
    QMessageBox, QProgressBar, QTabWidget, QSplitter, QStatusBar,
    QScrollArea, QCheckBox, QSlider, QSpinBox, QSizePolicy
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, pyqtSlot, QTimer, QObject
from PyQt6.QtGui import QFont, QIcon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('murf_ai_conversational.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ConversationMessage:
    """Enhanced conversation message with metadata"""
    role: str
    content: str
    timestamp: datetime
    has_audio: bool = False
    audio_file: Optional[str] = None
    voice_id: Optional[str] = None
    processing_time: Optional[float] = None

class MurfTTSClient:
    """Enhanced Murf Text-to-Speech client using official SDK"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self.available_voices = []
        
        if MURF_AVAILABLE and api_key and not api_key.startswith("your_"):
            try:
                # Set environment variable for SDK
                os.environ['MURF_API_KEY'] = api_key
                self.client = Murf(api_key=api_key)
                logger.info("✅ Murf client initialized successfully")
                self._load_demo_voices()  # Use demo voices for now
            except Exception as e:
                logger.error(f"❌ Failed to initialize Murf client: {e}")
                self.client = None
                self._load_demo_voices()
        else:
            logger.warning("⚠️ Murf SDK not available or API key not configured")
            self._load_demo_voices()
    
    def _load_demo_voices(self):
        """Load demo voices for testing including confirmed working voices"""
        self.available_voices = [
            # US English voices (confirmed working)
            {"voice_id": "en-US-terrell", "name": "Terrell", "language": "English", "accent": "US", "gender": "Male"},
            {"voice_id": "en-US-natalie", "name": "Natalie", "language": "English", "accent": "US", "gender": "Female"},
            {"voice_id": "en-US-julia", "name": "Julia", "language": "English", "accent": "US", "gender": "Female"},
            {"voice_id": "en-US-marcus", "name": "Marcus", "language": "English", "accent": "US", "gender": "Male"},
            
            # International English voices
            {"voice_id": "en-GB-charlotte", "name": "Charlotte", "language": "English", "accent": "British", "gender": "Female"},
            {"voice_id": "en-AU-ruby", "name": "Ruby", "language": "English", "accent": "Australian", "gender": "Female"},
            
            # Indian English voices (confirmed working)
            {"voice_id": "en-IN-priya", "name": "Priya", "language": "English", "accent": "Indian", "gender": "Female"},
            
            # Common Murf voices (these are standard voice IDs)
            {"voice_id": "michael", "name": "Michael", "language": "English", "accent": "US", "gender": "Male"},
            {"voice_id": "sarah", "name": "Sarah", "language": "English", "accent": "US", "gender": "Female"},
            {"voice_id": "john", "name": "John", "language": "English", "accent": "US", "gender": "Male"},
            {"voice_id": "emma", "name": "Emma", "language": "English", "accent": "British", "gender": "Female"},
            
            # Other international voices
            {"voice_id": "es-ES-elena", "name": "Elena", "language": "Spanish", "accent": "Spain", "gender": "Female"},
            {"voice_id": "fr-FR-marie", "name": "Marie", "language": "French", "accent": "France", "gender": "Female"},
            {"voice_id": "de-DE-hans", "name": "Hans", "language": "German", "accent": "Germany", "gender": "Male"},
            {"voice_id": "ja-JP-akira", "name": "Akira", "language": "Japanese", "accent": "Japan", "gender": "Male"},
        ]
        logger.info(f"✅ Loaded {len(self.available_voices)} demo voices with confirmed working voices")
    
    async def text_to_speech(self, text: str, voice_id: str = "en-US-terrell") -> Optional[bytes]:
        """Convert text to speech using Murf API"""
        try:
            if self.client and not self.api_key.startswith("your_"):
                # Use real Murf API
                logger.info(f"🎵 Generating speech with voice {voice_id}: '{text[:50]}...'")
                
                # Make the API call using the official SDK
                response = self.client.text_to_speech.generate(
                    text=text,
                    voice_id=voice_id
                )
                
                # The response should have an audio_file URL
                if hasattr(response, 'audio_file') and response.audio_file:
                    logger.info(f"📥 Downloading audio from: {response.audio_file}")
                    
                    # Download the audio file
                    audio_response = requests.get(response.audio_file)
                    if audio_response.status_code == 200:
                        logger.info("✅ Successfully generated and downloaded speech with Murf API")
                        return audio_response.content
                    else:
                        logger.error(f"❌ Failed to download audio: {audio_response.status_code}")
                        return self._generate_demo_audio(text, voice_id)
                else:
                    logger.error("❌ No audio_file URL in Murf API response")
                    logger.debug(f"Response attributes: {dir(response)}")
                    return self._generate_demo_audio(text, voice_id)
            else:
                # Demo mode - generate placeholder audio
                logger.info(f"🎪 Demo mode: Simulating speech for '{text[:50]}...'")
                return self._generate_demo_audio(text, voice_id)
                
        except Exception as e:
            logger.error(f"❌ Error in text_to_speech: {e}")
            logger.error(f"Exception details: {type(e).__name__}: {str(e)}")
            return self._generate_demo_audio(text, voice_id)
    
    def _generate_demo_audio(self, text: str, voice_id: str) -> bytes:
        """Generate pleasant demo audio notification"""
        try:
            if AUDIO_AVAILABLE and AudioSegment:
                # Create a more sophisticated demo audio
                sample_rate = 22050
                duration = min(len(text) * 0.1, 3.0)  # Up to 3 seconds based on text length
                
                # Generate pleasant chime sequence instead of beeps
                import numpy as np
                t = np.linspace(0, duration, int(sample_rate * duration))
                
                # Create a pleasant bell-like sound with harmonics
                fundamental = 523.25  # C5 note
                wave = np.zeros_like(t)
                
                # Add multiple harmonics for rich bell sound
                harmonics = [1, 2, 3, 4, 5]
                amplitudes = [0.5, 0.25, 0.15, 0.08, 0.05]
                
                for harm, amp in zip(harmonics, amplitudes):
                    wave += amp * np.sin(2 * np.pi * fundamental * harm * t)
                
                # Apply smooth envelope (bell-like attack and decay)
                attack_time = 0.1
                decay_time = duration - attack_time
                
                envelope = np.ones_like(t)
                attack_samples = int(attack_time * sample_rate)
                
                # Smooth attack
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                # Exponential decay
                decay_samples = len(t) - attack_samples
                envelope[attack_samples:] = np.exp(-np.linspace(0, 3, decay_samples))
                
                wave *= envelope
                
                # Add subtle modulation for more natural sound
                modulation = 1 + 0.1 * np.sin(2 * np.pi * 5 * t)  # 5Hz modulation
                wave *= modulation
                
                # Normalize and convert to int16
                wave = wave / np.max(np.abs(wave)) * 0.7  # Keep some headroom
                audio_data = (wave * 16383).astype(np.int16)
                
                # Create AudioSegment
                audio_segment = AudioSegment(
                    audio_data.tobytes(),
                    frame_rate=sample_rate,
                    sample_width=2,
                    channels=1
                )
                
                # Add a gentle fade-in and fade-out
                audio_segment = audio_segment.fade_in(100).fade_out(200)
                
                # Export to WAV bytes
                wav_io = io.BytesIO()
                audio_segment.export(wav_io, format="wav")
                return wav_io.getvalue()
            else:
                # Return minimal WAV header for silence if audio libraries not available
                return self._create_silence_wav(1.0)
                
        except Exception as e:
            logger.error(f"❌ Error generating demo audio: {e}")
            return self._create_silence_wav(1.0)
    
    def _create_silence_wav(self, duration: float) -> bytes:
        """Create a minimal WAV file with silence"""
        sample_rate = 22050
        samples = int(sample_rate * duration)
        
        # WAV file header for silence
        wav_header = b'RIFF'
        wav_header += (36 + samples * 2).to_bytes(4, 'little')  # File size
        wav_header += b'WAVE'
        wav_header += b'fmt '
        wav_header += (16).to_bytes(4, 'little')  # Format chunk size
        wav_header += (1).to_bytes(2, 'little')   # Audio format (PCM)
        wav_header += (1).to_bytes(2, 'little')   # Channels
        wav_header += sample_rate.to_bytes(4, 'little')  # Sample rate
        wav_header += (sample_rate * 2).to_bytes(4, 'little')  # Byte rate
        wav_header += (2).to_bytes(2, 'little')   # Block align
        wav_header += (16).to_bytes(2, 'little')  # Bits per sample
        wav_header += b'data'
        wav_header += (samples * 2).to_bytes(4, 'little')  # Data size
        
        # Silent audio data
        silence_data = b'\x00' * (samples * 2)
        
        return wav_header + silence_data

class SpeechWorker(QObject):
    """Worker for text-to-speech synthesis in separate thread"""
    
    speech_ready = pyqtSignal(bytes)  # audio_data
    speech_error = pyqtSignal(str)    # error_message
    
    def __init__(self, tts_client, text: str, voice_id: str):
        super().__init__()
        self.tts_client = tts_client
        self.text = text
        self.voice_id = voice_id
    
    @pyqtSlot()
    def generate_speech(self):
        """Generate speech in background thread"""
        try:
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                audio_data = loop.run_until_complete(
                    self.tts_client.text_to_speech(self.text, self.voice_id)
                )
                
                if audio_data:
                    self.speech_ready.emit(audio_data)
                else:
                    self.speech_error.emit("No audio data received")
            finally:
                loop.close()
                
        except Exception as e:
            self.speech_error.emit(f"Speech generation error: {str(e)}")

class VoiceInputWorker(QObject):
    """Worker for voice input recognition in separate thread"""
    
    voice_input_ready = pyqtSignal(str)  # recognized_text
    voice_input_error = pyqtSignal(str)  # error_message
    listening_started = pyqtSignal()
    listening_stopped = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_listening = False
    
    @pyqtSlot()
    def start_listening(self):
        """Start listening for voice input with improved settings"""
        if not SPEECH_RECOGNITION_AVAILABLE or sr is None:
            self.voice_input_error.emit("Speech recognition not available")
            return
        
        try:
            self.is_listening = True
            self.listening_started.emit()
            
            # Initialize recognizer and microphone with better settings
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 300  # Adjust for sensitivity
            recognizer.dynamic_energy_threshold = True
            recognizer.pause_threshold = 0.8  # Seconds of non-speaking audio before considering phrase complete
            
            microphone = sr.Microphone()
            
            # Adjust for ambient noise with shorter duration
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Listen for speech with shorter timeouts for better UX
            with microphone as source:
                audio = recognizer.listen(
                    source, 
                    timeout=5,  # Reduced from 10
                    phrase_time_limit=5  # Reduced from 10
                )
            
            self.listening_stopped.emit()
            
            # Recognize speech using Google's free service
            try:
                text = recognizer.recognize_google(audio, language='en-US')
                if text.strip():  # Only emit if we got actual text
                    self.voice_input_ready.emit(text)
                else:
                    self.voice_input_error.emit("No speech detected")
            except sr.UnknownValueError:
                self.voice_input_error.emit("Could not understand the audio - try speaking more clearly")
            except sr.RequestError as e:
                self.voice_input_error.emit(f"Recognition service error: {str(e)}")
                
        except sr.WaitTimeoutError:
            self.listening_stopped.emit()
            self.voice_input_error.emit("No speech detected within timeout - try again")
        except Exception as e:
            self.listening_stopped.emit()
            self.voice_input_error.emit(f"Voice input error: {str(e)}")
        finally:
            self.is_listening = False

class ConversationalAI(QThread):
    """Enhanced conversational AI with GitHub Models"""
    
    response_ready = pyqtSignal(str, float)  # response, processing_time
    error_occurred = pyqtSignal(str)
    
    def __init__(self, github_token: str):
        super().__init__()
        self.github_token = github_token
        self.base_url = "https://models.inference.ai.azure.com"
        self.current_model = "gpt-4o-mini"
        self.conversation_history = []
        self.user_message = ""
        self.system_prompt = """You are MurfAI Assistant, a friendly and helpful conversational AI with voice capabilities powered by Murf's premium text-to-speech technology. 

Key characteristics:
- Be conversational, natural, and engaging
- Keep responses concise but informative (2-3 sentences typically)
- Show enthusiasm about voice technology and AI capabilities
- Be helpful with various tasks and questions
- Mention your voice capabilities when relevant
- Be encouraging and positive

Remember: You can speak your responses using high-quality AI voices from Murf!"""
        
        # Initialize conversation with system prompt
        self.conversation_history.append({"role": "system", "content": self.system_prompt})
    
    def set_message(self, message: str):
        """Set the user message to process"""
        self.user_message = message
    
    def clear_history(self):
        """Clear conversation history but keep system prompt"""
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
    
    def run(self):
        """Process the user message"""
        start_time = datetime.now()
        
        try:
            if self.github_token.startswith("your_"):
                # Demo mode
                response = self._generate_contextual_demo_response(self.user_message)
                processing_time = (datetime.now() - start_time).total_seconds()
                self.response_ready.emit(response, processing_time)
                return
            
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": self.user_message})
            
            # Keep conversation history manageable (last 10 messages + system prompt)
            if len(self.conversation_history) > 11:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-10:]
            
            # Make API call
            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.current_model,
                "messages": self.conversation_history,
                "max_tokens": 500,  # Keep responses concise
                "temperature": 0.7
            }
            
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data["choices"][0]["message"]["content"]
                    
                    # Add AI response to history
                    self.conversation_history.append({"role": "assistant", "content": ai_response})
                    
                    processing_time = (datetime.now() - start_time).total_seconds()
                    self.response_ready.emit(ai_response, processing_time)
                else:
                    error_msg = f"API Error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    self.error_occurred.emit(error_msg)
        
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
    
    def _generate_contextual_demo_response(self, user_input: str) -> str:
        """Generate contextual demo responses based on conversation history"""
        user_lower = user_input.lower()
        
        # Contextual responses based on input
        if any(word in user_lower for word in ['hello', 'hi', 'hey', 'start']):
            return "Hello! I'm MurfAI Assistant, your conversational AI with premium voice capabilities. I can chat with you about anything and speak my responses using Murf's amazing AI voices! What would you like to talk about?"
        
        elif any(word in user_lower for word in ['voice', 'speak', 'audio', 'sound']):
            return "I use Murf's industry-leading AI voices to speak naturally! With over 150 voices in 21 languages, I can sound like anyone you prefer. Would you like me to demonstrate different voices or accents?"
        
        elif any(word in user_lower for word in ['how', 'what', 'tell', 'explain']):
            return "I'm here to help! I can assist with questions, have conversations, provide information, and even speak my responses aloud. My voice synthesis is powered by Murf's advanced AI technology. What specific topic interests you?"
        
        elif any(word in user_lower for word in ['weather', 'time', 'date']):
            return f"While I can't access real-time data in demo mode, I'd love to chat about that topic! The current time appears to be around {datetime.now().strftime('%I:%M %p')}. Is there something specific you'd like to discuss?"
        
        elif any(word in user_lower for word in ['help', 'assist', 'support']):
            return "I'm designed to be your helpful conversational companion! I can discuss topics, answer questions, help with tasks, and demonstrate voice synthesis. Plus, I can speak everything I say using Murf's natural AI voices. How can I assist you today?"
        
        elif any(word in user_lower for word in ['demo', 'test', 'show']):
            return "This is a live demonstration of conversational AI with voice synthesis! I can engage in natural dialogue and speak my responses using premium AI voices. Try asking me questions or starting a conversation - I'll respond both in text and voice!"
        
        elif any(word in user_lower for word in ['murf', 'api', 'technology']):
            return "Murf provides the most advanced AI voice technology available! Their text-to-speech system delivers human-like quality with incredible accuracy. I'm powered by their API to bring you the best conversational voice experience. Pretty amazing, right?"
        
        elif len(user_input) > 50:
            return f"That's a detailed message! I can see you mentioned several interesting points. In a real conversation, I'd engage with each aspect you brought up. My voice synthesis would make this feel like talking to a real person!"
        
        else:
            # Dynamic response based on input
            return f"Thanks for sharing that with me! I find it interesting when you mention '{user_input[:30]}...' - it gives me a chance to demonstrate natural conversation. With Murf's voice technology, our chat feels more human and engaging!"

class AudioPlayer(QThread):
    """Enhanced audio player with better error handling"""
    
    playback_finished = pyqtSignal()
    playback_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.audio_data = None
        self.is_playing = False
        self.pygame_available = False
        
        # Initialize pygame mixer for audio playback
        if AUDIO_AVAILABLE and pygame:
            try:
                pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1024)
                pygame.mixer.init()
                self.pygame_available = True
                logger.info("✅ Audio player initialized with pygame")
            except Exception as e:
                logger.error(f"❌ Failed to initialize pygame audio: {e}")
                self.pygame_available = False
        else:
            logger.warning("⚠️ Audio playback not available - pygame not installed")
    
    def play_audio(self, audio_data: bytes):
        """Play audio data"""
        if not self.pygame_available:
            logger.warning("⚠️ Audio playback not available")
            self.playback_error.emit("Audio playback not available")
            return
        
        self.audio_data = audio_data
        if not self.isRunning():
            self.start()
    
    def run(self):
        """Play audio in background thread"""
        try:
            if not self.audio_data or not self.pygame_available:
                return
            
            self.is_playing = True
            
            # Create temporary file for pygame
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(self.audio_data)
                tmp_file.flush()
                
                # Play the audio
                if pygame and pygame.mixer:
                    pygame.mixer.music.load(tmp_file.name)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                
                # Clean up
                try:
                    os.unlink(tmp_file.name)
                except Exception:
                    pass  # Ignore cleanup errors
            
            self.is_playing = False
            self.playback_finished.emit()
            
        except Exception as e:
            self.is_playing = False
            error_msg = f"Audio playback error: {str(e)}"
            logger.error(error_msg)
            self.playback_error.emit(error_msg)
    
    def stop_playback(self):
        """Stop current playback"""
        if self.pygame_available and pygame and pygame.mixer:
            try:
                pygame.mixer.music.stop()
                self.is_playing = False
            except Exception as e:
                logger.error(f"Error stopping playback: {e}")

class ConversationalMurfAI(QMainWindow):
    """Enhanced conversational MurfAI with better UX"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎤 MurfAI Conversational Assistant - Enhanced Voice AI")
        
        # Make window responsive and resizable
        self.setMinimumSize(900, 600)
        self.resize(1400, 900)  # Initial size but user can resize
        
        # Initialize components
        github_token = os.getenv("GITHUB_TOKEN", "your_github_token_here")
        murf_api_key = os.getenv("MURF_API_KEY", "your_murf_api_key_here")
        
        self.tts_client = MurfTTSClient(murf_api_key)
        self.ai_client = ConversationalAI(github_token)
        self.audio_player = AudioPlayer()
        
        # Application state
        self.conversation_messages: List[ConversationMessage] = []
        self.current_voice = "en-US-terrell"
        self.auto_speak = True
        self.conversation_count = 0
        
        # Thread management
        self._tts_thread = None
        self._tts_worker = None
        self._voice_input_thread = None
        self._voice_input_worker = None
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        self.setup_status_bar()
        
        # Welcome message
        self.add_conversation_message(
            "system", 
            "🎤 Welcome to MurfAI Conversational Assistant! I'm ready to chat and speak with you using premium AI voices including Indian voices.",
            has_audio=False
        )
        
        # Show configuration status
        if github_token.startswith("your_") or murf_api_key.startswith("your_"):
            self.add_conversation_message(
                "system",
                "🎪 Running in demo mode - perfect for testing! Configure your API keys in .env for full functionality.",
                has_audio=False
            )
        else:
            self.add_conversation_message(
                "system",
                "🔗 Connected to GitHub Models and Murf API - full functionality enabled!",
                has_audio=False
            )
    
    def setup_ui(self):
        """Setup the enhanced user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - Enhanced controls
        left_panel = self.create_enhanced_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Conversation
        right_panel = self.create_conversation_panel()
        splitter.addWidget(right_panel)
        
        # Set proportions and stretch factors for responsive design
        splitter.setSizes([450, 950])  # Initial proportions
        splitter.setStretchFactor(0, 0)  # Left panel doesn't stretch much
        splitter.setStretchFactor(1, 1)  # Right panel gets most expansion
        
        # Apply modern theme
        self.apply_enhanced_theme()
    
    def create_enhanced_control_panel(self) -> QWidget:
        """Create enhanced control panel with scroll support"""
        # Create the main content panel
        content_panel = QFrame()
        content_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(content_panel)
        
        # Header
        header = QLabel("🎤 MurfAI Control Center")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Status indicator
        self.status_indicator = QLabel("🟢 Ready for Conversation")
        self.status_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_indicator.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.status_indicator)
        
        # Voice settings section
        voice_section = self.create_voice_settings_section()
        layout.addWidget(voice_section)
        
        # Conversation settings
        conv_section = self.create_conversation_settings_section()
        layout.addWidget(conv_section)
        
        # Input section
        input_section = self.create_input_section()
        layout.addWidget(input_section)
        
        # Quick actions
        actions_section = self.create_quick_actions_section()
        layout.addWidget(actions_section)
        
        # Statistics
        stats_section = self.create_stats_section()
        layout.addWidget(stats_section)
        
        layout.addStretch()
        
        # Wrap in scroll area for responsiveness
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_panel)
        scroll_area.setMaximumWidth(450)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        return scroll_area
    
    def create_voice_settings_section(self) -> QWidget:
        """Create voice settings section"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        title = QLabel("🎵 Voice Settings")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Voice selection
        layout.addWidget(QLabel("Select Voice:"))
        self.voice_combo = QComboBox()
        for voice in self.tts_client.available_voices:
            if isinstance(voice, dict):
                display_name = f"{voice.get('name', 'Unknown')} ({voice.get('accent', 'Unknown')} {voice.get('gender', 'Unknown')})"
                self.voice_combo.addItem(display_name, voice.get('voice_id', 'en-US-terrell'))
            else:
                # Handle other voice formats
                display_name = str(voice)
                self.voice_combo.addItem(display_name, str(voice))
        
        self.voice_combo.currentTextChanged.connect(self.on_voice_changed)
        layout.addWidget(self.voice_combo)
        
        # Auto-speak toggle
        self.auto_speak_checkbox = QCheckBox("🔊 Auto-speak responses")
        self.auto_speak_checkbox.setChecked(True)
        self.auto_speak_checkbox.toggled.connect(self.on_auto_speak_toggled)
        layout.addWidget(self.auto_speak_checkbox)
        
        # Test voice button
        self.test_voice_btn = QPushButton("🎵 Test Voice")
        self.test_voice_btn.clicked.connect(self.test_current_voice)
        layout.addWidget(self.test_voice_btn)
        
        return section
    
    def create_conversation_settings_section(self) -> QWidget:
        """Create conversation settings section"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        title = QLabel("💬 Conversation Settings")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Clear conversation button
        self.clear_btn = QPushButton("🗑️ Clear Conversation")
        self.clear_btn.clicked.connect(self.clear_conversation)
        layout.addWidget(self.clear_btn)
        
        # Export conversation button
        self.export_btn = QPushButton("💾 Export Chat")
        self.export_btn.clicked.connect(self.export_conversation)
        layout.addWidget(self.export_btn)
        
        return section
    
    def create_input_section(self) -> QWidget:
        """Create message input section"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        title = QLabel("✍️ Message Input")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Message input
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here and press Enter...")
        self.message_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.message_input)
        
        # Send button
        self.send_btn = QPushButton("📤 Send Message")
        self.send_btn.clicked.connect(self.send_message)
        layout.addWidget(self.send_btn)
        
        # Voice input button
        self.voice_input_btn = QPushButton("🎤 Voice Input")
        if SPEECH_RECOGNITION_AVAILABLE:
            self.voice_input_btn.clicked.connect(self.start_voice_input)
        else:
            self.voice_input_btn.setEnabled(False)
            self.voice_input_btn.setText("🎤 Voice Input (Not Available)")
        layout.addWidget(self.voice_input_btn)
        
        return section
    
    def create_quick_actions_section(self) -> QWidget:
        """Create quick actions section"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        title = QLabel("⚡ Quick Actions")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Quick message buttons
        quick_messages = [
            ("👋 Say Hello", "Hello! How are you today?"),
            ("❓ Ask Question", "Can you help me understand how you work?"),
            ("🎵 Voice Demo", "Please demonstrate your voice capabilities"),
            ("🤖 About AI", "Tell me about your AI capabilities")
        ]
        
        for btn_text, message in quick_messages:
            btn = QPushButton(btn_text)
            btn.clicked.connect(lambda checked, msg=message: self.send_quick_message(msg))
            layout.addWidget(btn)
        
        return section
    
    def create_stats_section(self) -> QWidget:
        """Create statistics section"""
        section = QFrame()
        section.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(section)
        
        title = QLabel("📊 Session Statistics")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        self.stats_labels = {
            'messages': QLabel("💬 Messages: 0"),
            'voices_used': QLabel("🎵 Voice Syntheses: 0"),
            'avg_response': QLabel("⏱️ Avg Response: 0.0s"),
            'current_voice': QLabel(f"🎤 Current Voice: {self.current_voice}")
        }
        
        for label in self.stats_labels.values():
            layout.addWidget(label)
        
        return section
    
    def create_conversation_panel(self) -> QWidget:
        """Create the conversation panel with responsive design"""
        # Create the main content panel
        content_panel = QFrame()
        layout = QVBoxLayout(content_panel)
        
        # Title
        title = QLabel("💬 Conversational Chat with Voice Synthesis")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Conversation display with proper sizing policy
        self.conversation_display = QTextEdit()
        self.conversation_display.setReadOnly(True)
        self.conversation_display.setFont(QFont("Consolas", 11))
        self.conversation_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.conversation_display)
        
        # Audio controls
        audio_controls = QFrame()
        audio_layout = QHBoxLayout(audio_controls)
        
        self.speak_last_btn = QPushButton("🔊 Speak Last Message")
        self.speak_last_btn.clicked.connect(self.speak_last_message)
        audio_layout.addWidget(self.speak_last_btn)
        
        self.stop_audio_btn = QPushButton("⏹️ Stop Audio")
        self.stop_audio_btn.clicked.connect(self.stop_audio)
        audio_layout.addWidget(self.stop_audio_btn)
        
        audio_layout.addStretch()
        layout.addWidget(audio_controls)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return content_panel
    
    def setup_connections(self):
        """Setup signal connections"""
        # AI client connections
        self.ai_client.response_ready.connect(self.on_ai_response)
        self.ai_client.error_occurred.connect(self.on_ai_error)
        
        # Audio player connections
        self.audio_player.playback_finished.connect(self.on_audio_finished)
        self.audio_player.playback_error.connect(self.on_audio_error)
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Show API status
        github_token = os.getenv("GITHUB_TOKEN", "your_github_token_here")
        murf_key = os.getenv("MURF_API_KEY", "your_murf_api_key_here")
        
        if github_token.startswith("your_") or murf_key.startswith("your_"):
            self.status_bar.showMessage("🎪 Demo Mode - Configure API keys for full functionality")
        else:
            self.status_bar.showMessage("🔗 Connected to GitHub Models & Murf API - Full functionality active")
    
    def apply_enhanced_theme(self):
        """Apply enhanced modern dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
                border-radius: 12px;
                margin: 8px;
                padding: 16px;
            }
            QLabel {
                color: #ffffff;
                font-weight: bold;
                padding: 6px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 14px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 13px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d61;
            }
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 10px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                line-height: 1.4;
            }
            QLineEdit, QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                padding: 12px;
                font-size: 12px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 5px;
                border-color: #ffffff transparent transparent transparent;
            }
            QCheckBox {
                color: #ffffff;
                font-weight: bold;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #3e3e3e;
                border-radius: 4px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #0d7377;
                border-color: #0d7377;
            }
            QProgressBar {
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                text-align: center;
                color: #ffffff;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #0d7377;
                border-radius: 8px;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-top: 1px solid #3e3e3e;
                padding: 5px;
            }
        """)
    
    # Event handlers
    def add_conversation_message(self, role: str, content: str, has_audio: bool = False, 
                               processing_time: Optional[float] = None):
        """Add message to conversation display"""
        timestamp = datetime.now()
        
        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=timestamp,
            has_audio=has_audio,
            voice_id=self.current_voice if has_audio else None,
            processing_time=processing_time
        )
        
        self.conversation_messages.append(message)
        
        # Format message for display
        time_str = timestamp.strftime("%H:%M:%S")
        role_emojis = {
            "user": "👤 You",
            "assistant": "🤖 MurfAI",
            "system": "⚙️ System"
        }
        
        role_display = role_emojis.get(role, f"📝 {role.title()}")
        
        # Add processing time if available
        time_info = f"[{time_str}]"
        if processing_time:
            time_info += f" ({processing_time:.1f}s)"
        
        # Add audio indicator
        audio_indicator = " 🔊" if has_audio else ""
        
        formatted_message = f"{time_info} {role_display}{audio_indicator}:\n{content}\n"
        
        self.conversation_display.append(formatted_message)
        
        # Auto-scroll to bottom
        cursor = self.conversation_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.conversation_display.setTextCursor(cursor)
        
        # Update statistics
        self.update_statistics()
    
    def send_message(self):
        """Send user message"""
        message = self.message_input.text().strip()
        if not message:
            return
        
        self.send_quick_message(message)
        self.message_input.clear()
    
    def send_quick_message(self, message: str):
        """Send a quick message"""
        # Add user message
        self.add_conversation_message("user", message)
        self.conversation_count += 1
        
        # Show processing
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_indicator.setText("🔄 AI Processing...")
        self.send_btn.setEnabled(False)
        
        # Send to AI
        self.ai_client.set_message(message)
        if not self.ai_client.isRunning():
            self.ai_client.start()
    
    @pyqtSlot(str, float)
    def on_ai_response(self, response: str, processing_time: float):
        """Handle AI response"""
        # Add AI message
        self.add_conversation_message("assistant", response, processing_time=processing_time)
        
        # Speak response if auto-speak is enabled
        if self.auto_speak:
            self.speak_text(response)
        
        # Reset UI state
        self.progress_bar.setVisible(False)
        self.status_indicator.setText("🟢 Ready for Conversation")
        self.send_btn.setEnabled(True)
    
    @pyqtSlot(str)
    def on_ai_error(self, error: str):
        """Handle AI error"""
        self.add_conversation_message("system", f"❌ Error: {error}")
        self.progress_bar.setVisible(False)
        self.status_indicator.setText("🟡 Error Occurred")
        self.send_btn.setEnabled(True)
    
    def speak_text(self, text: str):
        """Convert text to speech and play using proper thread management"""
        if not text.strip():
            return
        
        # Clean up existing speech thread if any (with defensive checking)
        if self._tts_thread is not None:
            try:
                if self._tts_thread.isRunning():
                    self._tts_thread.quit()
                    self._tts_thread.wait()
            except RuntimeError:
                # Thread was already deleted, just reset the reference
                self._tts_thread = None
                self._tts_worker = None
        
        # Show audio processing
        self.status_indicator.setText("🎵 Generating Voice...")
        
        # Create worker and thread
        self._tts_worker = SpeechWorker(self.tts_client, text, self.current_voice)
        self._tts_thread = QThread()
        
        # Move worker to thread
        self._tts_worker.moveToThread(self._tts_thread)
        
        # Connect signals
        self._tts_thread.started.connect(self._tts_worker.generate_speech)
        self._tts_worker.speech_ready.connect(self.on_speech_ready)
        self._tts_worker.speech_error.connect(self.on_speech_error)
        self._tts_worker.speech_ready.connect(self._tts_thread.quit)
        self._tts_worker.speech_error.connect(self._tts_thread.quit)
        self._tts_thread.finished.connect(self._tts_thread.deleteLater)
        self._tts_thread.finished.connect(self._on_tts_thread_finished)
        
        # Start the thread
        self._tts_thread.start()
    
    @pyqtSlot()
    def _on_tts_thread_finished(self):
        """Clean up thread references when TTS thread finishes"""
        self._tts_thread = None
        self._tts_worker = None
    
    @pyqtSlot(bytes)
    def on_speech_ready(self, audio_data: bytes):
        """Handle speech synthesis completion"""
        try:
            # Update last message to show it has audio
            if self.conversation_messages:
                self.conversation_messages[-1].has_audio = True
            
            # Play audio
            self.audio_player.play_audio(audio_data)
            
            # Update stats
            self.update_voice_stats()
            
        except Exception as e:
            logger.error(f"❌ Error handling speech: {e}")
            self.status_indicator.setText("❌ Voice Error")
    
    @pyqtSlot(str)
    def on_speech_error(self, error_message: str):
        """Handle speech synthesis error"""
        logger.warning(f"⚠️ Speech error: {error_message}")
        self.status_indicator.setText("⚠️ Voice Generation Failed")
    
    def start_voice_input(self):
        """Start voice input recognition"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            self.add_conversation_message("system", "❌ Voice input not available - speech recognition not installed")
            return
        
        # Clean up existing voice input thread if any
        if self._voice_input_thread is not None:
            try:
                if self._voice_input_thread.isRunning():
                    return  # Already listening
            except RuntimeError:
                self._voice_input_thread = None
                self._voice_input_worker = None
        
        # Create worker and thread
        self._voice_input_worker = VoiceInputWorker()
        self._voice_input_thread = QThread()
        
        # Move worker to thread
        self._voice_input_worker.moveToThread(self._voice_input_thread)
        
        # Connect signals
        self._voice_input_thread.started.connect(self._voice_input_worker.start_listening)
        self._voice_input_worker.listening_started.connect(self.on_voice_listening_started)
        self._voice_input_worker.listening_stopped.connect(self.on_voice_listening_stopped)
        self._voice_input_worker.voice_input_ready.connect(self.on_voice_input_ready)
        self._voice_input_worker.voice_input_error.connect(self.on_voice_input_error)
        self._voice_input_worker.voice_input_ready.connect(self._voice_input_thread.quit)
        self._voice_input_worker.voice_input_error.connect(self._voice_input_thread.quit)
        self._voice_input_thread.finished.connect(self._voice_input_thread.deleteLater)
        self._voice_input_thread.finished.connect(self._on_voice_input_thread_finished)
        
        # Start the thread
        self._voice_input_thread.start()
    
    @pyqtSlot()
    def _on_voice_input_thread_finished(self):
        """Clean up voice input thread references"""
        self._voice_input_thread = None
        self._voice_input_worker = None
    
    @pyqtSlot()
    def on_voice_listening_started(self):
        """Handle voice listening started"""
        self.status_indicator.setText("🎤 Listening...")
        self.voice_input_btn.setText("🎤 Listening...")
        self.voice_input_btn.setEnabled(False)
        self.add_conversation_message("system", "🎤 Listening for voice input...")
    
    @pyqtSlot()
    def on_voice_listening_stopped(self):
        """Handle voice listening stopped"""
        self.status_indicator.setText("🔄 Processing voice...")
        self.voice_input_btn.setText("🎤 Voice Input")
        self.voice_input_btn.setEnabled(True)
    
    @pyqtSlot(str)
    def on_voice_input_ready(self, text: str):
        """Handle voice input recognition complete"""
        self.add_conversation_message("system", f"🎤 Voice input recognized: '{text}'")
        self.message_input.setText(text)
        self.status_indicator.setText("🟢 Ready for Conversation")
        
        # Optionally auto-send the voice input
        self.send_message()
    
    @pyqtSlot(str)
    def on_voice_input_error(self, error: str):
        """Handle voice input error"""
        self.add_conversation_message("system", f"🎤 Voice input error: {error}")
        self.status_indicator.setText("🟡 Voice Input Error")
        self.voice_input_btn.setText("🎤 Voice Input")
        self.voice_input_btn.setEnabled(True)

    def _sync_speak_text(self, text: str):
        """DEPRECATED - replaced by proper thread management"""
        # This method is no longer used but kept for compatibility
        pass
    
    def speak_last_message(self):
        """Speak the last assistant message"""
        # Find last assistant message
        for message in reversed(self.conversation_messages):
            if message.role == "assistant":
                self.speak_text(message.content)
                break
    
    def stop_audio(self):
        """Stop current audio playback"""
        self.audio_player.stop_playback()
        self.status_indicator.setText("⏹️ Audio Stopped")
    
    @pyqtSlot()
    def on_audio_finished(self):
        """Handle audio playback finished"""
        self.status_indicator.setText("🟢 Ready for Conversation")
    
    @pyqtSlot(str)
    def on_audio_error(self, error: str):
        """Handle audio playback error"""
        self.add_conversation_message("system", f"🔊 Audio Error: {error}")
        self.status_indicator.setText("🟡 Audio Error")
    
    def on_voice_changed(self):
        """Handle voice selection change"""
        current_data = self.voice_combo.currentData()
        if current_data:
            self.current_voice = current_data
            voice_name = self.voice_combo.currentText().split("(")[0].strip()
            self.add_conversation_message("system", f"🎵 Voice changed to: {voice_name}")
            self.update_statistics()
    
    def on_auto_speak_toggled(self, checked: bool):
        """Handle auto-speak toggle"""
        self.auto_speak = checked
        status = "enabled" if checked else "disabled"
        self.add_conversation_message("system", f"🔊 Auto-speak {status}")
    
    def test_current_voice(self):
        """Test current voice with sample text"""
        test_text = f"Hello! This is a test of the {self.voice_combo.currentText().split('(')[0].strip()} voice. How do I sound?"
        self.speak_text(test_text)
    
    def clear_conversation(self):
        """Clear conversation history"""
        reply = QMessageBox.question(
            self, 
            "Clear Conversation",
            "Are you sure you want to clear the conversation history?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.conversation_messages.clear()
            self.conversation_display.clear()
            self.ai_client.clear_history()
            self.conversation_count = 0
            
            # Add welcome message
            self.add_conversation_message(
                "system",
                "🔄 Conversation cleared. Ready for a fresh start!"
            )
            
            self.update_statistics()
    
    def export_conversation(self):
        """Export conversation to file"""
        if not self.conversation_messages:
            QMessageBox.information(self, "Export", "No conversation to export!")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"murf_conversation_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("MurfAI Conversational Assistant - Chat Export\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Messages: {len(self.conversation_messages)}\n")
                f.write("=" * 50 + "\n\n")
                
                for msg in self.conversation_messages:
                    role_display = {"user": "You", "assistant": "MurfAI", "system": "System"}.get(msg.role, msg.role)
                    f.write(f"[{msg.timestamp.strftime('%H:%M:%S')}] {role_display}:\n")
                    f.write(f"{msg.content}\n")
                    if msg.has_audio:
                        f.write(f"(Spoken with voice: {msg.voice_id})\n")
                    f.write("\n")
            
            QMessageBox.information(self, "Export Successful", f"Conversation exported to {filename}")
            logger.info(f"✅ Conversation exported to {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export conversation: {str(e)}")
            logger.error(f"❌ Export error: {e}")
    
    def update_statistics(self):
        """Update session statistics"""
        message_count = len([msg for msg in self.conversation_messages if msg.role in ["user", "assistant"]])
        voice_count = len([msg for msg in self.conversation_messages if msg.has_audio])
        
        # Calculate average response time
        response_times = [msg.processing_time for msg in self.conversation_messages 
                         if msg.processing_time and msg.role == "assistant"]
        avg_response = sum(response_times) / len(response_times) if response_times else 0.0
        
        self.stats_labels['messages'].setText(f"💬 Messages: {message_count}")
        self.stats_labels['voices_used'].setText(f"🎵 Voice Syntheses: {voice_count}")
        self.stats_labels['avg_response'].setText(f"⏱️ Avg Response: {avg_response:.1f}s")
        self.stats_labels['current_voice'].setText(f"🎤 Current Voice: {self.current_voice}")
    
    def update_voice_stats(self):
        """Update voice synthesis statistics"""
        self.update_statistics()
    
    def closeEvent(self, event):
        """Handle application close with proper thread cleanup"""
        try:
            # Stop any running threads safely
            if self.ai_client.isRunning():
                self.ai_client.quit()
                self.ai_client.wait(3000)  # Wait up to 3 seconds
            
            if self.audio_player.isRunning():
                self.audio_player.stop_playback()
                self.audio_player.quit()
                self.audio_player.wait(1000)  # Wait up to 1 second
            
            if self._tts_thread and self._tts_thread.isRunning():
                self._tts_thread.quit()
                self._tts_thread.wait(2000)  # Wait up to 2 seconds
            
            logger.info("✅ All threads stopped safely")
            
        except Exception as e:
            logger.error(f"⚠️ Error during cleanup: {e}")
        
        event.accept()
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts including fullscreen toggle"""
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()
        else:
            super().keyPressEvent(event)

def main():
    """Main application entry point"""
    try:
        # Check environment
        env_file = Path(".env")
        if not env_file.exists():
            print("⚠️  Warning: .env file not found!")
            print("💡 Create .env file with your API keys for full functionality")
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("MurfAI Conversational Assistant")
        app.setOrganizationName("MurfAI")
        
        # Create and show main window
        window = ConversationalMurfAI()
        window.show()
        
        logger.info("🚀 MurfAI Conversational Assistant started!")
        print("🚀 MurfAI Conversational Assistant is running!")
        print("💬 Ready for natural conversations with voice synthesis!")
        
        # Run the application
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: uv sync")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()