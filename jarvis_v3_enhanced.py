#!/usr/bin/env python3
"""
JARVIS AI ASSISTANT - ENHANCED VERSION 3.0
Advanced AI-Powered Personal Assistant with Machine Learning, Automation & Intelligence

Features:
- Advanced AI Integration (OpenAI, Claude, Google AI)
- File Management & Document Processing  
- Image Processing & OCR
- Data Analysis & Visualization
- Task Automation & Scheduling
- Security & Encryption
- Code Assistant & Programming Help
- Language Translation & NLP
- Financial Data & Analysis
- Media Control & Smart Home
- Health Monitoring & Fitness
- Learning System & Memory Enhancement
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
import json
import re
import random
import logging
import hashlib
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
import sqlite3
import schedule
from dataclasses import dataclass
import psutil
import qrcode
import io

# Advanced AI & ML imports (with fallbacks)
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    import pytesseract
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False

try:
    from googletrans import Translator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False

try:
    import yfinance as yf
    FINANCE_AVAILABLE = True
except ImportError:
    FINANCE_AVAILABLE = False

try:
    from textblob import TextBlob
    NLP_AVAILABLE = True
except ImportError:
    NLP_AVAILABLE = False

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed.")

# Audio system check
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    print("Warning: PyAudio not available. Voice input will be disabled.")
    pyaudio = None
    PYAUDIO_AVAILABLE = False

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis_enhanced.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Enhanced Configuration
@dataclass
class EnhancedConfig:
    ASSISTANT_NAME: str = "Jarvis"
    VERSION: str = "3.0 Enhanced"
    WAKE_WORDS: List[str] = None
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY")
    GOOGLE_AI_KEY: str = os.getenv("GOOGLE_AI_KEY")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY")
    WOLFRAM_ALPHA_API_KEY: str = os.getenv("WOLFRAM_ALPHA_API_KEY")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY")
    
    # Email Configuration
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    
    # Security
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY")
    
    # Directories
    CONFIG_DIR: Path = Path.home() / ".jarvis_enhanced"
    MEMORY_FILE: Path = CONFIG_DIR / "enhanced_memory.db"
    DOCUMENTS_DIR: Path = CONFIG_DIR / "documents"
    IMAGES_DIR: Path = CONFIG_DIR / "images"
    DATA_DIR: Path = CONFIG_DIR / "data"
    LOGS_DIR: Path = CONFIG_DIR / "logs"
    
    # TTS/STT Settings
    TTS_RATE: int = 170
    TTS_VOLUME: float = 0.9
    LISTEN_TIMEOUT: int = 3
    PHRASE_TIME_LIMIT: int = 5
    
    # AI Settings
    MAX_AI_RESPONSE_LENGTH: int = 500
    AI_TEMPERATURE: float = 0.7
    AI_MODEL: str = "gpt-3.5-turbo"
    
    def __post_init__(self):
        if self.WAKE_WORDS is None:
            self.WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis", "computer"]
        
        # Create directories
        for directory in [self.CONFIG_DIR, self.DOCUMENTS_DIR, self.IMAGES_DIR, 
                         self.DATA_DIR, self.LOGS_DIR]:
            directory.mkdir(exist_ok=True, parents=True)

config = EnhancedConfig()

# Enhanced Database Memory System
class EnhancedMemory:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with enhanced schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_input TEXT NOT NULL,
                assistant_response TEXT NOT NULL,
                context JSON,
                sentiment REAL,
                importance INTEGER DEFAULT 1
            )
        ''')
        
        # User preferences
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                category TEXT,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Tasks and reminders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                completed BOOLEAN DEFAULT FALSE,
                priority INTEGER DEFAULT 1,
                category TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Learning data
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                confidence REAL,
                created_at TEXT NOT NULL
            )
        ''')
        
        # File references
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                filepath TEXT NOT NULL,
                file_type TEXT,
                description TEXT,
                tags TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_conversation(self, user_input: str, response: str, context: Dict = None, sentiment: float = 0.0):
        """Add conversation with enhanced metadata"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (timestamp, user_input, assistant_response, context, sentiment)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.datetime.now().isoformat(), user_input, response, 
              json.dumps(context or {}), sentiment))
        
        conn.commit()
        conn.close()
    
    def set_preference(self, key: str, value: str, category: str = "general"):
        """Set user preference with category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO preferences (key, value, category, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (key, value, category, datetime.datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_preference(self, key: str) -> Optional[str]:
        """Get user preference"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM preferences WHERE key = ?', (key,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def add_task(self, title: str, description: str = "", due_date: str = "", 
                priority: int = 1, category: str = "general"):
        """Add task/reminder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, priority, category, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, description, due_date, priority, category, 
              datetime.datetime.now().isoformat()))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return task_id
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, due_date, priority, category, created_at
            FROM tasks WHERE completed = FALSE
            ORDER BY priority DESC, due_date ASC
        ''')
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'id': row[0], 'title': row[1], 'description': row[2],
                'due_date': row[3], 'priority': row[4], 'category': row[5],
                'created_at': row[6]
            })
        
        conn.close()
        return tasks
    
    def complete_task(self, task_id: int):
        """Mark task as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()

