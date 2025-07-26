# 🎤 MurfAI JARVIS - Advanced Indian AI Assistant

## 🚀 Next-Generation AI Assistant with Premium Indian Voices

A revolutionary desktop application that transforms your computer into a **smart Indian AI assistant** combining **Murf AI's premium Indian voices** with **advanced AI capabilities** and **system automation** - your personal JARVIS!

## ✅ Status: ENHANCED & READY

- ✅ **JARVIS Personality** - Smart, warm, Indian AI assistant
- ✅ **Advanced Hindi/English** - Seamless bilingual conversations
- ✅ **Premium Indian Voices** - Aditi, Rohan (Hindi), Priya, Kabir, Aarav (Indian English)
- ✅ **System Command Execution** - Open apps, search, control your PC
- ✅ **Smart Voice Switching** - Auto-detects language & switches voice
- ✅ **Modern UI Enhanced** - Better user experience
- ✅ **Cross-Platform Ready** - Linux/Windows/macOS

## 🌟 JARVIS Features

### � **Intelligent Conversations**
- **Bilingual Mastery**: Fluent Hindi (हिंदी) and Indian English
- **Context Awareness**: Remembers conversation history and builds relationships
- **Cultural Intelligence**: Uses Indian expressions naturally ("acha", "bilkul", "theek hai")
- **Emotion Recognition**: Responds with appropriate tone and personality

### 🎵 **Premium Indian Voice Experience**
- **Hindi Voices**: Aditi (Female), Rohan (Male) - Pure Hindi accent
- **Indian English**: Priya, Kabir, Aarav - Natural Indian English
- **Smart Detection**: Automatically switches voice based on your language
- **Premium Quality**: Murf's industry-leading voice synthesis

### 🚀 **System Command Execution**
- **App Control**: "Chrome kholo", "Gmail kholo", "Notepad kholo"
- **Web Search**: "Python tutorials search karo"
- **File Operations**: Screenshots, text typing, clipboard management
- **Smart Actions**: Detects commands and executes automatically

### 💬 **Natural Conversation Examples**

```
👤 User: "Hi Jitesh, aap kaise ho?"
🤖 JARVIS: "Namaste Jitesh! Main bilkul perfect hoon. Aap kaise hain? Kya madad chahiye?" 
          (Auto-switches to Aditi Hindi voice)

👤 User: "Chrome kholo please"  
🤖 JARVIS: [Opens Chrome] "Chrome browser khol diya! Ready for browsing! 🌐"
          (Executes system command + friendly response)

👤 User: "Search Python tutorials"
🤖 JARVIS: [Opens Google search] "Python tutorials search kar diya! Happy learning! 📚"
          (Uses Kabir voice for commands)
```

## 🛠️ **Enhanced Architecture**

### 🎯 **Smart Language Processing**
- **Language Detection**: Auto-detects Hindi, English, and Hinglish
- **Voice Matching**: Automatically selects appropriate Indian voice
- **Cultural Context**: Understands Indian conversation patterns
- **Action Recognition**: Extracts commands from natural language

### 🎮 **System Integration**
- **App Launcher**: Chrome, Gmail, Notepad, Calculator, File Explorer
- **Web Integration**: Google Search, YouTube Search, Website opening
- **Automation**: Text typing, clipboard operations, screenshots
- **Cross-Platform**: Windows, macOS, Linux support  
- **UI Agent**: Modern PyQt6 desktop interface with dark theme
- **Coordination Agent**: Seamless inter-agent communication

### 🎵 Advanced Voice Capabilities  
- **130+ Premium Voices** across 21 languages
- **Real-time voice synthesis** with natural human-like quality
- **Multi-language support** including English, Spanish, French, German, Japanese, Chinese, Hindi
- **Accent variety** covering US, UK, Australian, and regional accents

### 💻 Modern Desktop Experience
- **PyQt6 GUI** with professional dark theme
- **Real-time chat interface** with conversation history
- **System tray integration** for background operation
- **Cross-platform compatibility** (Windows, macOS, Linux)

### 🚀 Production-Ready Architecture
- **Async/await patterns** for optimal performance
- **Error handling and logging** for reliability
- **Environment configuration** with .env support
- **Modern dependency management** with uv package manager

