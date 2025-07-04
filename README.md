# 🤖 Jarvis AI Voice Assistant

A powerful, customizable AI voice assistant built with Python that can help you with various tasks through voice commands or text input.

## ✨ Features

### Core Capabilities
- 🎤 **Voice Recognition**: Advanced speech-to-text using Google's Speech Recognition
- 🔊 **Text-to-Speech**: Natural voice synthesis with customizable voices
- 💭 **Memory System**: Remembers conversations, preferences, and user information
- 🌐 **Multi-modal Input**: Supports both voice and text input
- 📝 **Logging**: Comprehensive logging for debugging and monitoring

### Smart Functions
- 🕐 **Time & Date**: Get current time and date
- 🌤️ **Weather**: Real-time weather information for any city
- 📚 **Wikipedia Search**: Quick access to Wikipedia information
- 🧮 **Calculator**: Basic math and complex calculations via Wolfram Alpha
- 📰 **News**: Latest headlines from News API
- 😂 **Entertainment**: Random jokes and humor
- 🌐 **Web Control**: Open websites (YouTube, Google, GitHub, Netflix)
- 📧 **Email**: Send emails through Gmail
- 📋 **Reminders**: Set and manage personal reminders
- 💾 **Personal Memory**: Remember user preferences and information
- ⚙️ **System Control**: Shutdown, restart system commands

### Advanced Features
- 🎯 **Multiple Wake Words**: "Jarvis", "Hey Jarvis", "OK Jarvis"
- 🧵 **Threaded TTS**: Non-blocking text-to-speech processing
- 🛡️ **Error Handling**: Robust error handling and graceful degradation
- 🔧 **Configurable**: Highly customizable through environment variables
- 📊 **Smart Command Processing**: Context-aware command interpretation

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Microphone for voice input
- Internet connection for API services

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jarvis-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies (Linux/Ubuntu)**
   ```bash
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-pyaudio
   sudo apt-get install espeak espeak-data libespeak1 libespeak-dev
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (see Configuration section)
   ```

5. **Run Jarvis**
   ```bash
   python jarvis.py
   ```

## ⚙️ Configuration

### Required API Keys

1. **OpenWeather API** (Free)
   - Visit: https://openweathermap.org/api
   - Get free API key for weather information
   - Add to `.env`: `OPENWEATHER_API_KEY=your_key`

2. **Wolfram Alpha API** (Free tier available)
   - Visit: https://developer.wolframalpha.com/portal/myapps/
   - Get API key for advanced calculations
   - Add to `.env`: `WOLFRAM_ALPHA_API_KEY=your_key`

3. **News API** (Free tier available)
   - Visit: https://newsapi.org/
   - Get API key for news headlines
   - Add to `.env`: `NEWS_API_KEY=your_key`

4. **Gmail Configuration** (Optional)
   - Enable 2-factor authentication on Gmail
   - Generate App Password: https://support.google.com/accounts/answer/185833
   - Add to `.env`: 
     ```
     EMAIL_ADDRESS=your_email@gmail.com
     EMAIL_PASSWORD=your_app_password
     ```

### Environment Variables
```bash
# Copy .env.example to .env and configure:
OPENWEATHER_API_KEY=your_openweather_key
WOLFRAM_ALPHA_API_KEY=your_wolfram_key
NEWS_API_KEY=your_news_key
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## 🎮 Usage

### Voice Commands

#### Basic Commands
- **"What time is it?"** - Get current time
- **"What's the date?"** - Get current date
- **"Tell me a joke"** - Random joke
- **"Help"** - List available commands

#### Information & Search
- **"Wikipedia [topic]"** - Search Wikipedia
- **"Weather in [city]"** - Get weather information
- **"News"** - Get latest headlines
- **"Calculate [expression]"** - Perform calculations

#### Web Control
- **"Open YouTube"** - Open YouTube in browser
- **"Open Google"** - Open Google in browser
- **"Open GitHub"** - Open GitHub in browser
- **"Open Netflix"** - Open Netflix in browser

#### Personal Assistant
- **"Remember my name is [name]"** - Store personal information
- **"Remind me to [task]"** - Set a reminder
- **"Show my reminders"** - View pending reminders
- **"Send an email"** - Send email (interactive)

#### System Control
- **"Shutdown"** - Shutdown system (with confirmation)
- **"Restart"** - Restart system
- **"Quit"** - Exit Jarvis

### Text Input
If voice recognition fails or you prefer typing, you can always type commands directly when prompted.

## 📁 Project Structure

```
jarvis-assistant/
├── jarvis.py           # Main application file
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env              # Your API keys (create from .env.example)
├── README.md         # This file
├── jarvis.log        # Application logs
└── ~/.jarvis/        # User data directory
    └── memory.json   # Conversation history and user preferences
```

## 🛠️ Development

### Code Structure
- **`JarvisAssistant`**: Main assistant class
- **`TTSEngine`**: Text-to-speech handling
- **`Memory`**: Persistent storage for conversations and preferences
- **`Config`**: Configuration management

### Adding New Features
1. Add new methods to `JarvisAssistant` class
2. Update `process_command()` method to handle new commands
3. Add any new dependencies to `requirements.txt`
4. Update this README with new features

### Logging
Logs are saved to `jarvis.log` with timestamps and detailed error information.

## 🐛 Troubleshooting

### Common Issues

1. **PyAudio Installation Error**
   ```bash
   # Linux/Ubuntu
   sudo apt-get install portaudio19-dev python3-pyaudio
   
   # macOS
   brew install portaudio
   
   # Windows: Download pre-compiled wheel or install Visual C++ Build Tools
   ```

2. **No Voice/TTS Not Working**
   - Check if system has TTS voices installed
   - Linux: `sudo apt-get install espeak`
   - macOS: TTS should work out of the box
   - Windows: TTS should work out of the box

3. **Speech Recognition Not Working**
   - Check microphone permissions
   - Ensure internet connection (Google Speech API)
   - Try typing commands instead

4. **API Errors**
   - Verify API keys in `.env` file
   - Check API rate limits
   - Ensure internet connectivity

### Error Logs
Check `jarvis.log` for detailed error information and debugging.

## 🔮 Future Enhancements

- 🧠 **AI Integration**: OpenAI GPT integration for advanced conversations
- 📱 **Mobile App**: Companion mobile application
- 🏠 **Smart Home**: IoT device control
- 🎵 **Music Control**: Spotify/Apple Music integration
- 🌍 **Multi-language**: Support for multiple languages
- 📊 **Analytics**: Usage statistics and insights
- 🔊 **Custom Wake Words**: Train custom wake word detection
- 💬 **Natural Language**: More natural conversation flow

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Review `jarvis.log` for error details
3. Create an issue on GitHub
4. Ensure all API keys are properly configured

---

**Happy Chatting with Jarvis! 🤖✨**