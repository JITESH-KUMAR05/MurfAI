# 🤖 Go To Buddy - AI-Powered Desktop Assistant

## 🚀 Your Intelligent Personal Assistant with Premium Voice Technology

I've created Go To Buddy as a sophisticated desktop application that serves as your personal AI assistant, featuring **premium voice synthesis**, **intelligent conversation capabilities**, and **seamless system automation**. I built it with modern Python technologies and designed it for productivity enhancement.

## ✨ Current Status: Production Ready

- ✅ **Intelligent AI Assistant** - Context-aware conversations and task assistance
- ✅ **Multi-Language Support** - Fluent English and Hindi communication
- ✅ **Premium Voice Experience** - High-quality text-to-speech with multiple voice options
- ✅ **System Integration** - Direct control of applications and system functions
- ✅ **Smart Voice Detection** - Automatic language recognition and voice switching
- ✅ **Modern Interface** - Professional desktop application with intuitive design
- ✅ **Cross-Platform** - Works on Linux, Windows, and macOS

## 🌟 Key Features

### 🧠 **Intelligent Conversation Engine**
- **Contextual Understanding** - Maintains conversation history and context awareness
- **Bilingual Communication** - Seamless English and Hindi language support
- **Natural Language Processing** - Understands commands in conversational language
- **Personality-Driven Responses** - Friendly, helpful, and engaging interaction style

### 🎵 **Premium Voice Experience**
- **High-Quality Voice Synthesis** - Powered by Murf's advanced text-to-speech technology
- **Multiple Voice Options** - Choose from professional voices in different accents
- **Smart Voice Switching** - Automatic voice selection based on detected language
- **Real-Time Audio** - Instant voice responses with natural speech patterns

### 🔧 **System Automation & Control**
- **Application Management** - Launch Chrome, Gmail, text editors, and system tools
- **Web Search Integration** - Direct Google and YouTube search capabilities
- **File Operations** - Screenshot capture, text input automation, clipboard management
- **Cross-Platform Compatibility** - Consistent experience across operating systems

### 💬 **Interactive Communication Examples**

```
👤 User: "Good morning! How can you help me today?"
🤖 Go To Buddy: "Good morning! I'm here to assist you. I can help you open applications, 
              search the web, manage tasks, or just have a conversation. What would you like to do?"

👤 User: "Open Chrome please"  
🤖 Go To Buddy: [Opens Chrome] "Chrome browser opened successfully! Ready for browsing! 🌐"

👤 User: "Search for Python programming tutorials"
🤖 Go To Buddy: [Opens Google search] "Searching for Python tutorials. Happy learning! 📚"
```

## 🛠️ Technical Architecture

### 🎯 **Core Technologies**
- **Language Processing** - Advanced language detection and response generation
- **Voice Technology** - Premium text-to-speech with natural voice synthesis  
- **System Integration** - Direct application control and automation capabilities
- **Modern UI Framework** - Responsive PyQt6 desktop interface

### 🎮 **System Capabilities**
- **Application Launcher** - Chrome, Gmail, text editors, calculator, file manager
- **Web Integration** - Google Search, YouTube, direct website access
- **Automation Features** - Text typing, clipboard operations, screenshot capture
- **Multi-Platform Support** - Windows, macOS, Linux compatibility
- **Voice Input** - Speech-to-text for hands-free operation

### 🎵 **Advanced Voice Features**
- **Multi-Language Voices** - English, Hindi, and international voice options
- **Real-Time Synthesis** - Natural human-like voice quality
- **Accent Variety** - US, UK, Australian, and Indian accent support
- **Voice Customization** - User-selectable voice preferences