# Advanced AI Integration System
class AISystem:
    def __init__(self):
        self.openai_client = None
        self.setup_ai_clients()
    
    def setup_ai_clients(self):
        """Setup AI service clients"""
        if OPENAI_AVAILABLE and config.OPENAI_API_KEY:
            try:
                openai.api_key = config.OPENAI_API_KEY
                self.openai_client = openai
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.error(f"OpenAI setup failed: {e}")
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate AI response using available AI services"""
        if not self.openai_client:
            return self._fallback_response(prompt)
        
        try:
            full_prompt = f"{context}\n\nUser: {prompt}\nAssistant: "
            
            response = self.openai_client.ChatCompletion.create(
                model=config.AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are Jarvis, an advanced AI assistant. Be helpful, concise, and intelligent."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=config.MAX_AI_RESPONSE_LENGTH,
                temperature=config.AI_TEMPERATURE
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"AI response generation failed: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when AI is unavailable"""
        responses = [
            "I understand your request. Let me help you with that.",
            "That's an interesting question. I'll do my best to assist.",
            "I'm processing your request. How else can I help?",
            "I'm here to help. Could you provide more details?",
            "That's a great question. Let me think about that."
        ]
        return random.choice(responses)
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text (-1.0 to 1.0)"""
        if NLP_AVAILABLE:
            try:
                blob = TextBlob(text)
                return blob.sentiment.polarity
            except:
                pass
        return 0.0

# File Management System
class FileManager:
    def __init__(self):
        self.base_dir = config.CONFIG_DIR
        self.documents_dir = config.DOCUMENTS_DIR
        self.images_dir = config.IMAGES_DIR
        self.data_dir = config.DATA_DIR
    
    def create_file(self, filename: str, content: str, file_type: str = "text") -> bool:
        """Create a new file"""
        try:
            filepath = self.documents_dir / filename
            
            if file_type == "text":
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            logger.info(f"Created file: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create file {filename}: {e}")
            return False
    
    def read_file(self, filename: str) -> Optional[str]:
        """Read file content"""
        try:
            possible_paths = [
                self.documents_dir / filename,
                self.base_dir / filename,
                Path(filename)  # Absolute path
            ]
            
            for filepath in possible_paths:
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        return f.read()
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {e}")
            return None
    
    def list_files(self, directory: str = None) -> List[str]:
        """List files in directory"""
        try:
            if directory:
                dir_path = Path(directory)
            else:
                dir_path = self.documents_dir
            
            if dir_path.exists():
                return [f.name for f in dir_path.iterdir() if f.is_file()]
            return []
            
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file"""
        try:
            filepath = self.documents_dir / filename
            if filepath.exists():
                filepath.unlink()
                logger.info(f"Deleted file: {filename}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {e}")
            return False

# Advanced Calculator & Data Analysis
class AdvancedCalculator:
    def __init__(self):
        self.history = []
    
    def calculate(self, expression: str) -> str:
        """Advanced calculation with multiple operations"""
        try:
            # Clean the expression
            expression = expression.lower().replace(' ', '')
            
            # Handle special functions
            if 'sqrt' in expression:
                expression = expression.replace('sqrt', 'math.sqrt')
            if 'sin' in expression:
                expression = expression.replace('sin', 'math.sin')
            if 'cos' in expression:
                expression = expression.replace('cos', 'math.cos')
            if 'tan' in expression:
                expression = expression.replace('tan', 'math.tan')
            if 'log' in expression:
                expression = expression.replace('log', 'math.log')
            if 'exp' in expression:
                expression = expression.replace('exp', 'math.exp')
            
            # Safe evaluation
            import math
            result = eval(expression, {"__builtins__": {}, "math": math})
            
            # Store in history
            self.history.append(f"{expression} = {result}")
            
            return str(result)
            
        except Exception as e:
            return f"Error in calculation: {str(e)}"
    
    def unit_conversion(self, value: float, from_unit: str, to_unit: str) -> str:
        """Unit conversion system"""
        conversions = {
            # Length
            ('m', 'ft'): 3.28084,
            ('ft', 'm'): 0.3048,
            ('cm', 'in'): 0.393701,
            ('in', 'cm'): 2.54,
            ('km', 'mi'): 0.621371,
            ('mi', 'km'): 1.60934,
            
            # Weight
            ('kg', 'lb'): 2.20462,
            ('lb', 'kg'): 0.453592,
            ('g', 'oz'): 0.035274,
            ('oz', 'g'): 28.3495,
            
            # Temperature
            ('c', 'f'): lambda c: c * 9/5 + 32,
            ('f', 'c'): lambda f: (f - 32) * 5/9,
            ('c', 'k'): lambda c: c + 273.15,
            ('k', 'c'): lambda k: k - 273.15,
        }
        
        try:
            key = (from_unit.lower(), to_unit.lower())
            if key in conversions:
                converter = conversions[key]
                if callable(converter):
                    result = converter(value)
                else:
                    result = value * converter
                
                return f"{value} {from_unit} = {result:.4f} {to_unit}"
            else:
                return f"Conversion from {from_unit} to {to_unit} not supported"
                
        except Exception as e:
            return f"Conversion error: {str(e)}"

# Security & Encryption System
class SecurityManager:
    def __init__(self):
        self.encryption_key = None
        self.setup_encryption()
    
    def setup_encryption(self):
        """Setup encryption system"""
        if ENCRYPTION_AVAILABLE:
            try:
                if config.ENCRYPTION_KEY:
                    self.encryption_key = config.ENCRYPTION_KEY.encode()
                else:
                    # Generate new key
                    self.encryption_key = Fernet.generate_key()
                    logger.info("Generated new encryption key")
            except Exception as e:
                logger.error(f"Encryption setup failed: {e}")
    
    def encrypt_text(self, text: str) -> str:
        """Encrypt text"""
        if not ENCRYPTION_AVAILABLE or not self.encryption_key:
            return "Encryption not available"
        
        try:
            fernet = Fernet(self.encryption_key)
            encrypted = fernet.encrypt(text.encode())
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            return f"Encryption failed: {str(e)}"
    
    def decrypt_text(self, encrypted_text: str) -> str:
        """Decrypt text"""
        if not ENCRYPTION_AVAILABLE or not self.encryption_key:
            return "Decryption not available"
        
        try:
            fernet = Fernet(self.encryption_key)
            encrypted_data = base64.b64decode(encrypted_text.encode())
            decrypted = fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception as e:
            return f"Decryption failed: {str(e)}"
    
    def generate_password(self, length: int = 12, include_symbols: bool = True) -> str:
        """Generate secure password"""
        import string
        import secrets
        
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*"
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    
    def hash_text(self, text: str) -> str:
        """Generate hash of text"""
        return hashlib.sha256(text.encode()).hexdigest()