## 🛠️ Technology Stack

- **� Python 3.11+** - Modern Python with latest features
- **🎵 Murf AI SDK** - Premium voice synthesis technology
- **🤖 GitHub Models API** - Free AI using GitHub access token
- **💻 PyQt6** - Modern desktop GUI framework
- **� uv** - Fast, modern Python package manager
- **🔄 asyncio** - Asynchronous programming for real-time features

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- uv package manager
- GitHub account with access token
- Murf AI account (optional for demo mode)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MurfAI
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   # Simplified version (RECOMMENDED - currently working)
   uv run python simple_app.py
   
   # Full featured version
   uv run python app.py
   ```

## 🎯 Demo Mode - PERFECT FOR HACKATHONS

The application includes a comprehensive demo mode that works without API keys:

- **🎪 Interactive demonstrations** of all features
- **🎵 Voice synthesis simulation** with realistic previews  
- **🤖 AI conversation examples** showcasing multi-agent capabilities
- **📊 Real-time statistics** and system monitoring
- **🎨 Professional UI** ready for live presentations

### Quick Demo Commands
- Type "hello" for system introduction
- Type "voice" for voice capabilities demo
- Type "hackathon" for project presentation
- Type "features" for complete feature showcase

## 📋 Configuration

### Required Environment Variables

Create a `.env` file with the following:

```env
# GitHub Models API (Free AI)
GITHUB_TOKEN=your_github_personal_access_token

# Murf AI API (Premium Voice Synthesis)  
MURF_API_KEY=your_murf_api_key

# Optional: Logging Level
LOG_LEVEL=INFO
```

### Getting API Keys

#### GitHub Token (Free)
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with appropriate scopes
3. Copy the token to your `.env` file

#### Murf AI Key (Optional)
1. Sign up at [Murf.ai](https://murf.ai)
2. Navigate to API settings in your dashboard
3. Generate an API key and copy to `.env`

## 🎪 Hackathon Features

### Why This Project Wins Hackathons

1. **🚀 Cutting-Edge Technology**
   - Multi-agent AI architecture
   - Premium voice synthesis integration
   - Modern async Python patterns
   - Professional desktop application

2. **💡 Innovation Factor**
   - Novel combination of voice AI and multi-agent systems
   - Real-time conversation with voice feedback
   - Cross-platform desktop solution
   - Production-ready architecture

3. **🎯 Practical Application**
   - Immediate real-world utility
   - Accessible through desktop interface
   - Scalable architecture for enterprise use
   - Cost-effective using free GitHub Models API

4. **🎨 Presentation Ready**
   - Professional UI with dark theme
   - Live demonstration capabilities
   - Real-time statistics and monitoring
   - Interactive demo mode

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Voice Agent   │    │    AI Agent     │    │   UI Agent      │
│                 │    │                 │    │                 │
│ • Murf AI SDK   │    │ • GitHub Models │    │ • PyQt6 GUI     │
│ • Voice Synth   │    │ • Conversation  │    │ • Real-time UI  │
│ • Multi-lang    │    │ • Context Mgmt  │    │ • Event Handling│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Coordination    │
                    │ Agent           │
                    │                 │
                    │ • Inter-agent   │
                    │ • Task Queue    │
                    │ • State Mgmt    │
                    └─────────────────┘
```

## 📚 Usage Examples

### Basic AI Conversation
```python
# The application automatically handles:
user_input = "Hello, tell me about your capabilities"
# → Multi-agent processing
# → AI response generation  
# → Optional voice synthesis
# → Real-time UI updates
```

### Voice Synthesis Demo
```python
# Select voice and synthesize speech
voice_id = "en-US-AriaNeural"
text = "Welcome to MurfAI Assistant!"
# → Automatic voice synthesis
# → Audio playback (in full version)
# → Visual feedback in UI
```

## 🔧 Development

