"""
Advanced Threat Detection & Monitoring Engine
Analyzes authentication patterns and detects suspicious activity
"""

import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json


class ThreatDetectionEngine:
    """
    Multi-factor threat detection system
    - Analyzes authentication patterns
    - Detects anomalies
    - Triggers alerts
    """
    
    def __init__(self, config_path: str = "security/threat_config.json"):
        """Initialize threat detection engine"""
        self.config = self._load_config(config_path)
        self.threat_log = []
        self.baseline_patterns = {}
        self.anomaly_threshold = 0.7
    
    def _load_config(self, config_path: str) -> dict:
        """Load threat detection config"""
        default_config = {
            "max_failed_attempts": 5,
            "lockout_duration_minutes": 30,
            "anomaly_threshold": 0.7,
            "alert_on_threats": True,
            "capture_on_failure": True,
            "log_retention_days": 90,
            "timezone": "UTC",
            "threat_levels": {
                "LOW": 0.3,
                "MEDIUM": 0.6,
                "HIGH": 0.8,
                "CRITICAL": 0.95
            }
        }
        
        if Path(config_path).exists():
            with open(config_path) as f:
                loaded = json.load(f)
                default_config.update(loaded)
        
        return default_config
    
    def analyze_authentication_attempt(self, attempt_data: dict) -> dict:
        """
        Analyze single authentication attempt for threats
        
        Args:
            attempt_data: {
                "timestamp": datetime,
                "voice_score": float (0-1),
                "liveness_score": float (0-1),
                "face_score": float (0-1) if available,
                "iris_score": float (0-1) if available,
                "ip_address": str,
                "device_info": dict,
                "user_location": dict
            }
        
        Returns:
            {
                "threat_level": "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
                "threat_score": float (0-1),
                "threats_detected": [str],
                "confidence": float
            }
        """
        threats = []
        scores = []
        
        # 1. Biometric spoofing detection
        spoof_threat = self._detect_spoofing(attempt_data)
        if spoof_threat["threat_detected"]:
            threats.append(f"Spoofing: {spoof_threat['reason']}")
            scores.append(spoof_threat["score"])
        
        # 2. Behavioral anomaly detection
        behavior_threat = self._detect_behavior_anomaly(attempt_data)
        if behavior_threat["threat_detected"]:
            threats.append(f"Behavior: {behavior_threat['reason']}")
            scores.append(behavior_threat["score"])
        
        # 3. Location anomaly detection
        location_threat = self._detect_location_anomaly(attempt_data)
        if location_threat["threat_detected"]:
            threats.append(f"Location: {location_threat['reason']}")
            scores.append(location_threat["score"])
        
        # 4. Device anomaly detection
        device_threat = self._detect_device_anomaly(attempt_data)
        if device_threat["threat_detected"]:
            threats.append(f"Device: {device_threat['reason']}")
            scores.append(device_threat["score"])
        
        # 5. Timing anomaly detection
        timing_threat = self._detect_timing_anomaly(attempt_data)
        if timing_threat["threat_detected"]:
            threats.append(f"Timing: {timing_threat['reason']}")
            scores.append(timing_threat["score"])
        
        # Calculate final threat score
        if scores:
            threat_score = np.mean(scores)
            confidence = min(1.0, len(scores) / 5.0)  # Up to 5 threat factors
        else:
            threat_score = 0.0
            confidence = 1.0
        
        # Determine threat level
        threat_level = self._determine_threat_level(threat_score)
        
        return {
            "threat_level": threat_level,
            "threat_score": float(np.clip(threat_score, 0.0, 1.0)),
            "threats_detected": threats,
            "confidence": float(confidence),
            "details": {
                "spoof_threat": spoof_threat,
                "behavior_threat": behavior_threat,
                "location_threat": location_threat,
                "device_threat": device_threat,
                "timing_threat": timing_threat
            }
        }
    
    def _detect_spoofing(self, attempt_data: dict) -> dict:
        """Detect biometric spoofing attempts"""
        voice_score = attempt_data.get("voice_score", 1.0)
        liveness_score = attempt_data.get("liveness_score", 1.0)
        
        # Low scores indicate potential spoofing
        spoof_score = 1.0 - min(voice_score, liveness_score)
        
        threat_detected = spoof_score > 0.3
        
        return {
            "threat_detected": threat_detected,
            "score": spoof_score,
            "reason": f"Biometric quality low ({min(voice_score, liveness_score):.2f})" if threat_detected else "Normal"
        }
    
    def _detect_behavior_anomaly(self, attempt_data: dict) -> dict:
        """Detect unusual authentication behavior"""
        # Simplified behavior analysis
        voice_score = attempt_data.get("voice_score", 1.0)
        
        # Check for unusual patterns
        behavior_anomaly = abs(voice_score - 0.95) > 0.3
        
        return {
            "threat_detected": behavior_anomaly,
            "score": abs(voice_score - 0.95),
            "reason": "Unusual voice characteristics" if behavior_anomaly else "Normal behavior"
        }
    
    def _detect_location_anomaly(self, attempt_data: dict) -> dict:
        """Detect location-based anomalies"""
        location = attempt_data.get("user_location", {})
        
        # Placeholder: check against baseline locations
        return {
            "threat_detected": False,
            "score": 0.0,
            "reason": "Location normal"
        }
    
    def _detect_device_anomaly(self, attempt_data: dict) -> dict:
        """Detect device-based anomalies"""
        device_info = attempt_data.get("device_info", {})
        
        # Placeholder: check against known devices
        return {
            "threat_detected": False,
            "score": 0.0,
            "reason": "Device normal"
        }
    
    def _detect_timing_anomaly(self, attempt_data: dict) -> dict:
        """Detect timing-based anomalies (impossible travel, unusual hours)"""
        timestamp = attempt_data.get("timestamp", datetime.now())
        
        # Check for unusual login times
        hour = timestamp.hour
        unusual_time = hour < 6 or hour > 22
        
        return {
            "threat_detected": unusual_time,
            "score": 0.2 if unusual_time else 0.0,
            "reason": f"Login at unusual time ({hour}:00)" if unusual_time else "Normal hours"
        }
    
    def _determine_threat_level(self, threat_score: float) -> str:
        """Map threat score to threat level"""
        thresholds = self.config["threat_levels"]
        
        if threat_score >= thresholds["CRITICAL"]:
            return "CRITICAL"
        elif threat_score >= thresholds["HIGH"]:
            return "HIGH"
        elif threat_score >= thresholds["MEDIUM"]:
            return "MEDIUM"
        else:
            return "LOW"
    
    def log_threat(self, threat_data: dict):
        """Log threat event"""
        threat_data["timestamp"] = datetime.now().isoformat()
        self.threat_log.append(threat_data)
        
        # Keep only recent logs
        cutoff_date = datetime.now() - timedelta(days=self.config["log_retention_days"])
        self.threat_log = [t for t in self.threat_log if datetime.fromisoformat(t["timestamp"]) > cutoff_date]
    
    def get_threat_summary(self) -> dict:
        """Get summary of recent threats"""
        if not self.threat_log:
            return {"total_threats": 0, "critical_threats": 0, "last_threat": None}
        
        critical_count = sum(1 for t in self.threat_log if t.get("threat_level") == "CRITICAL")
        
        return {
            "total_threats": len(self.threat_log),
            "critical_threats": critical_count,
            "threat_levels": {
                "LOW": sum(1 for t in self.threat_log if t.get("threat_level") == "LOW"),
                "MEDIUM": sum(1 for t in self.threat_log if t.get("threat_level") == "MEDIUM"),
                "HIGH": sum(1 for t in self.threat_log if t.get("threat_level") == "HIGH"),
                "CRITICAL": critical_count
            },
            "last_threat": self.threat_log[-1]["timestamp"] if self.threat_log else None
        }
