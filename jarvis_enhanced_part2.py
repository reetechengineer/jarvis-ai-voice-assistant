# Image Processing & OCR System
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

# Continue with command processing in next part...