# Deployment Guide - Sivaji Security System

## Prerequisites

- Python 3.8+
- Windows 10/11 (for Windows integration features)
- Microphone
- Optional: Webcam (for face/iris recognition)
- Optional: Near-infrared camera (for enhanced iris recognition)

## Installation Steps

### 1. Clone Repository

\`\`\`bash
git clone https://github.com/your-username/sivaji-security-system
cd sivaji-security-system
\`\`\`

### 2. Create Virtual Environment

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 3. Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Create Necessary Directories

\`\`\`bash
mkdir -p enrollments
mkdir -p logs
mkdir -p config
mkdir -p ai_models/pretrained
\`\`\`

### 5. Download Pre-trained Models

\`\`\`bash
# Download voice models
wget https://example.com/models/voice_model.h5 -O ai_models/pretrained/voice_model.h5

# Download face models (if using face recognition)
wget https://example.com/models/face_embedding_model.h5 -O ai_models/pretrained/face_embedding_model.h5
wget https://example.com/models/face_liveness_model.h5 -O ai_models/pretrained/face_liveness_model.h5

# Download iris models (if using iris recognition)
wget https://example.com/models/iris_embedding_model.h5 -O ai_models/pretrained/iris_embedding_model.h5
\`\`\`

### 6. Initialize Configuration

\`\`\`bash
python main.py --mode config
\`\`\`

## Windows Integration

### Option 1: Startup Script (Easiest)

1. Create shortcut to main.py
2. Place in: `C:\Users\[USERNAME]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
3. System will run authentication at startup

### Option 2: Registry Hook

\`\`\`bash
python windows/windows_integration.py --register
\`\`\`

### Option 3: Credential Provider (Advanced)

Requires C++ DLL development. See `windows/README_WINDOWS.md` for details.

## Enrollment

### Single User Setup

\`\`\`bash
python main.py --mode enroll --username "authorized_user"
\`\`\`

### Multiple Users

\`\`\`bash
python main.py --mode enroll --username "user1"
python main.py --mode enroll --username "user2"
python main.py --mode enroll --username "user3"
\`\`\`

## Running the System

### Basic Authentication

\`\`\`bash
python main.py
\`\`\`

### With Debug Logging

\`\`\`bash
python main.py --debug
\`\`\`

### Multi-Biometric Mode

\`\`\`bash
python main.py --enable-face --enable-iris
\`\`\`

## Configuration Management

### View Current Configuration

\`\`\`bash
python main.py --mode config
\`\`\`

### Modify Configuration

\`\`\`bash
python main.py --mode config
# Interactive wizard will guide you
\`\`\`

### Manual Configuration Edit

Edit `config/system_config.json`:

\`\`\`json
{
  "security": {
    "max_failed_attempts": 5,
    "lockout_duration_minutes": 30,
    "voice_confidence_threshold": 0.98
  },
  "biometric": {
    "enable_voice": true,
    "enable_face": false,
    "enable_iris": false
  },
  "notification": {
    "enable_email": false,
    "enable_sms": false
  }
}
\`\`\`

## System Testing

\`\`\`bash
python main.py --mode test
\`\`\`

This will test:
- Audio I/O
- Video I/O (if available)
- Voice model loading
- Encryption system
- File storage
- All enabled biometric models

## Logging and Monitoring

### View Authentication Logs

\`\`\`bash
cat logs/authentication.log
\`\`\`

### View Threat Logs

\`\`\`bash
cat logs/threats.log
\`\`\`

### View Audit Logs

\`\`\`bash
cat logs/audit.log
\`\`\`

## Notifications Setup

### Email Alerts

1. Update `config/notification_config.json`:

\`\`\`json
{
  "email_enabled": true,
  "email_smtp_server": "smtp.gmail.com",
  "email_from": "your-email@gmail.com",
  "email_app_password": "your-app-password",
  "alert_recipients": {
    "admin_emails": ["admin@example.com"]
  }
}
\`\`\`

2. Use Gmail app password (not regular password)

### SMS Alerts

1. Sign up for Twilio account
2. Update `config/notification_config.json`:

\`\`\`json
{
  "sms_enabled": true,
  "sms_account_sid": "your-account-sid",
  "sms_auth_token": "your-auth-token",
  "sms_from_number": "+1234567890",
  "alert_recipients": {
    "admin_phones": ["+1987654321"]
  }
}
\`\`\`

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution**: Install missing dependencies
\`\`\`bash
pip install -r requirements.txt --upgrade
\`\`\`

### Issue: "Camera not found"

**Solution**: Check camera permissions
\`\`\`bash
# Linux
sudo apt-get install libglib2.0-0

# Windows
Settings > Privacy & Security > Camera
\`\`\`

### Issue: "Audio device not found"

**Solution**: Check microphone
\`\`\`bash
python -c "import sounddevice; print(sounddevice.query_devices())"
\`\`\`

### Issue: "Low authentication accuracy"

**Solution**: Re-enroll with better quality samples
\`\`\`bash
python main.py --mode enroll --username "user1"
\`\`\`

## Performance Optimization

### Reduce Authentication Time

\`\`\`json
{
  "security": {
    "voice_confidence_threshold": 0.95
  }
}
\`\`\`

### Improve Accuracy

\`\`\`json
{
  "security": {
    "voice_confidence_threshold": 0.99
  }
}
\`\`\`

### Enable GPU Acceleration

\`\`\`python
# Automatic GPU detection in TensorFlow
# Requires CUDA toolkit installed
\`\`\`

## Uninstallation

\`\`\`bash
# Remove startup hook
python windows/windows_integration.py --unregister

# Delete data
rm -rf enrollments logs config ai_models

# Remove virtual environment
rm -rf venv
\`\`\`

## Support

For issues, refer to:
- `docs/TROUBLESHOOTING.md` - Common problems
- `docs/SYSTEM_ARCHITECTURE.md` - Technical details
- `docs/ALGORITHMS_USED.md` - Algorithm documentation
\`\`\`

Now let me create the final comprehensive documentation index:
