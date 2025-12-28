"""
System Configuration Management with Developer Fail-Safe Settings
Centralized configuration for Sivaji Security System
"""

import json
from pathlib import Path
from typing import Any, Dict
from dataclasses import dataclass, asdict


@dataclass
class SecurityConfig:
    """Security configuration"""
    max_failed_attempts: int = 5
    lockout_duration_minutes: int = 30
    authentication_timeout_seconds: int = 30
    voice_confidence_threshold: float = 0.98
    liveness_confidence_threshold: float = 0.90


@dataclass
class FailsafeConfig:
    """Developer fail-safe configuration"""
    enable_failsafe: bool = True
    failsafe_secret_length_min: int = 12
    failsafe_otk_validity_minutes: int = 15
    failsafe_max_uses_per_session: int = 3
    failsafe_timeout_seconds: int = 1800  # 30 minutes
    failsafe_physical_key_timeout_seconds: int = 10
    require_physical_confirmation: bool = True
    pbkdf2_iterations: int = 100000
    log_failsafe_events: bool = True


@dataclass
class BiometricConfig:
    """Biometric configuration"""
    enable_voice: bool = True
    enable_face: bool = False
    enable_iris: bool = False
    enable_passive_auth: bool = False
    voice_weight: float = 0.50
    face_weight: float = 0.25
    iris_weight: float = 0.15
    behavior_weight: float = 0.10


@dataclass
class UIConfig:
    """UI configuration"""
    theme: str = "dark"
    enable_avatar: bool = True
    avatar_3d: bool = True
    animation_fps: int = 30
    fullscreen: bool = True
    disable_mouse: bool = True
    disable_keyboard: bool = True


@dataclass
class NotificationConfig:
    """Notification configuration"""
    enable_email: bool = False
    enable_sms: bool = False
    enable_push: bool = True
    enable_system: bool = True
    alert_on_failed_attempt: bool = True
    alert_on_lockout: bool = True
    alert_on_critical_threat: bool = True


@dataclass
class SystemConfig:
    """Complete system configuration"""
    security: SecurityConfig
    failsafe: FailsafeConfig
    biometric: BiometricConfig
    ui: UIConfig
    notification: NotificationConfig
    
    @classmethod
    def load_from_file(cls, config_path: str = "config/system_config.json") -> "SystemConfig":
        """Load configuration from JSON file"""
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                config_dict = json.load(f)
            
            return cls(
                security=SecurityConfig(**config_dict.get("security", {})),
                failsafe=FailsafeConfig(**config_dict.get("failsafe", {})),
                biometric=BiometricConfig(**config_dict.get("biometric", {})),
                ui=UIConfig(**config_dict.get("ui", {})),
                notification=NotificationConfig(**config_dict.get("notification", {}))
            )
        else:
            return cls(
                security=SecurityConfig(),
                failsafe=FailsafeConfig(),
                biometric=BiometricConfig(),
                ui=UIConfig(),
                notification=NotificationConfig()
            )
    
    def save_to_file(self, config_path: str = "config/system_config.json"):
        """Save configuration to JSON file"""
        config_dict = {
            "security": asdict(self.security),
            "failsafe": asdict(self.failsafe),
            "biometric": asdict(self.biometric),
            "ui": asdict(self.ui),
            "notification": asdict(self.notification)
        }
        
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def get_active_biometrics(self) -> list:
        """Get list of active biometric methods"""
        active = []
        if self.biometric.enable_voice:
            active.append("voice")
        if self.biometric.enable_face:
            active.append("face")
        if self.biometric.enable_iris:
            active.append("iris")
        if self.biometric.enable_passive_auth:
            active.append("passive")
        return active