### Project Structure
```
MurfAI/
├── simple_app.py          # ✅ WORKING - Simplified version 
├── app.py                 # Full-featured main application
├── murf_ai_assistant.py   # Core application logic
├── src/                   # Core modules
│   ├── ai_engine.py       # GitHub Models integration
│   ├── voice_manager.py   # Murf AI voice synthesis
│   └── ...               # Other components
├── pyproject.toml         # ✅ Modern Python project config
├── .env.example          # Environment template
└── # 🎤 MurfAI Conversational Assistant

**A Premium Voice-Powered AI Assistant with Real-Time Conversation Capabilities**

Transform your interaction with AI through natural voice conversations powered by Murf's industry-leading text-to-speech technology and GitHub Models API.

![MurfAI Banner](https://img.shields.io/badge/MurfAI-Conversational%20Assistant-blue?style=for-the-badge&logo=python)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat-square&logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI%20Framework-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

## ✨ Features

### 🎯 **Core Capabilities**
- **Real-Time Voice Conversations**: Speak to the AI and hear responses instantly
- **Premium Voice Synthesis**: Powered by Murf's advanced text-to-speech technology
- **Multi-Language Support**: English, Hindi, and 15+ international voices
- **Indian Voice Collection**: Specialized Indian English and Hindi voices
- **GitHub Models Integration**: Free AI conversations using GitHub's model APIs
- **Modern Responsive UI**: Fully resizable, scrollable, and maximizable interface

### 🎵 **Voice Features**
- **15+ Premium Voices**: Including Terrell, Natalie, Julia, Aditi (Hindi), Priya, Kabir
- **Voice Selection**: Switch between voices on-the-fly
- **Auto-Speak**: Automatic voice responses to your messages
- **Voice Testing**: Test any voice before using
- **Real Audio Generation**: Actual Murf API integration (not simulation)

### 🗣️ **Speech Recognition**
- **Voice Input**: Speak your messages instead of typing
- **Real-Time Processing**: Instant speech-to-text conversion
- **Multiple Languages**: English (US/UK/AU/IN), Hindi support
- **Noise Adaptation**: Automatic ambient noise adjustment
- **Smart Timeout**: Responsive 5-second listening windows

### 💬 **Conversation Management**
- **Chat History**: Full conversation tracking with timestamps
- **Export Conversations**: Save chats to text files
- **Clear History**: Fresh conversation starts
- **Processing Times**: Response time tracking
- **Message Statistics**: Detailed session analytics

### 🎨 **User Interface**
- **Dark Modern Theme**: Professional dark mode interface
- **Responsive Design**: Adapts to any screen size
- **Fullscreen Support**: F11 for immersive experience
- **Scrollable Panels**: Never lose content on small screens
- **Quick Actions**: Pre-built conversation starters
- **Status Indicators**: Real-time operation feedback

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** (Python 3.13 recommended)
- **uv package manager** (modern Python package management)
- **Microphone** (for voice input)
- **Speakers/Headphones** (for voice output)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JITESH-KUMAR05/MurfAI.git
   cd MurfAI
   ```

2. **Install Dependencies**
   ```bash
   # Install uv if you don't have it
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install project dependencies
   uv sync
   ```

