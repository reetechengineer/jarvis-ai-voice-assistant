#!/usr/bin/env python3
"""
Enhanced Jarvis AI Voice Assistant
Author: AI Assistant
Version: 2.0
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import pyjokes
import requests
import queue
import threading
import os
import time
import sys
import subprocess
import json
import re
import random
import logging
from typing import Optional, Dict, Any
from pathlib import Path

try:
    import wolframalpha
except ImportError:
    wolframalpha = None

try:
    import smtplib
    from email.message import EmailMessage
except ImportError:
    smtplib = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Create a .env file manually.")

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    print("Warning: PyAudio not available. Voice input will be disabled.")
    pyaudio = None
    PYAUDIO_AVAILABLE = False

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Configuration ---
class Config:
    ASSISTANT_NAME = "Jarvis"
    WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis"]
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    WOLFRAM_ALPHA_API_KEY = os.getenv("WOLFRAM_ALPHA_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # Email Configuration
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # TTS Configuration
    TTS_RATE = 170
    TTS_VOLUME = 0.9
    
    # Speech Recognition
    LISTEN_TIMEOUT = 3
    PHRASE_TIME_LIMIT = 5
    
    # File paths
    CONFIG_DIR = Path.home() / ".jarvis"
    MEMORY_FILE = CONFIG_DIR / "memory.json"
    
    @classmethod
    def create_config_dir(cls):
        cls.CONFIG_DIR.mkdir(exist_ok=True)

# Initialize config directory
Config.create_config_dir()

# --- Enhanced TTS Engine Setup ---
class TTSEngine:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', Config.TTS_RATE)
            self.engine.setProperty('volume', Config.TTS_VOLUME)
            
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a female voice, fallback to first available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    self.engine.setProperty('voice', voices[0].id)
                self.has_voice = True
                logger.info(f"TTS initialized with voice: {voices[0].name}")
            else:
                self.has_voice = False
                logger.warning("No TTS voices found. Assistant will be silent.")
        except Exception as e:
            self.has_voice = False
            logger.error(f"TTS initialization failed: {e}")
    
    def speak(self, text: str):
        """Speak the given text"""
        if self.has_voice:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                logger.error(f"TTS Error: {e}")

# --- Memory System ---
class Memory:
    def __init__(self):
        self.memory_file = Config.MEMORY_FILE
        self.data = self.load_memory()
    
    def load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load memory: {e}")
        return {"conversations": [], "preferences": {}, "reminders": []}
    
    def save_memory(self):
        """Save memory to file"""
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
    
    def remember(self, key: str, value: Any):
        """Remember a key-value pair"""
        self.data["preferences"][key] = value
        self.save_memory()
    
    def recall(self, key: str) -> Any:
        """Recall a value by key"""
        return self.data["preferences"].get(key)
    
    def add_conversation(self, user_input: str, response: str):
        """Add conversation to memory"""
        self.data["conversations"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user_input,
            "assistant": response
        })
        # Keep only last 100 conversations
        if len(self.data["conversations"]) > 100:
            self.data["conversations"] = self.data["conversations"][-100:]
        self.save_memory()

# --- Enhanced Voice Assistant ---
class JarvisAssistant:
    def __init__(self):
        self.tts = TTSEngine()
        self.memory = Memory()
        self.recognizer = sr.Recognizer()
        
        # Initialize microphone only if PyAudio is available
        if PYAUDIO_AVAILABLE:
            try:
                self.microphone = sr.Microphone()
                self.has_microphone = True
                logger.info("Microphone initialized successfully")
            except Exception as e:
                logger.warning(f"Microphone initialization failed: {e}")
                self.microphone = None
                self.has_microphone = False
        else:
            self.microphone = None
            self.has_microphone = False
            logger.info("Microphone disabled - PyAudio not available")
        
        self.running = True
        
        # Initialize TTS queue for threaded speech
        self.tts_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()
        
        # Calibrate microphone if available
        if self.has_microphone:
            self._calibrate_microphone()
        
        logger.info("Jarvis Assistant initialized successfully")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if not self.has_microphone:
            logger.info("Skipping microphone calibration - no microphone available")
            return
        
        try:
            with self.microphone as source:
                logger.info("Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone calibrated")
        except Exception as e:
            logger.error(f"Microphone calibration failed: {e}")
            self.has_microphone = False
    
    def _tts_worker(self):
        """Worker thread for TTS queue"""
        while True:
            text = self.tts_queue.get()
            if text is None:
                break
            print(f"{Config.ASSISTANT_NAME}: {text}")
            self.tts.speak(text)
            self.tts_queue.task_done()
    
    def speak(self, text: str):
        """Add text to TTS queue"""
        self.tts_queue.put(text)
    
    def listen(self, timeout: int = Config.LISTEN_TIMEOUT) -> Optional[str]:
        """Listen for audio input and convert to text"""
        if not self.has_microphone:
            return None
            
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=Config.PHRASE_TIME_LIMIT
                )
                command = self.recognizer.recognize_google(audio).strip()
                print(f"👤 You: {command}")
                return command.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in listen(): {e}")
            return None
    
    def get_text_input(self) -> Optional[str]:
        """Get text input from user"""
        try:
            return input("👤 You: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return None
    
    # --- Utility Functions ---
    def get_greeting(self) -> str:
        """Get time-based greeting"""
        hour = datetime.datetime.now().hour
        name = self.memory.recall("user_name")
        greeting_base = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        return f"{greeting_base}{f', {name}' if name else ''}"
    
    def extract_city_from_weather_command(self, command: str) -> Optional[str]:
        """Extract city name from weather command"""
        # Remove common weather command words
        for phrase in ['weather', 'temperature', 'forecast', 'in', 'for', 'at']:
            command = command.replace(phrase, ' ')
        
        # Clean up and return non-empty result
        city = ' '.join(command.split()).strip()
        return city if city else None
    
    # --- Core Functions ---
    def tell_time(self):
        """Tell current time"""
        try:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d")
            response = f"It's {time_str} on {date_str}"
            self.speak(response)
            return response
        except Exception as e:
            logger.error(f"Error telling time: {e}")
            self.speak("Sorry, I couldn't get the current time.")
    
    def tell_date(self):
        """Tell current date"""
        try:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {today}"
            self.speak(response)
            return response
        except Exception as e:
            logger.error(f"Error telling date: {e}")
            self.speak("Sorry, I couldn't get the current date.")
    
    def search_wikipedia(self, query: str):
        """Search Wikipedia for information"""
        try:
            self.speak("Let me search Wikipedia for that...")
            
            # Clean query
            query = re.sub(r'\b(wikipedia|search|look up|find)\b', '', query).strip()
            if not query:
                self.speak("What would you like me to search for?")
                return
            
            # Search with error handling
            try:
                summary = wikipedia.summary(query, sentences=3, auto_suggest=True)
                response = f"According to Wikipedia: {summary}"
                self.speak(response)
                return response
            except wikipedia.DisambiguationError as e:
                options = ', '.join(e.options[:3])
                response = f"I found multiple results. Could you be more specific? Options include: {options}"
                self.speak(response)
                return response
            except wikipedia.PageError:
                response = f"I couldn't find information about {query} on Wikipedia."
                self.speak(response)
                return response
                
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            self.speak("Sorry, I encountered an error while searching Wikipedia.")
    
    def open_website(self, url: str, name: str = None):
        """Open website in browser"""
        try:
            if not name:
                name = url.split('//')[-1].split('/')[0]
            self.speak(f"Opening {name}")
            webbrowser.open(url)
            return f"Opened {name}"
        except Exception as e:
            logger.error(f"Browser error: {e}")
            self.speak("Sorry, I couldn't open that website.")
    
    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = pyjokes.get_joke()
            self.speak(joke)
            return joke
        except Exception as e:
            logger.error(f"Joke error: {e}")
            self.speak("I seem to have forgotten my jokes. Let me try to remember some!")
    
    def get_weather(self, city: str = None):
        """Get weather information"""
        if not Config.OPENWEATHER_API_KEY:
            self.speak("I need an OpenWeather API key to check the weather. Please configure it in your environment.")
            return
        
        if not city:
            self.speak("Which city's weather would you like to know?")
            response = self.listen(timeout=5) or self.get_text_input()
            if not response:
                self.speak("I didn't get a city name.")
                return
            city = response
        
        try:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city,
                "appid": Config.OPENWEATHER_API_KEY,
                "units": "metric"
            }
            
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get('cod') != 200:
                self.speak(f"Sorry, I couldn't find weather information for {city}.")
                return
            
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            city_name = data['name']
            
            weather_response = (
                f"Weather in {city_name}: {description}. "
                f"Temperature is {temp}°C, feels like {feels_like}°C. "
                f"Humidity is {humidity}%."
            )
            
            self.speak(weather_response)
            return weather_response
            
        except requests.exceptions.Timeout:
            self.speak("The weather service is taking too long to respond. Please try again later.")
        except Exception as e:
            logger.error(f"Weather error: {e}")
            self.speak("I couldn't retrieve weather information right now.")
    
    def get_news(self):
        """Get latest news headlines"""
        if not Config.NEWS_API_KEY:
            self.speak("I need a News API key to get news. You can get one from newsapi.org")
            return
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": Config.NEWS_API_KEY,
                "country": "us",
                "pageSize": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                if articles:
                    self.speak("Here are the top news headlines:")
                    for i, article in enumerate(articles[:3], 1):
                        title = article.get('title', '')
                        self.speak(f"{i}. {title}")
                else:
                    self.speak("No news articles found.")
            else:
                self.speak("I couldn't retrieve news at the moment.")
                
        except Exception as e:
            logger.error(f"News error: {e}")
            self.speak("I couldn't get the news right now.")
    
    def calculate(self, query: str):
        """Perform calculations using Wolfram Alpha or basic math"""
        # Try basic math first
        try:
            # Clean query for basic math
            math_query = re.sub(r'\b(calculate|what is|compute)\b', '', query).strip()
            
            # Simple arithmetic operations
            if re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', math_query):
                result = eval(math_query)
                response = f"The answer is {result}"
                self.speak(response)
                return response
        except:
            pass
        
        # Use Wolfram Alpha for complex queries
        if not Config.WOLFRAM_ALPHA_API_KEY or not wolframalpha:
            self.speak("I need Wolfram Alpha API access for complex calculations.")
            return
        
        try:
            client = wolframalpha.Client(Config.WOLFRAM_ALPHA_API_KEY)
            res = client.query(query)
            answer = next(res.results).text
            response = f"The answer is: {answer}"
            self.speak(response)
            return response
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            self.speak("I couldn't calculate that. Please try rephrasing your question.")
    
    def send_email(self):
        """Send email with user input"""
        if not Config.EMAIL_ADDRESS or not Config.EMAIL_PASSWORD or not smtplib:
            self.speak("Email is not configured. Please set up your email credentials.")
            return
        
        try:
            self.speak("Who would you like to send an email to?")
            receiver = self.listen(timeout=10) or self.get_text_input()
            if not receiver:
                self.speak("I didn't get the receiver's email.")
                return
            
            self.speak("What's the subject?")
            subject = self.listen(timeout=10) or self.get_text_input()
            if not subject:
                self.speak("I didn't get the subject.")
                return
            
            self.speak("What's the message?")
            message = self.listen(timeout=15) or self.get_text_input()
            if not message:
                self.speak("I didn't get the message.")
                return
            
            # Create and send email
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = subject
            msg['From'] = Config.EMAIL_ADDRESS
            msg['To'] = receiver
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD)
                server.send_message(msg)
            
            self.speak("Email sent successfully!")
            return "Email sent"
            
        except Exception as e:
            logger.error(f"Email error: {e}")
            self.speak("Failed to send email. Please check your configuration.")
    
    def set_reminder(self, reminder_text: str):
        """Set a reminder"""
        try:
            reminders = self.memory.data.get("reminders", [])
            reminder = {
                "text": reminder_text,
                "timestamp": datetime.datetime.now().isoformat(),
                "completed": False
            }
            reminders.append(reminder)
            self.memory.data["reminders"] = reminders
            self.memory.save_memory()
            
            self.speak(f"I'll remember to remind you: {reminder_text}")
            return "Reminder set"
        except Exception as e:
            logger.error(f"Reminder error: {e}")
            self.speak("I couldn't set that reminder.")
    
    def get_reminders(self):
        """Get pending reminders"""
        try:
            reminders = self.memory.data.get("reminders", [])
            pending = [r for r in reminders if not r.get("completed", False)]
            
            if pending:
                self.speak(f"You have {len(pending)} pending reminders:")
                for i, reminder in enumerate(pending, 1):
                    self.speak(f"{i}. {reminder['text']}")
            else:
                self.speak("You don't have any pending reminders.")
                
        except Exception as e:
            logger.error(f"Get reminders error: {e}")
            self.speak("I couldn't retrieve your reminders.")
    
    def remember_user_info(self, command: str):
        """Remember user information"""
        try:
            if "name is" in command:
                name = command.split("name is")[-1].strip()
                self.memory.remember("user_name", name)
                self.speak(f"Nice to meet you, {name}! I'll remember your name.")
            elif "favorite color" in command:
                color = command.split("favorite color")[-1].replace("is", "").strip()
                self.memory.remember("favorite_color", color)
                self.speak(f"Got it! Your favorite color is {color}.")
            else:
                self.speak("What would you like me to remember?")
        except Exception as e:
            logger.error(f"Remember info error: {e}")
            self.speak("I couldn't remember that information.")
    
    def system_control(self, command: str):
        """Control system functions"""
        try:
            if "shutdown" in command or "power off" in command:
                self.speak("Shutting down the system in 10 seconds. Say cancel to stop.")
                # Give user chance to cancel
                response = self.listen(timeout=5)
                if response and "cancel" in response:
                    self.speak("Shutdown cancelled.")
                    return
                
                self.speak("Shutting down now. Goodbye!")
                if sys.platform == "win32":
                    os.system('shutdown /s /t 1')
                else:
                    os.system('sudo shutdown now')
            elif "restart" in command or "reboot" in command:
                self.speak("Restarting the system.")
                if sys.platform == "win32":
                    os.system('shutdown /r /t 1')
                else:
                    os.system('sudo reboot')
        except Exception as e:
            logger.error(f"System control error: {e}")
            self.speak("I couldn't execute that system command.")
    
    # --- Command Processing ---
    def process_command(self, command: str) -> bool:
        """Process user command and return True if should quit"""
        if not command:
            return False
        
        # Remove wake words
        for wake_word in Config.WAKE_WORDS:
            command = command.replace(wake_word, "").strip()
        
        response = None
        
        try:
            # Time and date
            if any(word in command for word in ['time', 'clock']):
                response = self.tell_time()
            elif any(word in command for word in ['date', 'today']):
                response = self.tell_date()
            
            # Search and information
            elif 'wikipedia' in command:
                response = self.search_wikipedia(command)
            elif 'weather' in command:
                city = self.extract_city_from_weather_command(command)
                response = self.get_weather(city)
            elif 'news' in command or 'headlines' in command:
                response = self.get_news()
            
            # Web browsing
            elif 'open youtube' in command:
                response = self.open_website('https://www.youtube.com', "YouTube")
            elif 'open google' in command:
                response = self.open_website('https://www.google.com', "Google")
            elif 'open github' in command:
                response = self.open_website('https://www.github.com', "GitHub")
            elif 'open netflix' in command:
                response = self.open_website('https://www.netflix.com', "Netflix")
            
            # Entertainment
            elif any(word in command for word in ['joke', 'funny', 'humor']):
                response = self.tell_joke()
            
            # Calculations
            elif any(word in command for word in ['calculate', 'math', 'compute', 'what is']):
                response = self.calculate(command)
            
            # Communication
            elif 'email' in command or 'send email' in command:
                response = self.send_email()
            
            # Memory and reminders
            elif 'remember' in command and any(word in command for word in ['name', 'color', 'favorite']):
                response = self.remember_user_info(command)
            elif 'remind me' in command or 'set reminder' in command:
                reminder_text = command.replace('remind me', '').replace('set reminder', '').strip()
                response = self.set_reminder(reminder_text)
            elif 'my reminders' in command or 'show reminders' in command:
                response = self.get_reminders()
            
            # System control
            elif any(word in command for word in ['shutdown', 'power off', 'restart', 'reboot']):
                self.system_control(command)
                return True
            
            # Exit commands
            elif any(word in command for word in ['quit', 'exit', 'stop', 'bye', 'goodbye']):
                self.speak("It was nice talking to you. Goodbye!")
                return True
            
            # Help
            elif 'help' in command or 'what can you do' in command:
                help_text = (
                    "I can help you with time, date, weather, news, Wikipedia searches, "
                    "calculations, jokes, opening websites, sending emails, setting reminders, "
                    "and system control. Just ask me naturally!"
                )
                self.speak(help_text)
                response = help_text
            
            # Unknown command
            else:
                responses = [
                    "I didn't understand that. Could you try rephrasing?",
                    "I'm not sure what you mean. Can you be more specific?",
                    "Sorry, I didn't catch that. What would you like me to do?",
                    "I'm still learning. Could you try a different command?"
                ]
                response = random.choice(responses)
                self.speak(response)
            
            # Log conversation
            if response:
                self.memory.add_conversation(command, response)
                
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            self.speak("Sorry, I encountered an error processing that command.")
        
        return False
    
    def run(self):
        """Main execution loop"""
        try:
            # Initial greeting
            greeting = f"{self.get_greeting()}, I am {Config.ASSISTANT_NAME}. How can I help you today?"
            self.speak(greeting)
            print(f"\n🤖 {Config.ASSISTANT_NAME} is ready!")
            
            if self.has_microphone:
                print(f"💡 Say one of these wake words: {', '.join(Config.WAKE_WORDS)}")
                print("💡 Or type your commands directly")
            else:
                print("💡 Voice input disabled - type your commands")
                print("💡 Note: Install PyAudio to enable voice input")
            
            print("💡 Say 'help' to see what I can do")
            
            while self.running:
                try:
                    command = None
                    
                    if self.has_microphone:
                        # Try voice input first, fallback to text
                        command = self.listen()
                    
                    if command is None:
                        # If no voice input or voice disabled, use text input
                        try:
                            if self.has_microphone:
                                print("\n💬 No voice detected. Type your command or press Enter to continue listening:")
                            else:
                                print("\n💬 Type your command:")
                            command = input().strip().lower()
                            if not command:
                                continue
                        except (EOFError, KeyboardInterrupt):
                            break
                    
                    # Check for wake word or process direct command
                    if any(wake_word in command for wake_word in Config.WAKE_WORDS) or True:
                        if self.process_command(command):
                            break
                            
                except KeyboardInterrupt:
                    self.speak("Shutting down. Goodbye!")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error in main loop: {e}")
                    time.sleep(1)
        
        finally:
            # Cleanup
            self.tts_queue.put(None)
            if self.tts_thread.is_alive():
                self.tts_thread.join(timeout=2)
            logger.info("Jarvis Assistant shutdown complete")

# --- Main Entry Point ---
def main():
    """Main entry point"""
    try:
        assistant = JarvisAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
    finally:
        sys.exit(0)

if __name__ == '__main__':
    main()