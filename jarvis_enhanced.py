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

# Continue in next part due to length...