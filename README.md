# NetSwitch v1.0

🌐 **A modern, secure DNS management tool for Windows with an intuitive GUI**

![NetSwitch](https://img.shields.io/badge/NetSwitch-v1.0-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11.9+-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage](#usage)
- [DNS Providers](#dns-providers)
- [Security Features](#security-features)
- [Technical Requirements](#technical-requirements)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

NetSwitch is a comprehensive DNS management application built with Python and CustomTkinter that provides an easy-to-use interface for switching between different DNS providers, managing network adapters, and optimizing internet connectivity on Windows systems.

### Why NetSwitch?

- **🎨 Modern UI**: Beautiful, responsive interface with light/dark theme support
- **🔒 Enhanced Security**: Comprehensive input sanitization and validation
- **⚡ Performance Focused**: Built-in DNS speed testing and optimization
- **🌐 IPv4 & IPv6 Support**: Full support for both IP protocols
- **🛡️ Safe Operations**: Prevents command injection and malicious inputs
- **🎯 User-Friendly**: Intuitive design inspired by DNS Jumper

## ✨ Features

### Core Functionality
- **🔄 DNS Switching**: Quickly switch between popular DNS providers
- **📡 Network Adapter Detection**: Automatic detection of available network interfaces
- **🧹 DNS Cache Management**: Flush DNS cache with one click
- **⚡ Speed Testing**: Find the fastest DNS server for your connection
- **🎛️ Custom DNS**: Support for custom DNS server configurations

### Security & Validation
- **🛡️ Input Sanitization**: Comprehensive sanitization of all user inputs
- **✅ IP Validation**: Enhanced IPv4 and IPv6 address validation
- **🚫 Injection Prevention**: Protection against command injection attacks
- **⏱️ Timeout Protection**: Prevents hanging operations with timeout controls
- **🔍 Error Handling**: Robust error handling with user-friendly messages

### User Interface
- **🎨 Modern Design**: Clean, professional interface using CustomTkinter
- **🌙 Theme Support**: Light and dark mode themes
- **🟣 Custom Branding**: Purple NetSwitch branding with light grey background
- **🔴 Clear Actions**: Red exit button for clear visual distinction
- **📊 Status Updates**: Real-time status bar with operation feedback

### Advanced Features
- **🌐 IPv6 Support**: Full IPv6 DNS configuration support
- **🔧 Options Panel**: Customizable settings for themes and display
- **🧵 Threaded Operations**: Non-blocking operations for smooth user experience
- **💾 Persistent Settings**: Remember user preferences between sessions
- **📋 Multiple Adapters**: Support for multiple network interfaces

## 🖼️ Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────┐
│ NetSwitch                                      Exit │
├─────────────────────────────────────────────────────┤
│                🌐 NetSwitch                         │
│                                                     │
│ Select Network Adapter                              │
│ [All Network Adapters           ▼]                 │
│                                                     │
│ Choose a DNS Server                                 │
│ [AU - Cloudflare (1.1.1.1, 1.0.0.1) ▼]           │
│                                                     │
│ [💾 Apply DNS] [⚡ Fastest DNS] [🧹 Flush DNS] [⚙️ Options] │
│                                                     │
│ Ready.                                              │
└─────────────────────────────────────────────────────┘
```

### Custom DNS Configuration
When "Custom..." is selected, additional fields appear for manual DNS entry with IPv6 support.

## 🚀 Installation

### Prerequisites
- **Windows 10/11** (Required for netsh commands)
- **Python 3.11.9+**
- **Administrator privileges** (for DNS changes)

### Method 1: Direct Installation
```bash
# Clone or download the repository
git clone https://github.com/yourusername/netswitch.git
cd netswitch

# Install dependencies
pip install customtkinter

# Run the application
python net-switch.py
```

### Method 2: Requirements File
```bash
# Install from requirements.txt (if available)
pip install -r requirements.txt
python net-switch.py
```

### Dependencies
- `customtkinter>=5.0.0` - Modern UI framework
- `tkinter` - Built-in GUI library (included with Python)

## 📖 Usage

### Basic Operations

#### 1. Changing DNS Servers
1. **Select Network Adapter**: Choose your network interface from the dropdown
2. **Choose DNS Provider**: Select from Cloudflare, Google, Quad9, or Custom
3. **Apply Changes**: Click "💾 Apply DNS" to apply the settings
4. **Verify**: Check the status bar for confirmation

#### 2. Using Custom DNS
1. Select "Custom..." from the DNS dropdown
2. Enter primary and secondary DNS addresses
3. Optionally enable IPv6 and enter IPv6 DNS addresses
4. Click "💾 Apply DNS" to apply

#### 3. Finding Fastest DNS
1. Click "⚡ Fastest DNS" button
2. Wait for speed testing to complete
3. Review results in the popup dialog
4. Optionally apply the fastest DNS found

#### 4. Flushing DNS Cache
1. Click "🧹 Flush DNS" button
2. Wait for operation to complete
3. Check status bar for confirmation

### Advanced Settings

#### Theme Configuration
1. Click "⚙️ Options" button
2. Select Light or Dark theme
3. Toggle status bar visibility
4. Click "Save" to apply changes

#### IPv6 Configuration
1. Select "Custom..." DNS option
2. Check "Use IPv6 DNS" checkbox
3. Enter IPv6 DNS addresses in the format: `2001:4860:4860::8888`
4. Apply settings as usual

## 🌐 DNS Providers

### Included Providers

| Provider | Primary DNS | Secondary DNS | Features |
|----------|-------------|---------------|----------|
| **Cloudflare** | 1.1.1.1 | 1.0.0.1 | Fast, privacy-focused, global |
| **Google** | 8.8.8.8 | 8.8.4.4 | Reliable, widely used, feature-rich |
| **Quad9** | 9.9.9.9 | 149.112.112.112 | Security-focused, malware blocking |
| **Custom** | User-defined | User-defined | Your choice of DNS servers |

### IPv6 Support
All providers support IPv6 DNS servers when using custom configuration:
- **Cloudflare IPv6**: `2606:4700:4700::1111`, `2606:4700:4700::1001`
- **Google IPv6**: `2001:4860:4860::8888`, `2001:4860:4860::8844`
- **Quad9 IPv6**: `2620:fe::fe`, `2620:fe::9`

## 🔒 Security Features

### Input Sanitization
- **String Sanitization**: Removes control characters and limits length
- **Network Adapter Validation**: Validates adapter names against injection
- **Command Argument Sanitization**: Cleans command-line arguments
- **DNS Server Validation**: Ensures only valid DNS selections

### Validation Systems
- **IPv4 Validation**: Comprehensive IPv4 address validation
- **IPv6 Validation**: Support for IPv6 address formats
- **Length Limits**: Prevents buffer overflow attacks
- **Character Filtering**: Removes dangerous characters

### Protection Mechanisms
- **Command Injection Prevention**: Sanitizes all subprocess arguments
- **Timeout Protection**: Prevents hanging operations
- **Error Handling**: Safe error handling with sanitized messages
- **Safe Defaults**: Fallback to safe values on validation failure

## 💻 Technical Requirements

### System Requirements
- **Operating System**: Windows 10/11
- **Python Version**: 3.11.9 or higher
- **Memory**: 50MB RAM minimum
- **Storage**: 10MB disk space
- **Network**: Internet connection for DNS testing

### Permissions
- **Administrator Rights**: Required for changing DNS settings
- **Network Access**: Needed for DNS testing and validation
- **Registry Access**: For persistent settings (future feature)

## 🏗️ Architecture

### Project Structure
```
NetSwitch-v1.0/
├── net-switch.py          # Main application file
├── README.md             # This documentation
└── requirements.txt      # Python dependencies (optional)
```

### Code Organization
```python
# Input Sanitization Functions
├── sanitize_string()              # General string sanitization
├── sanitize_network_adapter_name() # Network adapter validation
├── validate_dns_server_name()     # DNS server selection validation
└── sanitize_command_args()        # Command argument sanitization

# Core DNS Functions
├── is_valid_ip()                  # IPv4 validation
├── is_valid_ipv6()                # IPv6 validation
├── apply_dns()                    # DNS application logic
├── flush_dns()                    # DNS cache flushing
├── test_dns()                     # DNS speed testing
└── find_fastest_dns()             # Fastest DNS detection

# GUI Components
└── NetSwitchApp                   # Main application class
    ├── __init__()                 # UI initialization
    ├── get_adapters()             # Network adapter detection
    ├── show_options()             # Options dialog
    ├── apply_dns_action()         # DNS application handler
    ├── flush_dns_action()         # DNS flush handler
    └── fastest_dns_action()       # Fastest DNS handler
```

### Design Patterns
- **MVC Pattern**: Separation of UI, logic, and data
- **Singleton Pattern**: Single application instance
- **Observer Pattern**: Status updates and threading
- **Factory Pattern**: DNS provider configurations

## 🔧 Troubleshooting

### Common Issues

#### "Access Denied" Error
**Cause**: Insufficient permissions to modify DNS settings
**Solution**: 
1. Right-click on Command Prompt/PowerShell
2. Select "Run as Administrator"
3. Navigate to NetSwitch directory
4. Run `python net-switch.py`

#### DNS Changes Not Applied
**Cause**: Network adapter name mismatch
**Solution**:
1. Select correct network adapter from dropdown
2. Try "All Network Adapters" option
3. Verify adapter is enabled in Network Settings

#### Application Won't Start
**Cause**: Missing dependencies or Python version
**Solution**:
```bash
# Check Python version
python --version

# Install/upgrade customtkinter
pip install --upgrade customtkinter

# Run with UTF-8 encoding
python -X utf8 net-switch.py
```

#### Unicode/Encoding Errors
**Cause**: System encoding issues with emojis
**Solution**:
```bash
# Run with explicit UTF-8 encoding
python -X utf8 net-switch.py

# Or set environment variable
set PYTHONIOENCODING=utf-8
python net-switch.py
```

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "Invalid Input" | IP address format error | Check IP address format |
| "Command timed out" | Network operation timeout | Check internet connection |
| "Failed to apply DNS" | System-level error | Run as administrator |
| "No DNS servers reachable" | Network connectivity issue | Check network connection |

### Performance Tips
- **Network Speed**: Use ethernet connection for fastest results
- **Firewall**: Ensure DNS traffic isn't blocked
- **Antivirus**: Add NetSwitch to exclusions if needed
- **Background Apps**: Close unnecessary network applications

## 🤝 Contributing

We welcome contributions to NetSwitch! Here's how you can help:

### Development Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/netswitch.git
cd netswitch

# Create virtual environment
python -m venv netswitch-env
netswitch-env\Scripts\activate

# Install dependencies
pip install customtkinter
```

### Contribution Guidelines
1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Test** your changes thoroughly
4. **Commit** with clear messages: `git commit -m "Add feature description"`
5. **Push** to your fork: `git push origin feature-name`
6. **Submit** a pull request

### Areas for Contribution
- 🌐 Additional DNS providers
- 🔧 Enhanced IPv6 support
- 🎨 UI/UX improvements
- 🔒 Security enhancements
- 📚 Documentation updates
- 🐛 Bug fixes and testing

### Code Standards
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations where possible
- **Documentation**: Include docstrings for functions
- **Security**: Maintain input sanitization standards
- **Testing**: Test on multiple Windows versions

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

```
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

Copyright 2025 NetSwitch Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 🙏 Acknowledgments

- **CustomTkinter** - Modern UI framework
- **DNS Jumper** - Inspiration for UI design
- **Python Community** - Excellent documentation and support
- **Contributors** - Everyone who helps improve NetSwitch

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/netswitch/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/netswitch/discussions)
- **Documentation**: This README and inline code comments

---

**Made with ❤️ by the NetSwitch team**

*NetSwitch v1.0 - Simplifying DNS management for Windows users*
