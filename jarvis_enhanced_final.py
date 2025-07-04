    # Enhanced Command Processing System
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