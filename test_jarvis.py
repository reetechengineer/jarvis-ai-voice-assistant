#!/usr/bin/env python3
"""
Jarvis AI Assistant - Test Script
Tests all components and dependencies to ensure proper installation
"""

import sys
import os
import platform
from pathlib import Path
import importlib

def print_header():
    print("🤖 Jarvis AI Assistant - Test Suite")
    print("=" * 50)
    print()

def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m", 
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    
    color = colors.get(status, colors["INFO"])
    reset = colors["RESET"]
    print(f"{color}[{status}]{reset} {message}")

def test_python_version():
    """Test Python version compatibility"""
    print_status("Testing Python version...")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version >= (3, 7):
        print_status(f"Python {version_str} - Compatible ✓", "SUCCESS")
        return True
    else:
        print_status(f"Python {version_str} - Requires 3.7+ ✗", "ERROR")
        return False

def test_import(module_name, package_name=None, optional=False):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        display_name = package_name or module_name
        print_status(f"{display_name} - Available ✓", "SUCCESS")
        return True
    except ImportError as e:
        display_name = package_name or module_name
        status = "WARNING" if optional else "ERROR"
        symbol = "⚠" if optional else "✗"
        print_status(f"{display_name} - Missing {symbol}", status)
        if not optional:
            print_status(f"  Error: {e}", "ERROR")
        return False

def test_dependencies():
    """Test all required and optional dependencies"""
    print_status("Testing dependencies...")
    
    # Required dependencies
    required_deps = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyttsx3", "pyttsx3"),
        ("requests", "requests"),
        ("wikipedia", "wikipedia"),
        ("pyjokes", "pyjokes"),
        ("datetime", "datetime"),
        ("threading", "threading"),
        ("queue", "queue"),
        ("json", "json"),
        ("re", "re"),
        ("logging", "logging"),
        ("pathlib", "pathlib"),
    ]
    
    # Optional dependencies
    optional_deps = [
        ("pyaudio", "PyAudio"),
        ("wolframalpha", "wolframalpha"),
        ("smtplib", "smtplib"),
        ("dotenv", "python-dotenv"),
        ("webbrowser", "webbrowser"),
    ]
    
    success_count = 0
    total_required = len(required_deps)
    
    print_status("Required dependencies:")
    for module, package in required_deps:
        if test_import(module, package):
            success_count += 1
    
    print_status("Optional dependencies:")
    for module, package in optional_deps:
        test_import(module, package, optional=True)
    
    print()
    if success_count == total_required:
        print_status(f"All required dependencies available ({success_count}/{total_required})", "SUCCESS")
        return True
    else:
        print_status(f"Missing dependencies ({success_count}/{total_required})", "ERROR")
        return False

def test_audio_system():
    """Test audio system components"""
    print_status("Testing audio system...")
    
    # Test PyAudio
    try:
        import pyaudio
        pa = pyaudio.PyAudio()
        device_count = pa.get_device_count()
        print_status(f"PyAudio - {device_count} audio devices found ✓", "SUCCESS")
        
        # List microphones
        mic_found = False
        for i in range(device_count):
            info = pa.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                mic_found = True
                break
        
        if mic_found:
            print_status("Microphone devices detected ✓", "SUCCESS")
        else:
            print_status("No microphone devices found ⚠", "WARNING")
            
        pa.terminate()
        return True
        
    except ImportError:
        print_status("PyAudio not available - Voice input will not work ✗", "ERROR")
        return False
    except Exception as e:
        print_status(f"Audio system error: {e} ⚠", "WARNING")
        return False

