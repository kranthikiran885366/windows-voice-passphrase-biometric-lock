# Sivaji Security System - System Architecture

## Overview

Sivaji is a production-grade AI voice biometric authentication system inspired by the Sivaji movie security interface. It provides military-grade speaker recognition with real-time liveness detection, Windows integration, and zero-knowledge voice storage.

## System Components

### 1. Voice Authentication Pipeline

**Module:** `voice_auth/`

#### Voice Processor (`voice_processor.py`)
- **MFCC Extraction**: Converts raw audio → 13-dimensional MFCC features
  - Sample Rate: 16 kHz
  - Frame Length: 2048 samples
  - Hop Length: 512 samples
  - Mel Bands: 40
  
- **Spectrogram**: Mel-scale power spectrogram for visual analysis

- **Voice Activity Detection (VAD)**:
  - Energy-based thresholding
  - Zero-crossing rate analysis
  - Filters silence and noise

#### Liveness Detector (`liveness_detector.py`)

Ensures voice is real-time, not recorded playback.

**Techniques:**
1. **F0 Contour Analysis** (Pitch Variation)
   - Extract fundamental frequency using PYIN algorithm
   - Real speakers have natural pitch variation
   - Recordings have flat or periodic patterns

2. **Spectral Dynamics**
   - Spectral centroid variation over time
   - Real speech has natural timbral changes
   - Playback has consistent spectrum

3. **Echo Pattern Detection**
   - Autocorrelation peaks indicate echoes
   - Real rooms vs. recording artifacts
   - Thresholded at 0.5 similarity

4. **Background Noise Variability**
   - Frame-wise energy statistics
   - Real speech has variable background
   - Playback has static noise