### 💻 **Modern Desktop Experience**
- **Professional Interface** - Clean, intuitive dark theme design
- **Real-Time Chat** - Conversation history with timestamps
- **Responsive Design** - Adapts to different screen sizes and resolutions
- **Fullscreen Support** - F11 for immersive interaction experience

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.11+** (Python 3.13 recommended for optimal performance)
- **Modern Package Manager** - uv for fast dependency management
- **Audio Hardware** - Microphone for voice input, speakers for audio output
- **Internet Connection** - For AI services and voice synthesis

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JITESH-KUMAR05/MurfAI.git
   cd MurfAI
   ```

2. **Install Dependencies**
   ```bash
   # Install uv package manager if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install all project dependencies
   uv sync
   ```

3. **Environment Configuration**
   ```bash
   # Copy the environment template
   cp .env.example .env
   
   # Edit the configuration file with your API keys
   nano .env
   ```

4. **Configure API Access**
   ```env
   # GitHub Models API (Free AI conversation engine)
   GITHUB_TOKEN=your_github_personal_access_token
   
   # Murf API Key (Premium voice synthesis)
   MURF_API_KEY=your_murf_api_key
   ```

5. **Launch the Application**
   ```bash
   uv run python conversational_murf_ai.py
   ```

## 🔧 Configuration & Setup

### API Keys Setup

#### GitHub Token (Free AI Engine)
1. Visit [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Create a new token with `repo` and `user` permissions
3. Copy the generated token to `GITHUB_TOKEN` in your `.env` file

#### Murf API Key (Premium Voice)
1. Create an account at [Murf.ai](https://murf.ai)
2. Navigate to API settings in your dashboard
3. Generate an API key and add it to `MURF_API_KEY` in your `.env` file

**Note**: I've included a demo mode that works without API keys for testing purposes.

## 🎵 Available Voice Options

### 🇺🇸 **English Voices**
- **Terrell** (Male) - Professional, clear articulation
- **Naomi** (Female) - Warm, conversational tone
- **Charles** (Male) - Authoritative, business-appropriate
- **Alicia** (Female) - Friendly, engaging style

### 🇮🇳 **Indian Voices**
- **Priya** (Female) - Natural Indian English accent
- **Aarav** (Male) - Professional Indian English
- **Ayushi** (Female, Hindi) - Native Hindi speaker
- **Amit** (Male, Hindi) - Clear Hindi pronunciation

### 🌍 **International Options**
- **Hazel** (British Female) - Classic British accent
- **Kylie** (Australian Female) - Australian English
- **Evelyn** (Australian Female) - Alternative Australian voice

## 💻 Usage Instructions

### Basic Operation

1. **Starting Conversations**
   - Type messages in the input field and press Enter
   - Click the "Send Message" button
   - Receive both text and voice responses

2. **Voice Input**
   - Click the "🎤 Voice Input" button
   - Speak clearly when the listening indicator appears
   - Your speech is automatically converted to text

3. **Voice Controls**
   - Toggle "Auto-speak responses" for automatic voice output
   - Use "Test Voice" to preview the selected voice
   - "Speak Last Message" repeats the most recent response

### Advanced Features

4. **Voice Management**
   - Select different voices from the settings dropdown
   - Enable/disable automatic voice switching based on language
   - Test voices before using them in conversations

5. **Window Management**
   - **F11** - Toggle fullscreen mode for immersive experience
   - **Escape** - Exit fullscreen mode
   - Resize windows by dragging corners or edges
   - Use maximize button for full-screen operation

6. **Conversation Management**
   - "Clear Conversation" - Start fresh conversations
   - "Export Chat" - Save conversation history to files
   - View session statistics and performance metrics

## 🔊 System Requirements & Audio Setup

### Hardware Requirements
- **CPU**: Multi-core processor (2.0 GHz or higher recommended)
- **RAM**: 4GB minimum, 8GB recommended for optimal performance
- **Storage**: 500MB for application and dependencies
- **Audio**: Microphone and speakers/headphones for full functionality

### Audio Configuration (Linux)
```bash
# Test microphone functionality
arecord -l                    # List available audio devices
arecord -d 3 test.wav        # Record a 3-second test sample

# Configure audio permissions
sudo usermod -a -G audio $USER  # Add user to audio group
```

### Common Audio Solutions

| Issue | Resolution |
|-------|------------|
| Microphone not detected | Check USB connections and system permissions |
| ALSA library warnings | Install `libasound2-dev` package |
| Voice input timeout | Reduce background noise, speak clearly |
| No audio output | Verify speaker connections and volume settings |

## 🛠️ Development Information

### Project Architecture
```
Go To Buddy/
├── conversational_murf_ai.py  # Main application entry point
├── pyproject.toml            # Modern Python project configuration
├── .env.example             # Environment variables template
├── requirements.txt         # Legacy dependency list
├── README.md               # This documentation file
└── uv.lock                # Dependency version lock file
```

### Core Components

#### Application Classes
- **`ConversationalMurfAI`** - Main application window and user interface
- **`MurfTTSClient`** - Murf API integration for voice synthesis
- **`VoiceInputWorker`** - Speech recognition processing in background threads
- **`ConversationalAI`** - GitHub Models API integration for AI responses
- **`AudioPlayer`** - Audio playback management and control
- **`SpeechWorker`** - Text-to-speech processing and synthesis

#### Threading Architecture
- **Main Thread** - User interface and event handling
- **AI Processing Thread** - GitHub Models API communication
- **Voice Synthesis Thread** - Murf text-to-speech processing
- **Speech Recognition Thread** - Voice input processing
- **Audio Playback Thread** - Audio output management

### Technology Stack

- **🐍 Python 3.11+** - Modern Python with latest language features
- **🎵 Murf AI SDK** - Premium voice synthesis technology
- **🤖 GitHub Models API** - Free AI conversation engine
- **💻 PyQt6** - Modern cross-platform GUI framework
- **📦 uv** - Fast, modern Python package manager
- **🔄 asyncio** - Asynchronous programming for responsive performance

## 🐛 Troubleshooting Guide

### Common Installation Issues

**1. Dependency Problems**
```bash
# Update dependencies
uv sync

