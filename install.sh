#!/bin/bash

# Jarvis AI Assistant Installation Script
# For Ubuntu/Debian systems

set -e  # Exit on any error

echo "🤖 Jarvis AI Assistant Installation Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on supported system
check_system() {
    print_status "Checking system compatibility..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            print_success "Ubuntu/Debian system detected"
        else
            print_error "This script is designed for Ubuntu/Debian systems with apt-get"
            exit 1
        fi
    else
        print_warning "This script is optimized for Linux. Manual installation may be required."
    fi
}

# Check Python version
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_success "Python $PYTHON_VERSION found"
        
        # Check if version is 3.7 or higher
        if python3 -c 'import sys; exit(0 if sys.version_info >= (3,7) else 1)'; then
            print_success "Python version is compatible (≥3.7)"
        else
            print_error "Python 3.7 or higher is required. Current version: $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3.7 or higher."
        exit 1
    fi
}

# Install system dependencies
install_system_deps() {
    print_status "Installing system dependencies..."
    
    print_status "Updating package lists..."
    sudo apt-get update
    
    print_status "Installing build essentials and audio libraries..."
    sudo apt-get install -y \
        build-essential \
        portaudio19-dev \
        python3-pyaudio \
        python3-pip \
        python3-dev \
        libasound2-dev \
        espeak \
        espeak-data \
        libespeak1 \
        libespeak-dev \
        festival \
        festvox-kallpc16k \
        alsa-utils \
        pulseaudio
    
    print_success "System dependencies installed"
}

# Install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip
    print_status "Upgrading pip..."
    python3 -m pip install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        print_status "Installing from requirements.txt..."
        python3 -m pip install -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "requirements.txt not found. Installing core dependencies manually..."
        python3 -m pip install \
            SpeechRecognition==3.10.0 \
            pyttsx3==2.90 \
            pyaudio==0.2.11 \
            requests==2.31.0 \
            wikipedia==1.4.0 \
            pyjokes==0.6.0 \
            wolframalpha==5.0.0 \
            python-dotenv==1.0.0
        print_success "Core dependencies installed"
    fi
}

# Setup configuration
setup_config() {
    print_status "Setting up configuration..."
    
    if [[ -f ".env.example" ]] && [[ ! -f ".env" ]]; then
        cp .env.example .env
        print_success "Created .env file from template"
        print_warning "Please edit .env file and add your API keys before running Jarvis"
    elif [[ -f ".env" ]]; then
        print_success ".env file already exists"
    else
        print_warning "No .env.example found. You'll need to create a .env file manually"
    fi
}

# Test microphone
test_microphone() {
    print_status "Testing microphone access..."
    
    if command -v arecord &> /dev/null; then
        print_status "Recording a 2-second test (speak now)..."
        timeout 2s arecord -f cd -t wav /dev/null 2>/dev/null || {
            print_warning "Microphone test failed. You may need to configure audio permissions."
            print_status "Try running: sudo usermod -a -G audio $USER"
            print_status "Then log out and log back in."
        }
        print_success "Microphone test completed"
    else
        print_warning "Cannot test microphone (arecord not available)"
    fi
}

# Create desktop shortcut (optional)
create_shortcut() {
    read -p "Create desktop shortcut? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        DESKTOP_FILE="$HOME/Desktop/Jarvis.desktop"
        CURRENT_DIR=$(pwd)
        
        cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Jarvis AI Assistant
Comment=Voice-controlled AI assistant
Exec=python3 "$CURRENT_DIR/jarvis.py"
Icon=utilities-terminal
Terminal=true
Path=$CURRENT_DIR
Categories=Utility;
EOF
        
        chmod +x "$DESKTOP_FILE"
        print_success "Desktop shortcut created: $DESKTOP_FILE"
    fi
}

# Main installation process
main() {
    echo "Starting installation process..."
    echo ""
    
    check_system
    check_python
    install_system_deps
    install_python_deps
    setup_config
    test_microphone
    create_shortcut
    
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit the .env file and add your API keys:"
    echo "   - OpenWeather API: https://openweathermap.org/api"
    echo "   - Wolfram Alpha API: https://developer.wolframalpha.com/"
    echo "   - News API: https://newsapi.org/"
    echo ""
    echo "2. Run Jarvis:"
    echo "   python3 jarvis.py"
    echo ""
    echo "3. Say 'Hey Jarvis' or type commands to interact!"
    echo ""
    print_success "Happy chatting with Jarvis! 🤖✨"
}

# Run main function
main "$@"