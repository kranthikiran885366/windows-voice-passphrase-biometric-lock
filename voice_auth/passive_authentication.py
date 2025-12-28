"""
Passive Authentication & Behavior Monitoring
Continuous biometric authentication while user operates system
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from pathlib import Path


class PassiveAuthenticationMonitor:
    """
    Monitors user behavior continuously for authentication
    - Voice patterns while typing/speaking
    - Behavioral biometrics (typing patterns)
    - Activity patterns
    """
    
    def __init__(self, sensitivity: float = 0.85):
        """Initialize passive authentication monitor"""
        self.sensitivity = sensitivity
        self.baseline_voice_patterns = {}
        self.baseline_behaviors = {}
        self.current_session = None
        self.anomaly_threshold = 1.0 - sensitivity
        self.monitoring_enabled = True
    
    def start_session(self, username: str):
        """Start monitoring session for user"""
        self.current_session = {
            "username": username,
            "start_time": datetime.now(),
            "voice_samples": [],
            "behavior_samples": [],
            "activity_log": [],
            "anomaly_count": 0,
            "authentication_status": "authenticated"
        }
    
    def end_session(self) -> Dict:
        """End monitoring session"""
        session = self.current_session
        self.current_session = None
        return session
    
    def monitor_voice_activity(self, audio_sample: np.ndarray, timestamp: datetime = None) -> Dict:
        """
        Analyze voice activity during normal use
        Compares against baseline patterns
        """
        if not self.monitoring_enabled or not self.current_session:
            return {"anomaly": False, "confidence": 0.0}
        
        timestamp = timestamp or datetime.now()
        
        # Extract features from audio
        features = self._extract_voice_features(audio_sample)
        
        # Compare against baseline
        baseline = self.baseline_voice_patterns.get(self.current_session["username"], {})
        
        if not baseline:
            return {"anomaly": False, "confidence": 0.0, "reason": "No baseline"}
        
        # Calculate deviation
        deviation = self._calculate_deviation(features, baseline)
        
        # Anomaly detection
        anomaly_detected = deviation > self.anomaly_threshold
        confidence = min(1.0, deviation)
        
        # Log to session
        self.current_session["voice_samples"].append({
            "timestamp": timestamp,
            "features": features,
            "deviation": deviation,
            "anomaly": anomaly_detected
        })
        
        if anomaly_detected:
            self.current_session["anomaly_count"] += 1
        
        return {
            "anomaly": anomaly_detected,
            "confidence": confidence,
            "deviation": deviation,
            "features": features
        }
    
    def monitor_typing_behavior(self, keystroke_data: Dict) -> Dict:
        """
        Analyze typing patterns (keystroke dynamics)
        - Key press duration
        - Inter-key timing
        - Key pressure (if available)
        """
        if not self.monitoring_enabled or not self.current_session:
            return {"anomaly": False, "confidence": 0.0}
        
        # Extract typing features
        features = {
            "avg_key_duration": keystroke_data.get("key_duration", 0),
            "avg_inter_key_time": keystroke_data.get("inter_key_time", 0),
            "key_press_variance": keystroke_data.get("key_variance", 0),
            "typing_speed": keystroke_data.get("typing_speed", 0)
        }
        
        # Compare against baseline
        baseline = self.baseline_behaviors.get(self.current_session["username"], {})
        
        if not baseline:
            return {"anomaly": False, "confidence": 0.0}
        
        # Calculate deviation
        deviation = self._calculate_deviation(features, baseline)
        
        # Anomaly detection
        anomaly_detected = deviation > self.anomaly_threshold
        
        # Log to session
        self.current_session["behavior_samples"].append({
            "timestamp": datetime.now(),
            "features": features,
            "deviation": deviation,
            "anomaly": anomaly_detected
        })
        
        return {
            "anomaly": anomaly_detected,
            "confidence": min(1.0, deviation),
            "deviation": deviation
        }
    
    def set_baseline_patterns(self, username: str, voice_baseline: Dict, behavior_baseline: Dict):
        """Set baseline patterns for user"""
        self.baseline_voice_patterns[username] = voice_baseline
        self.baseline_behaviors[username] = behavior_baseline
    
    def _extract_voice_features(self, audio_sample: np.ndarray) -> Dict:
        """Extract voice features from audio"""
        # Simplified feature extraction
        return {
            "energy": float(np.mean(audio_sample**2)),
            "zero_crossing_rate": float(np.mean(np.abs(np.diff(np.sign(audio_sample))))),
            "spectral_centroid": float(np.mean(np.fft.fft(audio_sample))),
            "pitch": float(np.mean(audio_sample))
        }
    
    def _calculate_deviation(self, features: Dict, baseline: Dict) -> float:
        """Calculate deviation from baseline"""
        deviations = []
        
        for key in features:
            if key in baseline:
                baseline_val = baseline[key]
                current_val = features[key]
                
                if baseline_val != 0:
                    deviation = abs(current_val - baseline_val) / abs(baseline_val)
                    deviations.append(min(deviation, 1.0))
        
        return float(np.mean(deviations)) if deviations else 0.5
    
    def get_session_report(self) -> Dict:
        """Get report on current session"""
        if not self.current_session:
            return {}
        
        session = self.current_session
        total_samples = len(session["voice_samples"]) + len(session["behavior_samples"])
        
        if total_samples == 0:
            anomaly_rate = 0.0
        else:
            anomaly_rate = session["anomaly_count"] / total_samples
        
        auth_status = "authenticated" if anomaly_rate < 0.3 else "suspicious"
        
        return {
            "duration": (datetime.now() - session["start_time"]).total_seconds(),
            "total_samples": total_samples,
            "anomaly_count": session["anomaly_count"],
            "anomaly_rate": anomaly_rate,
            "auth_status": auth_status,
            "confidence": 1.0 - anomaly_rate
        }