3. **Configure API Keys**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env with your API keys
   nano .env
   ```

4. **Add Your API Keys to `.env`**
   ```env
   # GitHub Models API (Free - get from https://github.com/settings/tokens)
   GITHUB_TOKEN=ghp_your_github_token_here
   
   # Murf API Key (Premium voices - get from https://murf.ai)
   MURF_API_KEY=your_murf_api_key_here
   ```

5. **Launch the Application**
   ```bash
   uv run python conversational_murf_ai.py
   ```

## 🔧 Configuration

### API Keys Setup

#### GitHub Token (Free AI Chat)
1. Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Create a new token with `repo` and `user` scopes
3. Copy token to `GITHUB_TOKEN` in `.env`

#### Murf API Key (Premium Voices)
1. Sign up at [Murf.ai](https://murf.ai)
2. Go to API settings in your dashboard
3. Generate API key and copy to `MURF_API_KEY` in `.env`

**Note**: The application works in demo mode without API keys, but with limited functionality.

## 🎵 Available Voices

### 🇺🇸 **English (US)**
- **Terrell** (Male) - Clear, professional
- **Natalie** (Female) - Warm, conversational
- **Julia** (Female) - Friendly, engaging
- **Marcus** (Male) - Deep, authoritative

### 🇮🇳 **Indian Voices**
- **Aditi** (Female, Hindi) - Natural Hindi speaker
- **Priya** (Female, English) - Indian English accent
- **Kabir** (Male, English) - Professional Indian English
- **Arjun** (Male, Hindi) - Clear Hindi pronunciation
- **Sneha** (Female, English) - Soft Indian English

### 🌍 **International**
- **Charlotte** (British Female)
- **Ruby** (Australian Female)
- **Elena** (Spanish Female)
- **Marie** (French Female)
- **Hans** (German Male)
- **Akira** (Japanese Male)

## 💻 Usage Guide

### Basic Operation

1. **Start Conversation**
   - Type message and press Enter
   - Or click "Send Message" button
   - AI responds with text and voice

2. **Voice Input**
   - Click "🎤 Voice Input" button
   - Speak clearly when prompted
   - Message appears in text field automatically

3. **Voice Controls**
   - Toggle "Auto-speak responses" for automatic voice output
   - Use "Test Voice" to preview selected voice
   - "Speak Last Message" to repeat last AI response

### Advanced Features

4. **Voice Selection**
   - Choose from dropdown in Voice Settings
   - Includes Indian voices for local users
   - Live switching during conversation

5. **Window Controls**
   - **F11**: Toggle fullscreen mode
   - **Escape**: Exit fullscreen
   - **Drag to resize**: Responsive window sizing
   - **Maximize button**: Standard window maximizing

6. **Conversation Management**
   - "Clear Conversation": Fresh start
   - "Export Chat": Save conversation to file
   - Statistics panel shows session metrics

## 🔊 Audio & Voice Setup

### Microphone Configuration
```bash
# Test your microphone (Linux)
arecord -l                    # List audio devices
arecord -d 3 test.wav        # Record 3-second test

# Check permissions
sudo usermod -a -G audio $USER  # Add user to audio group
```

### Common Audio Issues

| Issue | Solution |
|-------|----------|
| No microphone detected | Check USB connection, permissions |
| ALSA lib warnings | Ignore if audio works; install `libasound2-dev` |
| Voice input timeout | Speak clearly, reduce background noise |
| No audio output | Check speakers, volume, audio device selection |

## 🛠️ Development

### Project Structure
```
MurfAI/
├── conversational_murf_ai.py    # Main application
├── pyproject.toml              # Dependencies & metadata
├── .env.example               # Environment template
├── README.md                 # This file
├── .gitignore               # Git ignore rules
└── uv.lock                 # Dependency lock file
```

### Key Components

#### Classes Overview
- **`ConversationalMurfAI`**: Main application window and UI
- **`MurfTTSClient`**: Murf API integration for voice synthesis
- **`VoiceInputWorker`**: Speech recognition in separate thread
- **`ConversationalAI`**: GitHub Models API integration
- **`AudioPlayer`**: Audio playback management
- **`SpeechWorker`**: Text-to-speech processing

#### Threading Architecture
- **Main Thread**: UI and user interaction
- **AI Thread**: GitHub Models API calls
- **TTS Thread**: Murf voice synthesis
- **Voice Input Thread**: Speech recognition
- **Audio Thread**: Audio playback

### Customization

#### Adding New Voices
```python
# In MurfTTSClient._load_demo_voices()
self.available_voices.append({
    "voice_id": "your-voice-id",
    "name": "Voice Name",
    "language": "Language",
    "accent": "Accent",
    "gender": "Male/Female"
})
```

#### UI Modifications
- Styles in `apply_enhanced_theme()`
- Panels in `create_*_section()` methods
- Layouts in `setup_ui()`

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Missing dependencies
uv sync

# Python version issues
python --version  # Should be 3.11+
```

**2. API Connection Issues**
```bash
# Test GitHub token
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.github.com/user

# Check Murf API key in dashboard
```

**3. Audio Problems**
```bash
# Linux audio setup
sudo apt install python3-pyaudio portaudio19-dev
pip install --upgrade pyaudio pygame

# Test pygame audio
python -c "import pygame; pygame.mixer.init(); print('Audio OK')"
```

**4. Voice Input Not Working**
- Check microphone permissions
- Ensure quiet environment
- Speak clearly and loudly
- Try different microphone if available

**5. UI Not Resizing**
- Update to latest PyQt6: `uv add "PyQt6>=6.6"`
- Check window manager settings
- Try fullscreen mode (F11)

