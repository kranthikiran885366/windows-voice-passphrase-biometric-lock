# Sivaji Security System v3.0 - Windows Distribution Guide

## 🚀 Enterprise Windows Deployment

### Quick Download
**[Download Sivaji Security System v3.0 Enterprise (.exe)](https://github.com/kranthikiran885366/voice-based-system-unlock/releases/latest)**

### Distribution Packages
- **Standard Edition**: `sivaji_security_v3.0_standard.exe` (50MB)
- **Enterprise Edition**: `sivaji_security_v3.0_enterprise.exe` (120MB)
- **Developer Edition**: `sivaji_security_v3.0_developer.exe` (200MB)

## 🛠️ Build Instructions v3.0

### Prerequisites
```bat
# Install Python 3.11+ and required tools
winget install Python.Python.3.11
winget install Microsoft.VisualStudio.2022.BuildTools
```

### Build Process
```bat
# Clone and setup
git clone https://github.com/kranthikiran885366/voice-based-system-unlock.git
cd voice-based-system-unlock

# Install dependencies
pip install -r requirements-windows.txt
pip install pyinstaller[encryption]

# Build executable with advanced options
pyinstaller --onefile --windowed --icon=windows/app_icon.ico \
    --add-data "ai_models;ai_models" \
    --add-data "security;security" \
    --add-data "ui;ui" \
    --hidden-import tensorflow \
    --hidden-import torch \
    --hidden-import cryptography \
    --key YOUR_ENCRYPTION_KEY \
    main.py
```

### Advanced Build Options
```bat
# Enterprise build with all features
build_enterprise.bat

# Standard build for general users
build_standard.bat

# Developer build with debugging
build_developer.bat
```

## 💻 Installation & Deployment

### Method 1: Direct Execution (Recommended)
```bat
# Download and run directly
sivaji_security_v3.0_enterprise.exe

# First-time setup
sivaji_security_v3.0_enterprise.exe --setup

# Enterprise configuration
sivaji_security_v3.0_enterprise.exe --enterprise-config
```

### Method 2: Silent Installation
```bat
# Silent install with configuration
sivaji_security_v3.0_enterprise.exe /S /CONFIG=enterprise.json

# Automated deployment
msiexec /i sivaji_security_v3.0.msi /quiet TRANSFORMS=enterprise.mst
```

### Method 3: Group Policy Deployment
```bat
# Domain deployment via GPO
gpupdate /force
# Deploy via Software Installation policy
```

## 🔒 Security Features

- **Code Signing**: Authenticode signed with EV certificate
- **Tamper Protection**: Runtime integrity verification
- **Sandboxing**: Isolated execution environment
- **Auto-Updates**: Secure update mechanism with rollback
- **Telemetry**: Optional usage analytics (GDPR compliant)

## 🛠️ Enterprise Management

### Configuration Files
- `config/enterprise.json` - Enterprise settings
- `config/security_policy.xml` - Security policies
- `config/user_groups.yaml` - Role-based access control

### Command Line Options
```bat
sivaji_security.exe --help
sivaji_security.exe --version
sivaji_security.exe --config-check
sivaji_security.exe --diagnostic
sivaji_security.exe --export-logs
```

## 📊 System Requirements

| Component | Minimum | Recommended | Enterprise |
|-----------|---------|-------------|------------|
| **Windows** | 10 (1909+) | 11 (22H2+) | Server 2022 |
| **RAM** | 8GB | 16GB | 32GB+ |
| **Storage** | 10GB | 50GB | 500GB+ |
| **CPU** | Intel i5-8th gen | Intel i7-10th gen | Xeon Gold |
| **GPU** | Integrated | NVIDIA GTX 1660+ | NVIDIA RTX 4090+ |
| **TPM** | 2.0 | 2.0 | 2.0 + HSM |
| **.NET** | 6.0+ | 8.0+ | 8.0+ |

## 🔧 Troubleshooting

### Common Issues
| Issue | Solution |
|-------|----------|
| **"MSVCP140.dll missing"** | Install Visual C++ Redistributable 2022 |
| **"Access denied"** | Run as Administrator, check antivirus exclusions |
| **"Microphone not detected"** | Check privacy settings, update audio drivers |
| **"Model loading failed"** | Verify GPU drivers, check CUDA installation |
| **"License validation failed"** | Check internet connection, verify license key |

### Performance Optimization
```bat
# Optimize for performance
sivaji_security.exe --optimize-performance

# Enable GPU acceleration
sivaji_security.exe --enable-gpu

# Reduce memory usage
sivaji_security.exe --low-memory-mode
```
