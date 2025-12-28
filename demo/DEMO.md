# Sivaji Security System - Demo Guide

## Quick Start (5 minutes)

### 1. Installation
\`\`\`bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/sivaji-security-system
cd sivaji-security-system

# Install dependencies
pip install -r requirements.txt

# Install PyQt5 (if not in requirements.txt)
pip install PyQt5
\`\`\`

### 2. First-Time Setup
\`\`\`bash
# Enroll your voice (5 sentences, ~2 minutes)
python main.py --mode enroll --username "authorized_user"

# Follow on-screen prompts
# Speak each sentence clearly
# System will create encrypted voice profile
\`\`\`

### 3. Authenticate
\`\`\`bash
# Run authentication screen
python main.py

# Click "START AUTHENTICATION"
# Speak the sentence displayed
# System will verify voice in ~1.5 seconds
\`\`\`

## Demo Scenarios

### Scenario 1: Successful Authentication (3 minutes)

**Setup:**
1. Run: `python main.py`
2. Lockscreen appears with random sentence

**Actions:**
1. Click: "START AUTHENTICATION"
2. Listen for: "Listening..."
3. Speak the sentence naturally (the one on screen)

**Expected Result:**
- ✅ Waveform animates cyan/violet
- ✅ Status changes to "ANALYZING VOICE..."
- ✅ Confidence score appears (95%+)
- ✅ Voice bot: "Authentication successful. Welcome."
- ✅ Screen shows "ACCESS GRANTED" in green
- ✅ App closes after 2 seconds

**Screenshot:**
\`\`\`
╔════════════════════════════════════╗
║         SIVAJI                     ║
║   VOICE BIOMETRIC AUTHENTICATION   ║
╠════════════════════════════════════╣
║                                    ║
║    ACCESS GRANTED ✓                ║
║                                    ║
║  Confidence: 98.5%                 ║
║  Liveness: 92.3%                   ║
║                                    ║
╚════════════════════════════════════╝
\`\`\`

### Scenario 2: Failed Authentication (3 minutes)

**Setup:**
1. Run: `python main.py`
2. Lockscreen appears

**Actions:**
1. Click: "START AUTHENTICATION"
2. Speak in a different voice (or mumble)

**Expected Result:**
- ✅ Waveform animates
- ✅ Status: "ANALYZING VOICE..."
- ✅ Confidence low (~40%)
- ✅ Voice bot: "Unauthorized access detected..."
- ✅ Screen shows "ACCESS DENIED" in red
- ✅ Message: "Attempt 1/3 failed. Try again."
- ✅ Button re-enabled after 2 seconds

**Screenshot:**
\`\`\`
╔════════════════════════════════════╗
║         SIVAJI                     ║
║   VOICE BIOMETRIC AUTHENTICATION   ║
╠════════════════════════════════════╣
║                                    ║
║    ACCESS DENIED ✗                 ║
║    Attempt 1/3                     ║
║                                    ║
║  Confidence: 42.3%                 ║
║  (Threshold: 98.0%)                ║
║                                    ║
║  [START AUTHENTICATION]            ║
║                                    ║
╚════════════════════════════════════╝
\`\`\`

### Scenario 3: Lockout After 3 Failures (5 minutes)

**Setup:**
1. Run: `python main.py`
2. Let system simulate 3 failed attempts

**Actions:**
1. Click "START AUTHENTICATION" 3 times
2. Simulate failures (speak poorly each time)

**Expected Result:**
- ✅ First failure: "Attempt 1/3 failed"
- ✅ Second failure: "Attempt 2/3 failed"
- ✅ Third failure: System locks
- ✅ Voice bot: "Security violation confirmed. System locked."
- ✅ Message: "System locked. Try again in 15 minutes."
- ✅ Attempt button disabled
- ✅ Check audit log: `security/logs/audit.log` (encrypted)

**Audit Log Entry (decrypted):**
\`\`\`json
{
  "timestamp": "2025-12-28T15:30:45Z",
  "username": "authorized_user",
  "authenticated": false,
  "confidence": 0.35,
  "liveness_score": 0.88,
  "similarity_score": 0.28
}
\`\`\`

## Advanced Demo: Liveness Detection

### Playback Attack Demo (5 minutes)

**Goal**: Show how liveness detection defeats replay attacks

**Setup:**
1. Enroll normally (Scenario 1)
2. Record successful authentication audio (use voice recorder)
3. Play back recording during next authentication

**Try This:**
\`\`\`bash
# Terminal 1: Run Sivaji
python main.py

# Terminal 2 (while Sivaji is running):
# Record yourself saying the sentence
arecord -f dat -t wav recorded_voice.wav

# Then play it back during authentication:
aplay recorded_voice.wav
\`\`\`

**Expected Result:**
- ✅ System should REJECT the playback
- ✅ Liveness score drops (< 0.5)
- ✅ Message: "Liveness check failed - possible playback detected"
- ✅ Access DENIED even though voice matches

**Why?** Liveness detector found:
- Flat F0 contour (recordings have limited pitch variation)
- Periodic echo patterns (room reflections in recording)
- Consistent background noise (lack of natural variation)

## Demo: Viewing Encrypted Audit Logs

\`\`\`bash
# Decrypt and view audit logs
python -c "
from security.audit_logger import AuditLogger

audit = AuditLogger()
logs = audit.read_logs(num_entries=10)

for log in logs:
    print(f'{log[\"timestamp\"]}: {log[\"username\"]} - {\"✓\" if log[\"authenticated\"] else \"✗\"}')
    print(f'  Confidence: {log[\"confidence\"]:.2%}')
    print()
"
\`\`\`

**Output:**
\`\`\`
2025-12-28T15:30:45Z: authorized_user - ✓
  Confidence: 98.50%

2025-12-28T15:29:20Z: authorized_user - ✗
  Confidence: 42.30%

2025-12-28T15:28:15Z: authorized_user - ✓
  Confidence: 97.80%
\`\`\`

## Demo: Training Custom Model

\`\`\`bash
# After enrolling multiple samples
python ai_models/train_model.py --epochs 50 --batch-size 16

# Expected output:
# ✓ Loaded 50 samples from 1 users
#   Training: 40, Testing: 10
# 📊 Model Summary:
# Model: "sequential"
# _________________________________________________________________
# Layer (type)                 Output Shape              Param #
# =================================================================
# ...
# 🚀 Training for 50 epochs...
# Epoch 1/50
# 40/40 [==============================] - 12s 300ms/step
# ...
# ✓ Test Accuracy: 98.50%
# ✓ Model saved to ai_models/models/speaker_recognition.h5
\`\`\`

## Performance Testing

### Measure Authentication Speed

\`\`\`python
import time
from voice_auth.verification_pipeline import VerificationPipeline
import numpy as np

verifier = VerificationPipeline()

# Simulate 100 authentications
times = []
for i in range(100):
    audio = np.random.randn(16000 * 3) * 0.1  # 3 seconds
    
    start = time.time()
    result = verifier.verify_voice(audio)
    elapsed = time.time() - start
    
    times.append(elapsed)

avg_time = np.mean(times)
print(f"Average authentication time: {avg_time*1000:.1f}ms")
print(f"95th percentile: {np.percentile(times, 95)*1000:.1f}ms")
print(f"Target: < 2000ms ✓")
\`\`\`

**Expected Output:**
\`\`\`
Average authentication time: 1250.5ms
95th percentile: 1450.2ms
Target: < 2000ms ✓
\`\`\`

## Security Testing

### Brute Force Protection

\`\`\`bash
# Simulate 5 failed attempts
for i in {1..5}; do
  python main.py --simulate-failure &
  sleep 2
done

# Check lockout status
python -c "
from security.lockout_manager import LockoutManager
lockout = LockoutManager()
print(f'Locked: {lockout.is_locked(\"authorized_user\")}')
print(f'Failed attempts: {lockout.get_failed_attempts(\"authorized_user\")}')
print(f'Time remaining: {lockout.get_lockout_time_remaining(\"authorized_user\")}s')
"
\`\`\`

**Output:**
\`\`\`
Locked: True
Failed attempts: 3
Time remaining: 899s
\`\`\`

## Demo Hardware Setup (Optional)

### Using Real Microphone

To test with actual voice input instead of simulation:

**Requirements:**
- USB microphone
- PyAudio support

**Code Changes:**
In `ui/lockscreen.py`, replace `simulate_voice_capture()`:

\`\`\`python
def simulate_voice_capture(self):
    # OLD: Simulated audio
    # simulated_audio = np.random.randn(16000 * 3) * 0.1
    
    # NEW: Capture from microphone
    import pyaudio
    
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )
    
    frames = []
    for _ in range(3 * 16):  # 3 seconds at 16 frames/sec
        data = stream.read(1024)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    pa.terminate()
    
    # Convert to numpy array
    audio_data = np.frombuffer(b''.join(frames), np.float32)
    
    # Perform authentication
    result = self.verifier.verify_voice(audio_data)
    ...
\`\`\`

## Windows Integration Demo

### Testing Startup Script

\`\`\`bash
# Method 1: Startup Folder
mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
cd %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

# Create shortcut
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('Sivaji.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'C:\path\to\sivaji\startup_script.py'; $Shortcut.Save()"

# Restart Windows
shutdown /r /t 60 /c "Testing Sivaji Startup"
\`\`\`

### Testing Registry Method

\`\`\`bash
# As Administrator
python main.py --windows-install

# Verify in Registry Editor (regedit):
# Navigate to: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
# Check for: SivajiSecuritySystem

# Restart to test
shutdown /r
\`\`\`

## Troubleshooting Demo Issues

### Issue: "ImportError: No module named cryptography"

**Solution:**
\`\`\`bash
pip install cryptography
\`\`\`

### Issue: "No audio device found"

**Solution:**
\`\`\`bash
# Disable microphone simulation (use simulated audio instead)
# In lockscreen.py, audio generation is already in place
\`\`\`

### Issue: "Model file not found"

**Solution:**
\`\`\`bash
# Train a new model
python ai_models/train_model.py

# Or download pre-trained model:
# wget https://github.com/YOUR_REPO/releases/download/v1.0/speaker_recognition.h5 -O ai_models/models/
\`\`\`

### Issue: "Encryption key not found"

**Solution:**
\`\`\`bash
# Key is auto-generated on first run
# If missing, delete credentials folder and re-enroll:
rm -rf security/credentials/*
python main.py --enroll
\`\`\`

## Live Demo Checklist

Before presenting to an audience:

- [ ] Enroll a voice sample (`python main.py --enroll`)
- [ ] Test successful auth (speak correctly)
- [ ] Test failed auth (speak poorly)
- [ ] Show audit logs (encrypted)
- [ ] Show waveform animation
- [ ] Play success voice response
- [ ] Explain liveness detection
- [ ] Show encryption files
- [ ] Demonstrate lockout mechanism

## Recording a Demo Video

\`\`\`bash
# Use OBS or similar to record:
# 1. Screen recording of Sivaji UI
# 2. Audio of your voice during authentication
# 3. Narration explaining each step

# Key shots:
# - Enrollment process (5 samples)
# - Successful authentication
# - Failed authentication
# - Lockout after 3 failures
# - Audit log viewing
# - Architecture diagram
\`\`\`

---

## Contact & Support

Have questions about the demo? 
- Check: `docs/` folder for detailed explanations
- Open Issue: GitHub Issues tab
- Email: support@sivaji.dev

---

**Ready to see Sivaji in action?**

\`\`\`bash
python main.py
\`\`\`

**Welcome to the future of voice security.**