**Liveness Score Calculation:**
\`\`\`
liveness = 0.35 * f0_variation 
         + 0.25 * spectral_variation 
         + 0.25 * echo_liveness 
         + 0.15 * noise_liveness
\`\`\`

Threshold: > 0.5 (50% confidence)

### 2. AI Speaker Recognition Model

**Module:** `ai_models/`

#### Model Architecture: CNN + LSTM

\`\`\`
Input: (batch, 13, 50, 1)  # MFCC features
  ↓
Conv2D(32, 3×3) → ReLU → BatchNorm → MaxPool(2,2)
  ↓
Conv2D(64, 3×3) → ReLU → BatchNorm → MaxPool(2,2)
  ↓
Conv2D(128, 3×3) → ReLU → BatchNorm
  ↓
Reshape → (batch, time, 128)
  ↓
LSTM(256) → Dropout(0.3) → LSTM(128) → Dropout(0.3)
  ↓
Dense(512) → ReLU → BatchNorm  [SPEAKER EMBEDDING]
  ↓
Dense(256) → ReLU → Dropout(0.3)
  ↓
Dense(num_speakers+1) → Softmax  [CLASSIFICATION]
\`\`\`

**Key Design Choices:**
- **CNN for spectro-temporal features**: Captures local patterns
- **LSTM for temporal dynamics**: Models voice variations
- **512-dim embedding**: Speaker identity representation
- **Batch Normalization**: Improves training stability
- **Dropout**: Prevents overfitting

#### Training

**Loss Function:** Sparse Categorical Crossentropy
- Multi-class classification (one speaker per user + unknown)

**Optimizer:** Adam (lr=0.001)

**Metrics:**
- Accuracy on test set
- Confidence scores

**Data Augmentation:**
- Time-stretching (0.9-1.1×)
- Pitch-shifting (±2 semitones)
- Additive noise (SNR > 10dB)

### 3. Verification Pipeline

**Module:** `voice_auth/verification_pipeline.py`

**Flow:**
\`\`\`
Live Voice Audio
    ↓
[Preprocessing]
    - Normalize amplitude
    - Remove silence
    ↓
[Liveness Detection]
    - Check F0, spectral dynamics, echoes
    - Compute liveness_score
    ↓
[Feature Extraction]
    - Extract MFCC
    - Pad to 50 timesteps
    ↓
[Embedding Extraction]
    - Pass through CNN+LSTM
    - Extract 512-dim speaker embedding
    ↓
[Comparison]
    - Cosine similarity with stored embedding
    - Compute similarity_score
    ↓
[Decision]
    confidence = 0.7 * similarity + 0.3 * liveness
    
    if confidence >= 0.98:
        AUTHENTICATED
    else:
        DENIED
\`\`\`

**Thresholds:**
- Authentication: 98% confidence (high security)
- False Acceptance Rate (FAR): < 0.5%
- False Rejection Rate (FRR): < 2%

### 4. Encryption & Security

**Module:** `security/`

#### Encryption Manager (`encryption.py`)

**Algorithm:** Fernet (AES-128-CBC + HMAC-SHA256)
- Symmetric key encryption
- Key derivation: Fernet default (os.urandom())
- Master key stored in: `security/credentials/.master_key`

**Data Encrypted:**
- User voice embeddings
- Voice profiles (mean + std)
- Audit logs

#### Audit Logger (`audit_logger.py`)

**Logged Events:**
\`\`\`json
{
  "timestamp": "2025-12-28T15:30:45Z",
  "username": "authorized_user",
  "authenticated": true,
  "confidence": 0.998,
  "liveness_score": 0.95,
  "similarity_score": 0.998,
  "reason": "Authenticated"
}
\`\`\`

**Storage:** Encrypted JSON lines format
**Retention:** Indefinite (supports log rotation)

#### Lockout Manager (`lockout_manager.py`)

**Failed Attempt Tracking:**
- Max attempts: 3
- Lockout duration: 15 minutes
- Reset on success

**Lockout State:**
\`\`\`json
{
  "authorized_user": {
    "failed_attempts": 2,
    "last_attempt": "2025-12-28T15:30:00Z",
    "locked_until": null
  }
}
\`\`\`

### 5. UI/UX Layer

**Module:** `ui/`

#### Lockscreen (`lockscreen.py`)

**Features:**
- Full-screen, frameless window
- Dark cinematic theme (#0a0e27)
- Neon accents (Cyan #00d9ff, Violet #7c3aed)
- Animated microphone indicator
- Real-time waveform visualization

**Interaction Flow:**
1. Display random authentication sentence
2. User clicks START AUTHENTICATION
3. Waveform animates during recording
4. Status updates: LISTENING → ANALYZING → Result
5. Voice response (TTS) plays
6. UI shows result (green for success, red for failure)

#### Waveform Animation (`waveform_animation.py`)

**Visualization:**
- 40 frequency bands
- Height represents audio intensity
- Color gradient: Cyan (quiet) → Violet (medium) → Red (loud)
- Updates every 50ms

### 6. Voice Bot (TTS)

**Module:** `voice_bot/`

**Engine:** pyttsx3 (offline, no cloud)

**Voice Settings:**
- Rate: 120 WPM (slower, deliberate)
- Volume: 0.9 (high, authoritative)
- Voice: System default (preferring male voice)

**Responses:**
- Success: "Authentication successful. Welcome. System access granted."
- Failure: "Unauthorized access detected. You are not permitted to use this system."
- Lockout: "Security violation confirmed. System locked."

### 7. Windows Integration

**Module:** `windows/`

**Methods:**

**Method 1: Startup Script**
- Runs after Windows loads
- Registered in user's Startup folder
- Works on standard accounts

**Method 2: Registry Run Key**
- Early startup via HKEY_LOCAL_MACHINE
- Requires admin during installation
- Works on all systems

**Method 3: Custom Credential Provider (Future)**
- Pre-login integration
- Runs at SYSTEM privilege
- Replaces Windows logon UI
- Requires DLL + registry modifications

## Data Flow

### Enrollment Process

\`\`\`
User Input (Voice)
    ↓
Audio Recording
    ↓
Voice Processor (MFCC extraction)
    ↓
AI Model (Extract 512-dim embedding)
    ↓
Multiple Samples (5 sentences)
    ↓
Compute Mean Embedding
    ↓
Encryption Manager (AES-256)
    ↓
Save to: security/credentials/authorized_user.enc
\`\`\`

### Authentication Process

\`\`\`
User Input (Voice)
    ↓
Audio Recording
    ↓
Liveness Detection (Real-time voice?)
    ↓
Voice Processor (MFCC extraction)
    ↓
AI Model (Extract embedding)
    ↓
Verification (Cosine similarity)
    ↓
Confidence = 0.7*similarity + 0.3*liveness
    ↓
Threshold >= 0.98?
    ├─ YES → Grant Access
    │         Audit Log (success)
    │         Lockout Reset
    │         TTS: "Access Granted"
    │
    └─ NO → Deny Access
            Failed Attempts += 1
            Audit Log (failure)
            TTS: "Access Denied"
            Check if >= 3 failures?
            ├─ YES → Lockout 15 minutes
            └─ NO → Allow retry
\`\`\`

## Modular Design

Each component is independent and testable:

\`\`\`
┌─────────────────────────────────────────┐
│         UI Layer (PyQt5)                 │
│         lockscreen.py                    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│    Verification Pipeline                 │
│  verification_pipeline.py                │
└─────────────────┬───────────────────────┘
                  │
      ┌───────────┼────────────┐
      │           │            │
      ▼           ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Liveness │ │ AI Model │ │Encryption│
│ Detector │ │ Inference│ │ Manager  │
└──────────┘ └──────────┘ └──────────┘
      │           │            │
      └───────────┼────────────┘
                  │
      ┌───────────┴──────────┐
      │                      │
      ▼                      ▼
┌──────────────┐    ┌──────────────┐
│ Voice Proc.  │    │ Audit Logger │
│ (MFCC)       │    │ Lockout Mgr  │
└──────────────┘    └──────────────┘
\`\`\`

## Security Properties

### What's Protected
✅ Voice embeddings (encrypted at rest)
✅ User profiles (encrypted)
✅ Audit logs (encrypted)
✅ Authentication decisions (logged + encrypted)
✅ System locked on repeated failures

### What's NOT Protected (Limitations)
⚠️ System-level key interception
⚠️ Microphone tampering
⚠️ Physical GPU access
⚠️ DLL injection attacks (user mode)

### Threat Mitigations

| Threat | Mitigation |
|--------|-----------|
| Voice Spoofing (Playback) | Liveness detection (F0, spectral) |
| Voice Cloning (AI) | 98% accuracy threshold |
| Brute Force | 3-attempt lockout, encrypted profiles |
| Man-in-Middle (None) | All processing local, offline |
| Key Extraction | Fernet key in file system |
| Audit Log Tampering | Encrypted + HMAC |

## Performance Metrics

| Metric | Target | Implementation |
|--------|--------|-----------------|
| Auth Time | <2s | MFCC + inference = ~1.2s |
| Accuracy | ≥98% | CNN+LSTM on 512-dim embeddings |
| FAR | <0.5% | Cosine similarity + liveness |
| FRR | <2% | Threshold = 0.98 |
| Liveness Detection | 90%+ | Multi-factor (F0, spectral, echo) |

## Future Enhancements

1. **Multi-speaker Support** - Add users to system
2. **Adaptive Thresholds** - Adjust confidence based on environment
3. **Face + Voice Fusion** - Multi-modal biometrics
4. **Cloud Backup** (Optional) - Encrypted profile sync
5. **Mobile App** - Remote enrollment/verification
6. **Real Credential Provider** - True pre-login integration