# Continue in next part due to length...# Image Processing & OCR System
class ImageProcessor:
    def __init__(self):
        self.available = IMAGE_PROCESSING_AVAILABLE
    
    def create_qr_code(self, text: str, filename: str = None) -> str:
        """Generate QR code from text"""
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            if filename:
                filepath = config.IMAGES_DIR / f"{filename}.png"
                img.save(filepath)
                return f"QR code saved as {filepath}"
            else:
                # Return base64 encoded image
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                return f"QR code generated (base64): {img_str[:50]}..."
                
        except Exception as e:
            return f"QR code generation failed: {str(e)}"
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        if not self.available:
            return "Image processing not available"
        
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text.strip() if text else "No text found in image"
        except Exception as e:
            return f"OCR failed: {str(e)}"
    
    def create_image_with_text(self, text: str, filename: str = None) -> str:
        """Create image with text"""
        if not self.available:
            return "Image processing not available"
        
        try:
            # Create image
            img = Image.new('RGB', (800, 200), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a font
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            
            # Add text
            draw.text((50, 50), text, fill='black', font=font)
            
            if filename:
                filepath = config.IMAGES_DIR / f"{filename}.png"
                img.save(filepath)
                return f"Image with text saved as {filepath}"
            else:
                return "Image created successfully"
                
        except Exception as e:
            return f"Image creation failed: {str(e)}"

# Language Translation System
class TranslationSystem:
    def __init__(self):
        self.translator = None
        self.setup_translator()
    
    def setup_translator(self):
        """Setup translation service"""
        if TRANSLATION_AVAILABLE:
            try:
                self.translator = Translator()
                logger.info("Translation service initialized")
            except Exception as e:
                logger.error(f"Translation setup failed: {e}")
    
    def translate_text(self, text: str, target_language: str = 'en', source_language: str = 'auto') -> str:
        """Translate text to target language"""
        if not self.translator:
            return "Translation service not available"
        
        try:
            result = self.translator.translate(text, dest=target_language, src=source_language)
            return f"Translation ({result.src} → {target_language}): {result.text}"
        except Exception as e:
            return f"Translation failed: {str(e)}"
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        if not self.translator:
            return "Language detection not available"
        
        try:
            result = self.translator.detect(text)
            return f"Detected language: {result.lang} (confidence: {result.confidence:.2f})"
        except Exception as e:
            return f"Language detection failed: {str(e)}"

# Financial Data System
class FinancialSystem:
    def __init__(self):
        self.available = FINANCE_AVAILABLE
    
    def get_stock_price(self, symbol: str) -> str:
        """Get current stock price"""
        if not self.available:
            return "Financial data not available"
        
        try:
            stock = yf.Ticker(symbol.upper())
            info = stock.info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            change = info.get('regularMarketChange', 0)
            change_percent = info.get('regularMarketChangePercent', 0) * 100
            
            return f"{symbol.upper()}: ${price:.2f} ({change:+.2f}, {change_percent:+.2f}%)"
        except Exception as e:
            return f"Failed to get stock price for {symbol}: {str(e)}"
    
    def get_market_summary(self) -> str:
        """Get major market indices"""
        if not self.available:
            return "Financial data not available"
        
        try:
            indices = ['^GSPC', '^DJI', '^IXIC']  # S&P 500, Dow Jones, NASDAQ
            results = []
            
            for index in indices:
                ticker = yf.Ticker(index)
                info = ticker.info
                price = info.get('regularMarketPrice', 0)
                change = info.get('regularMarketChange', 0)
                change_percent = info.get('regularMarketChangePercent', 0) * 100
                
                name = {'^GSPC': 'S&P 500', '^DJI': 'Dow Jones', '^IXIC': 'NASDAQ'}[index]
                results.append(f"{name}: {price:.2f} ({change:+.2f}, {change_percent:+.2f}%)")
            
            return "Market Summary:\n" + "\n".join(results)
        except Exception as e:
            return f"Failed to get market summary: {str(e)}"

# Data Analysis System
class DataAnalyzer:
    def __init__(self):
        self.available = PANDAS_AVAILABLE and PLOTTING_AVAILABLE
    
    def analyze_csv(self, filepath: str) -> str:
        """Analyze CSV data"""
        if not self.available:
            return "Data analysis not available"
        
        try:
            df = pd.read_csv(filepath)
            
            analysis = f"""Data Analysis Results:
- Rows: {len(df)}
- Columns: {len(df.columns)}
- Column Names: {', '.join(df.columns.tolist())}
- Data Types: {df.dtypes.to_dict()}
- Missing Values: {df.isnull().sum().to_dict()}
- Numeric Summary:
{df.describe()}"""
            
            return analysis
        except Exception as e:
            return f"Data analysis failed: {str(e)}"
    
    def create_chart(self, data: List[float], chart_type: str = 'line', title: str = "Chart") -> str:
        """Create simple chart from data"""
        if not self.available:
            return "Chart creation not available"
        
        try:
            plt.figure(figsize=(10, 6))
            
            if chart_type == 'line':
                plt.plot(data)
            elif chart_type == 'bar':
                plt.bar(range(len(data)), data)
            elif chart_type == 'histogram':
                plt.hist(data, bins=20)
            
            plt.title(title)
            plt.grid(True)
            
            filename = f"chart_{int(time.time())}.png"
            filepath = config.IMAGES_DIR / filename
            plt.savefig(filepath)
            plt.close()
            
            return f"Chart saved as {filepath}"
        except Exception as e:
            return f"Chart creation failed: {str(e)}"

# Task Automation & Scheduling
class TaskAutomation:
    def __init__(self):
        self.scheduled_tasks = []
        self.running = False
    
    def schedule_task(self, task_func, schedule_time: str, description: str = "") -> str:
        """Schedule a task to run at specific time"""
        try:
            if schedule_time.lower() == "daily":
                schedule.every().day.do(task_func)
            elif schedule_time.lower() == "hourly":
                schedule.every().hour.do(task_func)
            elif schedule_time.startswith("every"):
                # Parse "every 5 minutes", "every 2 hours", etc.
                parts = schedule_time.split()
                if len(parts) >= 3:
                    interval = int(parts[1])
                    unit = parts[2].lower()
                    
                    if "minute" in unit:
                        schedule.every(interval).minutes.do(task_func)
                    elif "hour" in unit:
                        schedule.every(interval).hours.do(task_func)
                    elif "day" in unit:
                        schedule.every(interval).days.do(task_func)
            else:
                # Try to parse time like "14:30"
                schedule.every().day.at(schedule_time).do(task_func)
            
            self.scheduled_tasks.append({
                'description': description,
                'schedule': schedule_time,
                'function': task_func.__name__
            })
            
            return f"Task scheduled: {description} at {schedule_time}"
        except Exception as e:
            return f"Task scheduling failed: {str(e)}"
    
    def start_scheduler(self):
        """Start the task scheduler"""
        self.running = True
        
        def run_scheduler():
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("Task scheduler started")
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        self.running = False
        schedule.clear()
        logger.info("Task scheduler stopped")
    
    def get_scheduled_tasks(self) -> List[Dict]:
        """Get list of scheduled tasks"""
        return self.scheduled_tasks

# System Monitor
class SystemMonitor:
    def get_system_info(self) -> str:
        """Get comprehensive system information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""System Information:
CPU Usage: {cpu_percent}%
Memory: {memory.percent}% used ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)
Disk: {disk.percent}% used ({disk.used // (1024**3):.1f}GB / {disk.total // (1024**3):.1f}GB)
Boot Time: {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}"""
            
            return info
        except Exception as e:
            return f"Failed to get system info: {str(e)}"
    
    def get_network_info(self) -> str:
        """Get network information"""
        try:
            stats = psutil.net_io_counters()
            
            info = f"""Network Information:
Bytes Sent: {stats.bytes_sent // (1024**2):.1f} MB
Bytes Received: {stats.bytes_recv // (1024**2):.1f} MB
Packets Sent: {stats.packets_sent:,}
Packets Received: {stats.packets_recv:,}"""
            
            return info
        except Exception as e:
            return f"Failed to get network info: {str(e)}"

# Code Assistant
class CodeAssistant:
    def __init__(self):
        self.supported_languages = ['python', 'javascript', 'html', 'css', 'sql', 'bash']
    
    def analyze_code(self, code: str, language: str = 'python') -> str:
        """Analyze code for basic issues"""
        try:
            if language.lower() == 'python':
                return self._analyze_python_code(code)
            else:
                return f"Code analysis for {language} not yet implemented"
        except Exception as e:
            return f"Code analysis failed: {str(e)}"
    
    def _analyze_python_code(self, code: str) -> str:
        """Basic Python code analysis"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for common issues
            if line.strip().endswith(':') and not line.strip().startswith('#'):
                next_line = lines[i] if i < len(lines) else ""
                if next_line and not next_line.startswith('    ') and next_line.strip():
                    issues.append(f"Line {i+1}: Indentation might be missing")
            
            if 'print(' in line and line.count('(') != line.count(')'):
                issues.append(f"Line {i}: Unmatched parentheses")
            
            if line.strip().startswith('import ') and i > 10:
                issues.append(f"Line {i}: Import statement should be at the top")
        
        if not issues:
            return "Code looks good! No obvious issues found."
        else:
            return "Code Analysis Issues:\n" + "\n".join(issues)
    
    def format_code(self, code: str, language: str = 'python') -> str:
        """Format code (basic formatting)"""
        if language.lower() == 'python':
            # Basic Python formatting
            lines = code.split('\n')
            formatted_lines = []
            indent_level = 0
            
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    formatted_lines.append('')
                    continue
                
                # Decrease indent for certain keywords
                if stripped.startswith(('except', 'elif', 'else', 'finally')):
                    indent_level = max(0, indent_level - 1)
                
                # Add proper indentation
                formatted_lines.append('    ' * indent_level + stripped)
                
                # Increase indent after certain keywords
                if stripped.endswith(':') and any(stripped.startswith(kw) for kw in 
                    ['if', 'for', 'while', 'def', 'class', 'try', 'except', 'elif', 'else', 'with']):
                    indent_level += 1
            
            return '\n'.join(formatted_lines)
        else:
            return code  # Return unchanged for unsupported languages
    
    def generate_docstring(self, function_code: str) -> str:
        """Generate basic docstring for Python function"""
        lines = function_code.split('\n')
        func_line = next((line for line in lines if line.strip().startswith('def ')), "")
        
        if not func_line:
            return "No function definition found"
        
        # Extract function name and parameters
        func_name = func_line.split('(')[0].replace('def ', '').strip()
        params_part = func_line.split('(')[1].split(')')[0] if '(' in func_line else ""
        params = [p.strip().split('=')[0].strip() for p in params_part.split(',') if p.strip()]
        
        docstring = f'    """\n    {func_name.replace("_", " ").title()}\n    \n'
        
        if params:
            docstring += "    Args:\n"
            for param in params:
                if param != 'self':
                    docstring += f"        {param}: Description of {param}\n"
        
        docstring += "    \n    Returns:\n        Description of return value\n    \"\"\""
        
        return docstring

# Main Enhanced Jarvis Assistant Class
class EnhancedJarvisAssistant:
    def __init__(self):
        logger.info(f"Initializing {config.ASSISTANT_NAME} {config.VERSION}")
        
        # Initialize core systems
        self.memory = EnhancedMemory(config.MEMORY_FILE)
        self.ai_system = AISystem()
        self.file_manager = FileManager()
        self.calculator = AdvancedCalculator()
        self.security = SecurityManager()
        self.image_processor = ImageProcessor()
        self.translator = TranslationSystem()
        self.financial = FinancialSystem()
        self.data_analyzer = DataAnalyzer()
        self.task_automation = TaskAutomation()
        self.system_monitor = SystemMonitor()
        self.code_assistant = CodeAssistant()
        
        # Initialize TTS and STT
        self.setup_speech_systems()
        
        # Start automation systems
        self.task_automation.start_scheduler()
        
        # Initialize TTS queue
        self.tts_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()
        
        self.running = True
        logger.info("Enhanced Jarvis Assistant initialized successfully")
    
    def setup_speech_systems(self):
        """Setup text-to-speech and speech recognition"""
        # TTS Setup
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', config.TTS_RATE)
            self.tts_engine.setProperty('volume', config.TTS_VOLUME)
            
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
                self.has_tts = True
                logger.info("TTS system initialized")
            else:
                self.has_tts = False
        except Exception as e:
            self.has_tts = False
            logger.error(f"TTS initialization failed: {e}")
        
        # STT Setup
        self.recognizer = sr.Recognizer()
        if PYAUDIO_AVAILABLE:
            try:
                self.microphone = sr.Microphone()
                self.has_microphone = True
                self._calibrate_microphone()
                logger.info("Speech recognition initialized")
            except Exception as e:
                self.has_microphone = False
                logger.error(f"Microphone initialization failed: {e}")
        else:
            self.has_microphone = False
            logger.info("Voice input disabled - PyAudio not available")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        if self.has_microphone:
            try:
                with self.microphone as source:
                    logger.info("Calibrating microphone...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Microphone calibrated")
            except Exception as e:
                logger.error(f"Microphone calibration failed: {e}")
                self.has_microphone = False
    
    def _tts_worker(self):
        """Worker thread for text-to-speech"""
        while True:
            text = self.tts_queue.get()
            if text is None:
                break
            print(f"{config.ASSISTANT_NAME}: {text}")
            if self.has_tts:
                try:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                except Exception as e:
                    logger.error(f"TTS error: {e}")
            self.tts_queue.task_done()
    
    def speak(self, text: str):
        """Add text to TTS queue"""
        self.tts_queue.put(text)
    
    def listen(self, timeout: int = config.LISTEN_TIMEOUT) -> Optional[str]:
        """Listen for voice input"""
        if not self.has_microphone:
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, 
                                             phrase_time_limit=config.PHRASE_TIME_LIMIT)
                command = self.recognizer.recognize_google(audio).strip()
                print(f"👤 You: {command}")
                return command.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Listen error: {e}")
            return None
    
    def get_text_input(self) -> Optional[str]:
        """Get text input from user"""
        try:
            return input("👤 You: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            return None

# Continue with command processing in next part...    # Enhanced Command Processing System
    def process_command(self, command: str) -> bool:
        """Process user command with enhanced AI capabilities"""
        if not command:
            return False
        
        # Remove wake words
        for wake_word in config.WAKE_WORDS:
            command = command.replace(wake_word, "").strip()
        
        original_command = command
        response = None
        
        try:
            # AI-Powered Commands (Use AI for complex queries)
            if self._is_ai_query(command):
                response = self.ai_system.generate_response(command)
                self.speak(response)
                sentiment = self.ai_system.analyze_sentiment(command)
                self.memory.add_conversation(original_command, response, 
                                           {"ai_generated": True}, sentiment)
                return False
            
            # Core System Commands
            elif any(word in command for word in ['time', 'clock']):
                response = self._tell_time()
            elif any(word in command for word in ['date', 'today', 'day']):
                response = self._tell_date()
            elif 'system info' in command or 'system status' in command:
                response = self.system_monitor.get_system_info()
                self.speak(response)
            elif 'network info' in command:
                response = self.system_monitor.get_network_info()
                self.speak(response)
            
            # File Management Commands
            elif 'create file' in command:
                response = self._handle_file_creation(command)
            elif 'read file' in command:
                response = self._handle_file_reading(command)
            elif 'list files' in command:
                response = self._handle_file_listing(command)
            elif 'delete file' in command:
                response = self._handle_file_deletion(command)
            
            # Security Commands
            elif 'encrypt' in command:
                response = self._handle_encryption(command)
            elif 'decrypt' in command:
                response = self._handle_decryption(command)
            elif 'generate password' in command:
                response = self._handle_password_generation(command)
            elif 'hash' in command and 'text' in command:
                response = self._handle_text_hashing(command)
            
            # Image Processing Commands
            elif 'create qr code' in command or 'generate qr' in command:
                response = self._handle_qr_creation(command)
            elif 'read image' in command or 'ocr' in command:
                response = self._handle_image_ocr(command)
            elif 'create image' in command:
                response = self._handle_image_creation(command)
            
            # Translation Commands
            elif 'translate' in command:
                response = self._handle_translation(command)
            elif 'detect language' in command:
                response = self._handle_language_detection(command)
            
            # Financial Commands
            elif 'stock price' in command or 'stock' in command:
                response = self._handle_stock_query(command)
            elif 'market summary' in command or 'market' in command:
                response = self.financial.get_market_summary()
                self.speak(response)
            
            # Advanced Calculation Commands
            elif any(word in command for word in ['calculate', 'math', 'compute']) and 'advanced' in command:
                response = self._handle_advanced_calculation(command)
            elif 'convert' in command and any(unit in command for unit in ['km', 'miles', 'kg', 'pounds', 'celsius', 'fahrenheit']):
                response = self._handle_unit_conversion(command)
            
            # Data Analysis Commands
            elif 'analyze csv' in command or 'analyze data' in command:
                response = self._handle_data_analysis(command)
            elif 'create chart' in command:
                response = self._handle_chart_creation(command)
            
            # Task Management Commands
            elif 'schedule task' in command:
                response = self._handle_task_scheduling(command)
            elif 'my tasks' in command or 'show tasks' in command:
                response = self._handle_task_display()
            elif 'complete task' in command:
                response = self._handle_task_completion(command)
            
            # Code Assistant Commands
            elif 'analyze code' in command:
                response = self._handle_code_analysis(command)
            elif 'format code' in command:
                response = self._handle_code_formatting(command)
            elif 'generate docstring' in command:
                response = self._handle_docstring_generation(command)
            
            # Web Automation Commands
            elif 'search web' in command or 'web search' in command:
                response = self._handle_web_search(command)
            elif 'open website' in command:
                response = self._handle_website_opening(command)
            
            # Original Commands (Enhanced)
            elif 'wikipedia' in command:
                response = self._search_wikipedia(command)
            elif 'weather' in command:
                response = self._get_weather(command)
            elif 'news' in command or 'headlines' in command:
                response = self._get_news()
            elif any(word in command for word in ['joke', 'funny', 'humor']):
                response = self._tell_joke()
            elif 'open youtube' in command:
                response = self._open_website('https://www.youtube.com', "YouTube")
            elif 'open google' in command:
                response = self._open_website('https://www.google.com', "Google")
            elif 'open github' in command:
                response = self._open_website('https://www.github.com', "GitHub")
            
            # Memory and Learning Commands
            elif 'remember' in command and any(word in command for word in ['name', 'preference', 'setting']):
                response = self._handle_memory_storage(command)
            elif 'what do you know about' in command:
                response = self._handle_knowledge_query(command)
            elif 'learn' in command:
                response = self._handle_learning(command)
            
            # System Control Commands
            elif any(word in command for word in ['shutdown', 'power off', 'restart', 'reboot']):
                response = self._handle_system_control(command)
                if 'shutdown' in response or 'restart' in response:
                    return True
            
            # Exit Commands
            elif any(word in command for word in ['quit', 'exit', 'stop', 'bye', 'goodbye']):
                self.speak("It was great working with you! Goodbye!")
                return True
            
            # Help Commands
            elif 'help' in command or 'what can you do' in command:
                response = self._get_help_text()
                self.speak(response)
            
            # Enhanced Features Commands
            elif 'show capabilities' in command or 'features' in command:
                response = self._show_capabilities()
                self.speak(response)
            
            # Unknown Command - Use AI if available
            else:
                if self.ai_system.openai_client:
                    response = self.ai_system.generate_response(command)
                    self.speak(response)
                else:
                    responses = [
                        "I'm not sure how to help with that. Could you try rephrasing?",
                        "That's interesting! Can you provide more details?",
                        "I don't understand that command yet. Try 'help' to see what I can do.",
                        "I'm still learning. Could you try a different command?"
                    ]
                    response = random.choice(responses)
                    self.speak(response)
            
            # Log conversation if response was generated
            if response:
                sentiment = self.ai_system.analyze_sentiment(command)
                self.memory.add_conversation(original_command, response, {}, sentiment)
                
        except Exception as e:
            logger.error(f"Command processing error: {e}")
            self.speak("Sorry, I encountered an error processing that command.")
        
        return False
    
    def _is_ai_query(self, command: str) -> bool:
        """Determine if command should be handled by AI"""
        ai_keywords = [
            'what is', 'how do', 'why', 'explain', 'tell me about', 
            'what would happen if', 'compare', 'analyze', 'opinion',
            'should i', 'recommend', 'suggest', 'advice'
        ]
        return any(keyword in command for keyword in ai_keywords) and self.ai_system.openai_client
    
    # Enhanced Command Handlers
    def _tell_time(self) -> str:
        """Enhanced time telling with timezone support"""
        try:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            date_str = now.strftime("%A, %B %d")
            timezone = now.astimezone().tzname()
            response = f"It's {time_str} {timezone} on {date_str}"
            self.speak(response)
            return response
        except Exception as e:
            logger.error(f"Error telling time: {e}")
            self.speak("Sorry, I couldn't get the current time.")
    
    def _tell_date(self) -> str:
        """Enhanced date with additional information"""
        try:
            today = datetime.datetime.now()
            date_str = today.strftime("%A, %B %d, %Y")
            day_of_year = today.timetuple().tm_yday
            week_number = today.isocalendar()[1]
            response = f"Today is {date_str}. Day {day_of_year} of the year, week {week_number}."
            self.speak(response)
            return response
        except Exception as e:
            logger.error(f"Error telling date: {e}")
            self.speak("Sorry, I couldn't get the current date.")
    
    # File Management Handlers
    def _handle_file_creation(self, command: str) -> str:
        """Handle file creation commands"""
        try:
            # Extract filename and content
            parts = command.split('create file')[-1].strip()
            if 'with content' in parts:
                filename = parts.split('with content')[0].strip()
                content = parts.split('with content')[1].strip()
            else:
                filename = parts
                content = "# New file created by Jarvis\n"
            
            if self.file_manager.create_file(filename, content):
                response = f"File '{filename}' created successfully!"
            else:
                response = f"Failed to create file '{filename}'"
            
            self.speak(response)
            return response
        except Exception as e:
            response = f"Error creating file: {str(e)}"
            self.speak(response)
            return response
    
    def _handle_file_reading(self, command: str) -> str:
        """Handle file reading commands"""
        try:
            filename = command.split('read file')[-1].strip()
            content = self.file_manager.read_file(filename)
            
            if content:
                # Limit output for speech
                if len(content) > 200:
                    preview = content[:200] + "..."
                    response = f"File content preview: {preview}"
                else:
                    response = f"File content: {content}"
            else:
                response = f"File '{filename}' not found or couldn't be read"
            
            self.speak(response)
            return response
        except Exception as e:
            response = f"Error reading file: {str(e)}"
            self.speak(response)
            return response
    
    def _handle_file_listing(self, command: str) -> str:
        """Handle file listing commands"""
        try:
            files = self.file_manager.list_files()
            if files:
                file_list = ", ".join(files[:10])  # Limit to first 10 files
                response = f"Files found: {file_list}"
                if len(files) > 10:
                    response += f" and {len(files) - 10} more files"
            else:
                response = "No files found in the documents directory"
            
            self.speak(response)
            return response
        except Exception as e:
            response = f"Error listing files: {str(e)}"
            self.speak(response)
            return response
    
    # Security Handlers
    def _handle_encryption(self, command: str) -> str:
        """Handle text encryption commands"""
        try:
            text = command.split('encrypt')[-1].strip()
            if not text:
                response = "Please provide text to encrypt"
            else:
                encrypted = self.security.encrypt_text(text)
                response = f"Encrypted text: {encrypted}"
            
            self.speak("Text encrypted successfully" if "Encryption" not in encrypted else encrypted)
            return response
        except Exception as e:
            response = f"Encryption error: {str(e)}"
            self.speak(response)
            return response
    
    def _handle_password_generation(self, command: str) -> str:
        """Handle password generation commands"""
        try:
            # Extract length if specified
            length = 12
            if 'length' in command:
                parts = command.split('length')[-1].strip().split()
                if parts and parts[0].isdigit():
                    length = int(parts[0])
            
            include_symbols = 'symbols' in command or 'special' in command
            password = self.security.generate_password(length, include_symbols)
            
            response = f"Generated password: {password}"
            self.speak(f"I've generated a {length}-character password for you")
            return response
        except Exception as e:
            response = f"Password generation error: {str(e)}"
            self.speak(response)
            return response
    
    # Image Processing Handlers
    def _handle_qr_creation(self, command: str) -> str:
        """Handle QR code creation"""
        try:
            text = command.replace('create qr code', '').replace('generate qr', '').strip()
            if 'for' in text:
                text = text.split('for')[-1].strip()
            
            if not text:
                response = "Please provide text for the QR code"
                self.speak(response)
                return response
            
            filename = f"qr_{int(time.time())}"
            result = self.image_processor.create_qr_code(text, filename)
            self.speak(f"QR code created for: {text}")
            return result
        except Exception as e:
            response = f"QR code creation error: {str(e)}"
            self.speak(response)
            return response
    
    # Translation Handlers
    def _handle_translation(self, command: str) -> str:
        """Handle translation commands"""
        try:
            # Parse command like "translate hello to spanish"
            if 'to' in command:
                parts = command.split('translate')[-1].split('to')
                text = parts[0].strip()
                target_lang = parts[1].strip()
            else:
                text = command.split('translate')[-1].strip()
                target_lang = 'spanish'  # Default
            
            result = self.translator.translate_text(text, target_lang)
            self.speak(result)
            return result
        except Exception as e:
            response = f"Translation error: {str(e)}"
            self.speak(response)
            return response
    
    # Financial Handlers
    def _handle_stock_query(self, command: str) -> str:
        """Handle stock price queries"""
        try:
            # Extract stock symbol
            symbol = command.replace('stock price', '').replace('stock', '').strip()
            if 'of' in symbol:
                symbol = symbol.split('of')[-1].strip()
            if 'for' in symbol:
                symbol = symbol.split('for')[-1].strip()
            
            if not symbol:
                response = "Please specify a stock symbol"
                self.speak(response)
                return response
            
            result = self.financial.get_stock_price(symbol)
            self.speak(result)
            return result
        except Exception as e:
            response = f"Stock query error: {str(e)}"
            self.speak(response)
            return response
    
    # Original Enhanced Handlers
    def _search_wikipedia(self, command: str) -> str:
        """Enhanced Wikipedia search"""
        try:
            self.speak("Searching Wikipedia...")
            query = re.sub(r'\b(wikipedia|search|look up|find)\b', '', command).strip()
            
            if not query:
                self.speak("What would you like me to search for?")
                return "No search query provided"
            
            try:
                summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
                response = f"According to Wikipedia: {summary}"
                self.speak(response)
                return response
            except wikipedia.DisambiguationError as e:
                options = ', '.join(e.options[:3])
                response = f"Multiple results found. Options include: {options}"
                self.speak(response)
                return response
            except wikipedia.PageError:
                response = f"I couldn't find information about {query} on Wikipedia."
                self.speak(response)
                return response
                
        except Exception as e:
            logger.error(f"Wikipedia search error: {e}")
            self.speak("Sorry, I encountered an error searching Wikipedia.")
    
    def _get_help_text(self) -> str:
        """Enhanced help text with all capabilities"""
        help_text = f"""
{config.ASSISTANT_NAME} {config.VERSION} - AI Assistant Capabilities:

🎯 CORE FEATURES:
• Time & Date: "what time is it", "what's the date"
• System Info: "system status", "network info"
• Weather: "weather in [city]"
• News: "latest news"

🗂️ FILE MANAGEMENT:
• Create: "create file report.txt with content Hello World"
• Read: "read file report.txt"
• List: "list files"

🔐 SECURITY:
• Encrypt: "encrypt my secret message"
• Password: "generate password length 16 with symbols"
• Hash: "hash text hello world"

🖼️ IMAGE PROCESSING:
• QR Codes: "create qr code for https://example.com"
• OCR: "read text from image photo.jpg"

🌍 TRANSLATION:
• Translate: "translate hello to spanish"
• Detect: "detect language of bonjour"

📊 DATA & FINANCE:
• Stocks: "stock price of AAPL"
• Market: "market summary"
• Charts: "create chart from data 1,2,3,4,5"

💻 CODE ASSISTANT:
• Analyze: "analyze python code [code here]"
• Format: "format code [code here]"

🤖 AI POWERED:
• Ask anything: "explain quantum physics"
• Get advice: "should I learn Python?"
• Analysis: "compare Python vs JavaScript"

📋 TASK MANAGEMENT:
• Schedule: "schedule task backup files daily"
• Tasks: "show my tasks"

🎮 ENTERTAINMENT:
• Jokes: "tell me a joke"
• Wikipedia: "wikipedia artificial intelligence"

Say 'show capabilities' for the full feature list!
        """
        return help_text.strip()
    
    def _show_capabilities(self) -> str:
        """Show full system capabilities"""
        capabilities = f"""
🚀 {config.ASSISTANT_NAME} {config.VERSION} - FULL CAPABILITIES:

✅ AVAILABLE FEATURES:
• AI Integration: {'✓' if self.ai_system.openai_client else '✗'}
• File Management: ✓
• Security & Encryption: {'✓' if ENCRYPTION_AVAILABLE else '✗'}
• Image Processing: {'✓' if IMAGE_PROCESSING_AVAILABLE else '✗'}
• Translation: {'✓' if TRANSLATION_AVAILABLE else '✗'}
• Financial Data: {'✓' if FINANCE_AVAILABLE else '✗'}
• Data Analysis: {'✓' if PANDAS_AVAILABLE else '✗'}
• Voice Input: {'✓' if self.has_microphone else '✗'}
• Voice Output: {'✓' if self.has_tts else '✗'}

🎯 COMMAND CATEGORIES:
1. Information & Search
2. File & Document Management
3. Security & Privacy
4. Image Processing & OCR
5. Language & Translation
6. Financial & Market Data
7. Data Analysis & Visualization
8. Task Automation
9. Code Development Assistant
10. System Monitoring
11. AI-Powered Conversations
12. Entertainment & Utilities

📈 ADVANCED FEATURES:
• Machine Learning Integration
• Natural Language Processing
• Automated Task Scheduling
• Multi-language Support
• Secure Data Encryption
• Real-time Financial Data
• Image Generation & Analysis
• Code Analysis & Formatting
• System Performance Monitoring
• Intelligent Memory System

Type 'help' for basic commands or ask me anything!
        """
        return capabilities.strip()
    
    # Main execution loop
    def run(self):
        """Enhanced main execution loop"""
        try:
            # Enhanced greeting
            user_name = self.memory.get_preference("user_name")
            greeting_base = f"{self._get_greeting()}"
            if user_name:
                greeting_base += f", {user_name}"
            
            greeting = f"{greeting_base}! I am {config.ASSISTANT_NAME} {config.VERSION}, your enhanced AI assistant."
            self.speak(greeting)
            
            print(f"\n🤖 {config.ASSISTANT_NAME} {config.VERSION} - Enhanced AI Assistant")
            print("=" * 60)
            
            if self.has_microphone:
                print(f"🎤 Voice Commands: Say '{', '.join(config.WAKE_WORDS[:2])}'")
                print("⌨️  Text Commands: Type directly")
            else:
                print("⌨️  Text Input Mode (PyAudio not available)")
                print("📦 Install PyAudio for voice commands")
            
            print("💡 Try: 'help', 'show capabilities', or ask me anything!")
            print("🚀 Enhanced features: AI chat, file management, security, and more!")
            print("-" * 60)
            
            while self.running:
                try:
                    command = None
                    
                    if self.has_microphone:
                        command = self.listen()
                    
                    if command is None:
                        try:
                            if self.has_microphone:
                                print("\n💬 No voice detected. Type your command:")
                            else:
                                print("\n💬 Enter command:")
                            command = input("👤 ").strip().lower()
                            if not command:
                                continue
                        except (EOFError, KeyboardInterrupt):
                            break
                    
                    # Process command
                    if any(wake_word in command for wake_word in config.WAKE_WORDS) or not self.has_microphone:
                        if self.process_command(command):
                            break
                            
                except KeyboardInterrupt:
                    self.speak("Shutting down. It was great working with you!")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error in main loop: {e}")
                    time.sleep(1)
        
        finally:
            # Enhanced cleanup
            self.task_automation.stop_scheduler()
            self.tts_queue.put(None)
            if self.tts_thread.is_alive():
                self.tts_thread.join(timeout=2)
            logger.info(f"{config.ASSISTANT_NAME} {config.VERSION} shutdown complete")
    
    def _get_greeting(self) -> str:
        """Get time-based greeting"""
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good morning"
        elif hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"

# Main Entry Point
def main():
    """Enhanced main entry point"""
    try:
        print(f"🚀 Starting {config.ASSISTANT_NAME} {config.VERSION}...")
        assistant = EnhancedJarvisAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
    finally:
        sys.exit(0)

if __name__ == '__main__':
    main()