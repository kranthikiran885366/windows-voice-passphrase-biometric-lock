"""
Main Lockscreen UI - Sivaji Security System
Full-screen authentication interface with voice input
"""

import sys
import random
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRect
from PyQt5.QtGui import QFont, QColor, QPixmap
import numpy as np
from datetime import datetime

from ui.styles import STYLESHEET, COLORS
from ui.waveform_animation import WaveformWidget
from ui.avatar_system import Avatar3DWidget
from voice_auth.verification_pipeline import VerificationPipeline
from security.lockout_manager import LockoutManager
from security.audit_logger import AuditLogger
from voice_bot.tts_engine import SivajiTTS
from security.threat_detection import ThreatDetectionEngine
from security.notification_system import NotificationSystem
from voice_auth.passive_authentication import PassiveAuthenticationMonitor
from security.developer_failsafe import DeveloperFailsafeManager  # Import DeveloperFailsafeManager


class SivajiLockscreen(QMainWindow):
    """Main authentication lockscreen with multi-biometric support"""
    
    # Authentication sentences
    AUTH_SENTENCES = [
        "The quick brown fox jumps over the lazy dog",
        "Sivaji is the most advanced security system ever created",
        "My voice is my password and my identity",
        "Authentication complete and system is now accessible",
        "Unauthorized users will be denied immediate access",
        "Voice biometric authentication is the future of security",
        "This system protects against unauthorized access attempts",
        "Speak clearly and naturally for best results",
    ]
    
    def __init__(self, enable_face=False, enable_iris=False, failsafe_manager=None):
        super().__init__()
        
        # Security systems
        self.verifier = VerificationPipeline()
        self.lockout = LockoutManager()
        self.audit = AuditLogger()
        self.tts = SivajiTTS()
        self.threat_detector = ThreatDetectionEngine()
        self.notification_system = NotificationSystem()
        self.passive_auth = PassiveAuthenticationMonitor()
        self.failsafe_manager = failsafe_manager  # Added fail-safe manager parameter
        
        # Biometric options
        self.enable_face = enable_face
        self.enable_iris = enable_iris
        
        # State
        self.username = "authorized_user"
        self.is_authenticated = False
        self.is_recording = False
        self.current_sentence = ""
        self.failed_attempts = 0
        self.max_attempts = 3
        self.failsafe_active = False  # Track fail-safe state
        
        # Setup UI
        self.setWindowTitle("SIVAJI SECURITY SYSTEM")
        self.setStyleSheet(STYLESHEET)
        self.setup_ui()
        
        # Make window full-screen and non-resizable
        self.setGeometry(0, 0, QApplication.primaryScreen().size().width(),
                        QApplication.primaryScreen().size().height())
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Disable Alt+Tab and system keys
        self.disable_system_keys()
        
        # Start authentication UI
        self.show_authentication_screen()
    
    def setup_ui(self):
        """Setup main UI layout with optional avatar"""
        central = QWidget()
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout()
        
        # Left side: Avatar (optional)
        if True:  # Always include avatar area for future expansion
            left_layout = QVBoxLayout()
            self.avatar = Avatar3DWidget()
            self.avatar.setMinimumSize(400, 600)
            left_layout.addWidget(self.avatar)
            left_layout.setAlignment(self.avatar, Qt.AlignCenter)
            main_layout.addLayout(left_layout, 1)
        
        # Right side: Authentication UI
        right_layout = QVBoxLayout()
        right_layout.setSpacing(30)
        right_layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title = QLabel("SIVAJI")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("VOICE BIOMETRIC AUTHENTICATION")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: #7c3aed; letter-spacing: 2px;")
        subtitle.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(subtitle)
        
        # Spacer
        right_layout.addSpacing(40)
        
        # Status label
        self.status_label = QLabel("INITIALIZING SYSTEM...")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.status_label)
        
        # Sentence to speak
        self.sentence_label = QLabel()
        self.sentence_label.setObjectName("sentenceLabel")
        self.sentence_label.setAlignment(Qt.AlignCenter)
        self.sentence_label.setWordWrap(True)
        right_layout.addWidget(self.sentence_label)
        
        # Waveform visualization
        self.waveform = WaveformWidget()
        right_layout.addWidget(self.waveform)
        
        # Confidence display
        self.confidence_label = QLabel()
        self.confidence_label.setObjectName("statusIndicator")
        self.confidence_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.confidence_label)
        
        # Microphone indicator
        self.mic_label = QLabel("🎤")
        self.mic_label.setObjectName("micLabel")
        self.mic_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.mic_label)
        
        # Message
        self.message_label = QLabel()
        self.message_label.setObjectName("messageLabel")
        self.message_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.message_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.start_button = QPushButton("START AUTHENTICATION")
        self.start_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: white;
                padding: 12px 30px;
                border: 2px solid #00d9ff;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6b2fb5;
                border-color: #00ffff;
            }
            QPushButton:pressed {
                background-color: #5c27a0;
            }
        """)
        self.start_button.clicked.connect(self.start_authentication)
        button_layout.addWidget(self.start_button)
        
        button_layout.addStretch()
        right_layout.addLayout(button_layout)
        
        self.threat_level_label = QLabel("THREAT: LOW")
        self.threat_level_label.setFont(QFont("Arial", 10))
        self.threat_level_label.setStyleSheet("color: #00ff66;")
        right_layout.addWidget(self.threat_level_label)
        
        # Add spacer at bottom
        right_layout.addStretch()
        
        main_layout.addLayout(right_layout, 1)
        central.setLayout(main_layout)
        
        # Timer for voice recording simulation
        self.record_timer = QTimer()
        self.record_timer.timeout.connect(self.simulate_voice_capture)
    
    def show_authentication_screen(self):
        """Display authentication UI"""
        self.status_label.setText("VOICE AUTHENTICATION REQUIRED")
        self.current_sentence = random.choice(self.AUTH_SENTENCES)
        self.sentence_label.setText(f'Speak: "{self.current_sentence}"')
        self.message_label.setText("Click START AUTHENTICATION and speak the sentence above")
        self.confidence_label.setText("")
        self.start_button.show()
        self.start_button.setEnabled(True)
        self.is_authenticated = False
        
        # Reset avatar state
        if hasattr(self, 'avatar'):
            self.avatar.set_state("idle")
    
    def start_authentication(self):
        """Start voice recording and authentication"""
        if self.failsafe_manager and self.failsafe_manager.is_failsafe_valid():
            self.status_label.setText("FAIL-SAFE ACTIVE")
            self.message_label.setText("Emergency developer access enabled")
            self.start_button.hide()
            self.grant_system_access()
            return
        
        # Check if locked out
        if self.lockout.is_locked(self.username):
            remaining = self.lockout.get_lockout_time_remaining(self.username)
            mins = remaining // 60
            self.message_label.setText(
                f"System locked. Try again in {mins} minutes."
            )
            self.tts.speak(f"System locked. Try again in {mins} minutes.")
            return
        
        self.status_label.setText("LISTENING...")
        self.message_label.setText("Speak now. Recording...")
        self.start_button.setEnabled(False)
        self.is_recording = True
        
        # Update avatar state
        if hasattr(self, 'avatar'):
            self.avatar.set_state("listening")
        
        # Animate waveform
        self.waveform.start_animation()
        
        # Simulate recording for 3 seconds
        self.record_timer.start(3000)
    
    def simulate_voice_capture(self):
        """Simulate voice capture and authentication"""
        self.record_timer.stop()
        self.waveform.stop_animation()
        self.is_recording = False
        
        # Simulate recorded audio (in real app, capture from microphone)
        simulated_audio = np.random.randn(16000 * 3) * 0.1
        
        self.status_label.setText("ANALYZING VOICE...")
        self.message_label.setText("Processing biometric data...")
        
        # Simulate authentication delay
        QApplication.processEvents()
        
        # Perform verification
        result = self.verifier.verify_voice(simulated_audio)
        
        if result['authenticated']:
            self.on_authentication_success(result)
        else:
            self.on_authentication_failure(result)
    
    def on_authentication_success(self, result):
        """Handle successful authentication"""
        self.is_authenticated = True
        self.failed_attempts = 0
        self.lockout.record_successful_attempt(self.username)
        self.audit.log_authentication_attempt(self.username, result)
        
        self.passive_auth.start_session(self.username)
        
        self.notification_system.send_alert("AUTHENTICATION_SUCCESS", {
            "timestamp": datetime.now().isoformat(),
            "confidence": result.get("confidence", 0.0)
        })
        
        # Update UI
        self.status_label.setText("ACCESS GRANTED")
        self.status_label.setStyleSheet("color: #00ff66; font-size: 32px;")
        self.sentence_label.setText("✓ AUTHENTICATION SUCCESSFUL")
        self.sentence_label.setStyleSheet("""
            QLabel {
                color: #00ff66;
                border: 2px solid #00ff66;
                font-size: 18px;
            }
        """)
        self.confidence_label.setText(
            f"Confidence: {result['confidence']*100:.1f}% | "
            f"Liveness: {result['liveness_score']*100:.1f}%"
        )
        self.confidence_label.setStyleSheet("color: #00ff66;")
        self.start_button.hide()
        
        if hasattr(self, 'avatar'):
            self.avatar.set_state("approved")
        
        # Voice response
        self.tts.speak("Authentication successful. Welcome. System access granted.")
        
        # Close after 2 seconds
        QTimer.singleShot(2000, self.grant_system_access)
    
    def on_authentication_failure(self, result):
        """Handle failed authentication"""
        self.failed_attempts += 1
        self.lockout.record_failed_attempt(self.username)
        self.audit.log_authentication_attempt(self.username, result)
        
        attempt_data = {
            "timestamp": datetime.now(),
            "voice_score": result.get("confidence", 0.0),
            "liveness_score": result.get("liveness_score", 0.0),
            "device_info": self._get_device_info(),
            "user_location": self._get_user_location()
        }
        
        threat_result = self.threat_detector.analyze_authentication_attempt(attempt_data)
        self.threat_detector.log_threat(threat_result)
        
        if self.failed_attempts >= 2:
            self.notification_system.send_alert("UNAUTHORIZED_ACCESS", {
                "attempt_number": self.failed_attempts,
                "threat_score": threat_result.get("threat_score", 0.0)
            })
        
        # Update UI
        self.status_label.setText("ACCESS DENIED")
        self.status_label.setStyleSheet("color: #ff3333; font-size: 32px;")
        self.sentence_label.setText(f"Attempt {self.failed_attempts}/{self.max_attempts}")
        self.sentence_label.setStyleSheet("""
            QLabel {
                color: #ff3333;
                border: 2px solid #ff3333;
            }
        """)
        self.confidence_label.setText(
            f"Confidence: {result['confidence']*100:.1f}% "
            f"(threshold: 98.0%)"
        )
        self.confidence_label.setStyleSheet("color: #ff3333;")
        
        # Voice response
        if self.failed_attempts >= self.max_attempts:
            self.tts.speak("Security violation confirmed. System locked.")
            self.message_label.setText("Too many failed attempts. System locked for 15 minutes.")
            if hasattr(self, 'avatar'):
                self.avatar.set_state("locked")
            
            self.notification_system.send_alert("SYSTEM_LOCKED", {
                "reason": "Multiple failed authentication attempts",
                "lockout_duration_minutes": 15
            })
        else:
            self.tts.speak("Unauthorized access detected. You are not permitted to use this system.")
            remaining = self.max_attempts - self.failed_attempts
            self.message_label.setText(
                f"Authentication failed. {remaining} attempt(s) remaining."
            )
            if hasattr(self, 'avatar'):
                self.avatar.set_state("denied")
        
        # Re-enable button
        QTimer.singleShot(2000, self.show_authentication_screen)
    
    def _get_device_info(self) -> dict:
        """Get device information"""
        import platform
        return {
            "platform": platform.system(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node()
        }
    
    def _get_user_location(self) -> dict:
        """Get user location (simplified - no actual geolocation)"""
        return {
            "latitude": 0.0,
            "longitude": 0.0,
            "timezone": "UTC"
        }
    
    def grant_system_access(self):
        """Grant access and close lockscreen"""
        self.close()
        sys.exit(0)
    
    def disable_system_keys(self):
        """Disable Alt+Tab, Ctrl+Alt+Del, and other system keys"""
        # This is OS-specific and requires ctypes/win32api
        # Simplified version for demonstration
        pass
    
    def keyPressEvent(self, event):
        """Block keyboard input"""
        if event.key() == Qt.Key_Alt or event.key() == Qt.Key_Tab:
            event.ignore()
        else:
            event.ignore()
    
    def mousePressEvent(self, event):
        """Block mouse interaction outside buttons"""
        # Only allow clicks on buttons
        event.ignore()
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.is_authenticated:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    lockscreen = SivajiLockscreen(failsafe_manager=DeveloperFailsafeManager())  # Initialize with DeveloperFailsafeManager
    lockscreen.show()
    sys.exit(app.exec_())