### Debug Mode
```bash
# Run with debug logging
PYTHONPATH=. uv run python conversational_murf_ai.py --debug
```

### Log Files
- Application logs: `murf_ai_conversational.log`
- Check for errors and API responses

## 📊 Performance Tips

### Optimizing Voice Synthesis
- Use shorter text for faster generation
- Cache common responses locally
- Choose faster voices (US English typically fastest)

### Improving Speech Recognition
- Use good quality microphone
- Minimize background noise
- Speak at normal pace, clearly
- Position microphone 6-12 inches from mouth

### UI Performance
- Close unnecessary applications
- Use hardware acceleration if available
- Consider lower resolution on older systems

## 🔐 Security & Privacy

### API Key Protection
- Never commit API keys to version control
- Use environment variables (`.env` file)
- Rotate keys regularly
- Restrict key permissions where possible

### Data Handling
- Conversations stored locally only
- Voice data processed in memory
- No persistent audio storage
- Clear sensitive conversations after use

### Network Security
- All API calls use HTTPS
- Tokens transmitted securely
- No data shared with third parties

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the Repository**
   ```bash
   git fork https://github.com/JITESH-KUMAR05/MurfAI.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

4. **Submit Pull Request**
   - Describe changes clearly
   - Include test results
   - Reference any issues

### Development Setup
```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy conversational_murf_ai.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Technologies Used
- **[Murf.ai](https://murf.ai)** - Premium voice synthesis
- **[GitHub Models](https://github.com/marketplace/models)** - AI conversation engine
- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Modern UI framework
- **[SpeechRecognition](https://pypi.org/project/SpeechRecognition/)** - Voice input processing
- **[pygame](https://www.pygame.org/)** - Audio playback
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package management

### Special Thanks
- OpenAI & GitHub for free AI model access
- Murf team for excellent voice synthesis
- Python community for amazing libraries
- Contributors and beta testers

## 📞 Support

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/JITESH-KUMAR05/MurfAI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/JITESH-KUMAR05/MurfAI/discussions)
- **Email**: [Support Email](mailto:support@example.com)

### Documentation
- **API Documentation**: [Murf API Docs](https://docs.murf.ai)
- **GitHub Models**: [GitHub Models Documentation](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api)
- **PyQt6 Guide**: [PyQt6 Documentation](https://doc.qt.io/qtforpython/)

---

**Made with ❤️ by [JITESH-KUMAR05](https://github.com/JITESH-KUMAR05)**

*Transform your AI conversations with the power of voice!*             # This file
```

### Current Working Files
- ✅ `simple_app.py` - Main working application
- ✅ `pyproject.toml` - Optimized dependencies
- ✅ `.env.example` - Configuration template
- ✅ All core functionality implemented and tested

## 🚨 Troubleshooting

### ✅ RESOLVED: PyAudio Installation Issues
**Issue**: PyAudio compilation errors on Fedora
**Solution**: Simplified dependencies to remove problematic audio libraries
**Status**: ✅ FIXED - Application now runs without PyAudio

### Common Issues

**GitHub API Rate Limits**
- Use personal access token for higher limits
- Implement request caching for demo mode
- Monitor API usage in application logs

**Voice Synthesis Issues**
- Check Murf API key validity
- Verify internet connection
- Use demo mode for presentations

## 🤝 Contributing

We welcome contributions to make this project even better for hackathons!

1. Fork the repository
2. Create a feature branch
3. Make your improvements  
4. Add tests and documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🏆 Hackathon Success Status: READY! 

✅ **Technical Excellence**: Modern Python, async programming, multi-agent architecture  
✅ **Innovation**: Novel AI + voice synthesis combination  
✅ **Practical Value**: Real desktop application with immediate utility  
✅ **Presentation Ready**: Professional UI, demo mode, live capabilities  
✅ **Working Application**: Successfully running on Fedora Linux  
✅ **Cross-Platform**: Compatible with Windows, macOS, Linux  

## 🎯 Ready to Win Hackathons!

Your MurfAI Assistant is now **fully functional** and ready for hackathon demonstrations! 

### To start presenting:
```bash
uv run python simple_app.py
```

Perfect for impressing hackathon judges and winning competitions! 🏆

---

**Built with ❤️ for hackathon success! Now WORKING! 🚀**