# Check Python version compatibility
python --version  # Should be 3.11 or higher
```

**2. API Connection Issues**
```bash
# Test GitHub token validity
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/user

# Verify Murf API key in dashboard
```

**3. Audio System Problems**
```bash
# Linux audio system setup
sudo apt install python3-pyaudio portaudio19-dev
pip install --upgrade pyaudio pygame

# Test audio functionality
python -c "import pygame; pygame.mixer.init(); print('Audio system OK')"
```

**4. Voice Input Issues**
- Ensure microphone permissions are granted
- Test in a quiet environment
- Speak clearly and at normal volume
- Try different microphone hardware if available

**5. Display and UI Issues**
- Update PyQt6: `uv add "PyQt6>=6.6"`
- Check display manager settings
- Try fullscreen mode (F11) for better experience

### Debug Mode
```bash
# Run with detailed logging
PYTHONPATH=. uv run python conversational_murf_ai.py --debug
```

### Log File Analysis
- Application logs are saved to: `murf_ai_conversational.log`
- Check for API response errors and system issues

## 📊 Performance Optimization

### Voice Synthesis Performance
- Use shorter text segments for faster processing
- Cache frequently used responses locally
- Select faster-processing voices when speed is priority

### Speech Recognition Optimization
- Use high-quality microphone equipment
- Maintain consistent 6-12 inch microphone distance
- Minimize background noise and echo
- Speak at normal, clear pace

### System Performance
- Close unnecessary background applications
- Enable hardware acceleration when available
- Consider system resource allocation for large conversations

## 🔐 Privacy & Security

### Data Protection
- All conversations are stored locally only
- Voice data is processed in memory without persistent storage
- No personal data is transmitted to third parties
- Clear sensitive conversations after use when needed

### API Security
- Store API keys in environment variables only
- Never commit credentials to version control systems
- Rotate API keys regularly for enhanced security
- Use minimal required permissions for API tokens

### Network Security
- All API communications use HTTPS encryption
- Tokens are transmitted securely with proper headers
- No data sharing with unauthorized services

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for complete details.

## 🙏 Acknowledgments

### Core Technologies
- **[Murf.ai](https://murf.ai)** - Advanced voice synthesis platform
- **[GitHub Models](https://github.com/marketplace/models)** - AI conversation capabilities
- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Modern GUI framework
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** - Voice input processing
- **[pygame](https://www.pygame.org/)** - Audio playback functionality
- **[uv](https://github.com/astral-sh/uv)** - Modern Python package management

### Development Support
- OpenAI and GitHub for providing accessible AI model APIs
- Murf development team for excellent voice synthesis technology
- Python community for comprehensive library ecosystem

## 📞 Support & Contact

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/JITESH-KUMAR05/MurfAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JITESH-KUMAR05/MurfAI/discussions)

### Documentation Resources
- **Murf API**: [Official Murf Documentation](https://docs.murf.ai)
- **GitHub Models**: [GitHub Models Documentation](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api)
- **PyQt6**: [PyQt6 Framework Documentation](https://doc.qt.io/qtforpython/)

---

**Developed by [Jitesh](https://github.com/JITESH-KUMAR05)**

*Enhance your productivity with AI-powered assistance and natural voice interaction!*

## 🚀 Ready to Use!

Your Go To Buddy assistant is ready for deployment and daily use. Start the application with:

```bash
uv run python conversational_murf_ai.py
```

Experience the future of desktop AI assistance! 🤖✨
