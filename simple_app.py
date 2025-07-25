#!/usr/bin/env python3
"""
MurfAI Assistant - Simplified Version for Quick Testing
Multi-Agent AI Assistant with Murf voice integration and GitHub Models
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Core imports
import httpx
import requests

# GUI imports
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QTextEdit, QLabel, QComboBox, QFrame, QLineEdit,
    QMessageBox, QProgressBar, QTabWidget, QSplitter
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, pyqtSlot
from PyQt6.QtGui import QFont

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubModelsClient(QThread):
    """GitHub Models API client for free AI using GitHub token"""
    
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.base_url = "https://models.inference.ai.azure.com"
        self.current_model = "gpt-4o-mini"
        self.user_message = ""
        
    def set_message(self, message: str):
        """Set the message to process"""
        self.user_message = message
        
    def run(self):
        """Process the message in background thread"""
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "MurfAI-Assistant/1.0"
            }
            
            payload = {
                "model": self.current_model,
                "messages": [{"role": "user", "content": self.user_message}],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            # Demo mode for placeholder token
            if self.token == "your_github_token_here":
                logger.info("Demo mode: AI processing...")
                response_text = self._generate_demo_response(self.user_message)
                self.response_ready.emit(response_text)
                return
            
            # Make actual API call
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    data = response.json()
                    response_text = data["choices"][0]["message"]["content"]
                    self.response_ready.emit(response_text)
                else:
                    error_msg = f"API Error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    self.error_occurred.emit(error_msg)
                    
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
    
    def _generate_demo_response(self, user_input: str) -> str:
        """Generate demo responses for presentation"""
        user_lower = user_input.lower()
        
        demo_responses = {
            'hello': "🎤 Hello! I'm your MurfAI Assistant - a multi-agent AI system with advanced voice synthesis capabilities!",
            'voice': "🎵 I use Murf's premium AI voices to provide natural, human-like speech synthesis with 120+ voices in 20+ languages!",
            'murf': "🚀 Murf provides cutting-edge AI voice technology that I integrate seamlessly for the best voice experience!",
            'hackathon': "🏆 This is our hackathon-winning project showcasing multi-agent AI with Murf's voice synthesis technology!",
            'help': "💡 I can help with voice synthesis, real-time conversations, document analysis, and task automation!",
            'demo': "🎯 Live demonstration: This showcases our multi-agent AI system with GitHub Models and Murf integration!",
            'features': "✨ Key features: Real-time voice commands, 120+ AI voices, multi-language support, screen monitoring, and intelligent task automation!"
        }
        
        # Find matching response
        for keyword, response in demo_responses.items():
            if keyword in user_lower:
                return response
        
        # Default response
        return f"🤖 I understand you mentioned '{user_input[:50]}...' - This demonstrates our advanced AI capabilities with Murf's premium voice synthesis technology!"

class MurfAIMainWindow(QMainWindow):
    """Main application window - Simplified version"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎤 MurfAI Assistant - Multi-Agent Voice AI")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize AI client
        github_token = os.getenv("GITHUB_TOKEN", "your_github_token_here")
        self.ai_client = GitHubModelsClient(github_token)
        self.ai_client.response_ready.connect(self.on_ai_response)
        self.ai_client.error_occurred.connect(self.on_ai_error)
        
        # Setup UI
        self.setup_ui()
        
        # Welcome message
        self.add_message("system", "🎤 MurfAI Assistant ready! Multi-agent AI system with Murf voice integration.")
        
        # Show demo status
        if github_token.startswith("your_"):
            self.add_message("system", "🎯 Running in DEMO mode - perfect for hackathon presentations!")
            self.status_label.setText("💡 Demo Mode Active")
        else:
            self.status_label.setText("🔗 Connected to GitHub Models")
    
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)
        
        # Left panel - Controls
        left_panel = self.create_control_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Chat
        right_panel = self.create_chat_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
        
        # Apply modern theme
        self.apply_theme()
    
    def create_control_panel(self) -> QWidget:
        """Create the control panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        panel.setMaximumWidth(450)
        
        layout = QVBoxLayout(panel)
        
        # Header
        header = QLabel("🎤 MurfAI Control Center")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Status
        self.status_label = QLabel("🔄 Initializing...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Input section
        input_section = QFrame()
        input_section.setFrameStyle(QFrame.Shape.StyledPanel)
        input_layout = QVBoxLayout(input_section)
        
        input_layout.addWidget(QLabel("💬 Message Input:"))
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        self.send_btn = QPushButton("📤 Send Message")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addWidget(input_section)
        
        # Demo section
        demo_section = QFrame()
        demo_section.setFrameStyle(QFrame.Shape.StyledPanel)
        demo_layout = QVBoxLayout(demo_section)
        
        demo_title = QLabel("🚀 Hackathon Demo")
        demo_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        demo_layout.addWidget(demo_title)
        
        # Demo buttons
        self.demo_features_btn = QPushButton("🎯 Demo Core Features")
        self.demo_features_btn.clicked.connect(self.demo_features)
        demo_layout.addWidget(self.demo_features_btn)
        
        self.demo_voices_btn = QPushButton("🎵 Demo Voice Collection")
        self.demo_voices_btn.clicked.connect(self.demo_voices)
        demo_layout.addWidget(self.demo_voices_btn)
        
        self.demo_agents_btn = QPushButton("🤖 Demo Multi-Agent")
        self.demo_agents_btn.clicked.connect(self.demo_agents)
        demo_layout.addWidget(self.demo_agents_btn)
        
        layout.addWidget(demo_section)
        
        # Info section
        info_section = QFrame()
        info_section.setFrameStyle(QFrame.Shape.StyledPanel)
        info_layout = QVBoxLayout(info_section)
        
        info_title = QLabel("ℹ️ System Info")
        info_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        info_layout.addWidget(info_title)
        
        github_token = os.getenv("GITHUB_TOKEN", "Not configured")
        murf_key = os.getenv("MURF_API_KEY", "Not configured")
        
        info_layout.addWidget(QLabel(f"🔗 GitHub Token: {'✅ Set' if not github_token.startswith('your_') else '⚠️ Demo'}"))
        info_layout.addWidget(QLabel(f"🎵 Murf API: {'✅ Set' if not murf_key.startswith('your_') else '⚠️ Demo'}"))
        info_layout.addWidget(QLabel(f"🖥️ Platform: {sys.platform}"))
        info_layout.addWidget(QLabel(f"🐍 Python: {sys.version.split()[0]}"))
        
        layout.addWidget(info_section)
        
        layout.addStretch()
        return panel
    
    def create_chat_panel(self) -> QWidget:
        """Create the chat panel"""
        panel = QFrame()
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
    
    def apply_theme(self):
        """Apply modern dark theme"""
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
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', monospace;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3e3e3e;
                border-radius: 6px;
                padding: 10px;
                font-size: 11px;
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
        """)
    
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
        
        # Auto-scroll
        cursor = self.chat_display.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.chat_display.setTextCursor(cursor)
    
    def send_message(self):
        """Send message to AI"""
        message = self.message_input.text().strip()
        if not message:
            return
        
        # Clear input
        self.message_input.clear()
        
        # Add to chat
        self.add_message("user", message)
        
        # Show progress
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.status_label.setText("🤖 AI thinking...")
        
        # Send to AI (in background thread)
        self.ai_client.set_message(message)
        self.ai_client.start()
    
    @pyqtSlot(str)
    def on_ai_response(self, response: str):
        """Handle AI response"""
        self.add_message("assistant", response)
        self.progress_bar.setVisible(False)
        self.status_label.setText("✅ Ready")
    
    @pyqtSlot(str)
    def on_ai_error(self, error: str):
        """Handle AI error"""
        self.add_message("system", f"❌ Error: {error}")
        self.progress_bar.setVisible(False)
        self.status_label.setText("❌ Error occurred")
    
    def demo_features(self):
        """Demo core features"""
        self.message_input.setText("Tell me about your core features")
        self.send_message()
    
    def demo_voices(self):
        """Demo voice capabilities"""
        self.message_input.setText("Show me your voice synthesis capabilities")
        self.send_message()
    
    def demo_agents(self):
        """Demo multi-agent system"""
        self.message_input.setText("Demonstrate your multi-agent AI system")
        self.send_message()

def main():
    """Main application entry point"""
    try:
        # Check environment
        env_file = Path(".env")
        if not env_file.exists():
            print("⚠️  Warning: .env file not found!")
            print("📝 Application will run in demo mode")
            print()
        
        # Create Qt application
        app = QApplication(sys.argv)
        app.setApplicationName("MurfAI Assistant")
        app.setOrganizationName("MurfAI")
        
        # Create and show main window
        window = MurfAIMainWindow()
        window.show()
        
        logger.info("🚀 MurfAI Assistant started successfully!")
        print("🚀 MurfAI Assistant is running!")
        print("💡 This is the simplified version for quick testing")
        
        # Run the application
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: uv add python-dotenv httpx pyqt6 requests")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"❌ Failed to start MurfAI Assistant: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