def test_tts():
    """Test text-to-speech system"""
    print_status("Testing text-to-speech...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if voices:
            print_status(f"TTS - {len(voices)} voices available ✓", "SUCCESS")
            return True
        else:
            print_status("TTS - No voices found ⚠", "WARNING")
            return False
            
    except Exception as e:
        print_status(f"TTS error: {e} ✗", "ERROR")
        return False

def test_config():
    """Test configuration files"""
    print_status("Testing configuration...")
    
    config_files = {
        ".env.example": "Environment template",
        "requirements.txt": "Dependencies list",
        "jarvis.py": "Main application"
    }
    
    all_good = True
    for file_path, description in config_files.items():
        if Path(file_path).exists():
            print_status(f"{description} - Found ✓", "SUCCESS")
        else:
            print_status(f"{description} - Missing ✗", "ERROR")
            all_good = False
    
    # Check .env file
    if Path(".env").exists():
        print_status("Environment file (.env) - Found ✓", "SUCCESS")
    else:
        print_status("Environment file (.env) - Not configured ⚠", "WARNING")
        print_status("  Copy .env.example to .env and add your API keys", "INFO")
    
    return all_good

def test_internet_connection():
    """Test internet connectivity"""
    print_status("Testing internet connection...")
    
    try:
        import requests
        response = requests.get("https://httpbin.org/ip", timeout=5)
        if response.status_code == 200:
            print_status("Internet connection - Available ✓", "SUCCESS")
            return True
        else:
            print_status("Internet connection - Issues detected ⚠", "WARNING")
            return False
    except Exception as e:
        print_status("Internet connection - Not available ✗", "ERROR")
        return False

def test_api_keys():
    """Test API key configuration"""
    print_status("Testing API key configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print_status("python-dotenv not available - Cannot test API keys", "WARNING")
        return False
    
    api_keys = {
        "OPENWEATHER_API_KEY": "OpenWeather API",
        "WOLFRAM_ALPHA_API_KEY": "Wolfram Alpha API", 
        "NEWS_API_KEY": "News API",
        "EMAIL_ADDRESS": "Email configuration",
        "EMAIL_PASSWORD": "Email password"
    }
    
    configured_count = 0
    for key, description in api_keys.items():
        value = os.getenv(key)
        if value and value != f"your_{key.lower()}_here" and value != "your_email@gmail.com":
            print_status(f"{description} - Configured ✓", "SUCCESS")
            configured_count += 1
        else:
            print_status(f"{description} - Not configured ⚠", "WARNING")
    
    if configured_count > 0:
        print_status(f"{configured_count} API keys configured", "INFO")
    else:
        print_status("No API keys configured - Limited functionality", "WARNING")
    
    return configured_count > 0

def run_basic_test():
    """Run a basic functionality test"""
    print_status("Running basic functionality test...")
    
    try:
        # Test basic imports and initialization
        sys.path.append('.')
        
        # This is a simple test - just check if main components load
        print_status("Testing core components...")
        
        # Test datetime functionality
        import datetime
        now = datetime.datetime.now()
        print_status(f"Current time: {now.strftime('%H:%M:%S')} ✓", "SUCCESS")
        
        # Test JSON functionality
        import json
        test_data = {"test": "success"}
        json_str = json.dumps(test_data)
        print_status("JSON functionality - Working ✓", "SUCCESS")
        
        return True
        
    except Exception as e:
        print_status(f"Basic test failed: {e} ✗", "ERROR")
        return False

def print_summary(results):
    """Print test summary"""
    print()
    print("=" * 50)
    print("🔍 Test Summary")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        color = "\033[92m" if passed else "\033[91m"
        print(f"{color}[{status}]\033[0m {test_name}")
    
    print()
    print(f"Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print_status("🎉 All tests passed! Jarvis should work correctly.", "SUCCESS")
    elif passed_tests >= total_tests * 0.7:
        print_status("⚠️  Most tests passed. Jarvis should work with limited functionality.", "WARNING")
    else:
        print_status("❌ Many tests failed. Please check your installation.", "ERROR")
    
    print()
    print("Next steps:")
    print("1. If tests failed, run: pip install -r requirements.txt")
    print("2. Configure API keys in .env file")
    print("3. Run Jarvis: python3 jarvis.py")

def main():
    """Main test function"""
    print_header()
    
    # Run all tests
    results = {
        "Python Version": test_python_version(),
        "Dependencies": test_dependencies(),
        "Audio System": test_audio_system(),
        "Text-to-Speech": test_tts(),
        "Configuration": test_config(),
        "Internet Connection": test_internet_connection(),
        "API Keys": test_api_keys(),
        "Basic Functionality": run_basic_test()
    }
    
    print_summary(results)

if __name__ == "__main__":
    main()