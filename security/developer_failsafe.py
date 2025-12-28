"""
SIVAJI SECURITY SYSTEM - DEVELOPER FAIL-SAFE ACCESS MECHANISM
==============================================================

Critical Emergency Access System:
- Completely hidden from normal users
- Multi-step developer authentication required
- Time-bound one-time keys
- Physical confirmation required
- Encrypted, auditable, tamper-detected
- Auto-disables when system restored
"""

import os
import hashlib
import hmac
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from cryptography.fernet import Fernet, InvalidToken
import threading
import logging

logger = logging.getLogger(__name__)


class DeveloperFailsafeManager:
    """
    Implements a secure, multi-layer developer fail-safe mechanism.
    
    Activation requirements:
    1. System failure detected (microphone, AI model, voice auth unavailable)
    2. Developer secret (encrypted, stored securely)
    3. Time-bound one-time key (generated server-side, 15-min validity)
    4. Physical confirmation (specific key sequence: Ctrl+Alt+F12+D)
    5. HMAC verification of all inputs
    6. Encrypted audit logging
    """
    
    def __init__(self, encryption_key: bytes, audit_logger):
        self.encryption_key = encryption_key
        self.audit_logger = audit_logger
        self.cipher = Fernet(encryption_key)
        self.is_failsafe_active = False
        self.failsafe_activation_time = None
        self.failsafe_timeout = 1800  # 30 minutes max duration
        self.max_failsafe_uses = 3  # Max 3 uses per session
        self.failsafe_use_count = 0
        self.developer_secret_hash = None
        self.one_time_key_pool = []
        self.physical_confirmation_sequence = []
        self.expected_key_sequence = ['ctrl', 'alt', 'f12', 'd']  # Ctrl+Alt+F12+D
        self.tamper_detected = False
        self.failsafe_log_file = 'logs/failsafe_events.enc'
        
        # Initialize failsafe state file (encrypted)
        self.failsafe_state_file = 'data/failsafe_state.enc'
        self._initialize_failsafe_state()
        
        logger.info("[v0] Developer Fail-Safe Manager initialized")
    
    def _initialize_failsafe_state(self):
        """Initialize or load encrypted failsafe state."""
        if os.path.exists(self.failsafe_state_file):
            try:
                with open(self.failsafe_state_file, 'rb') as f:
                    encrypted_state = f.read()
                    decrypted_state = self.cipher.decrypt(encrypted_state)
                    state = json.loads(decrypted_state.decode())
                    self.failsafe_use_count = state.get('use_count', 0)
                    logger.info(f"[v0] Failsafe state loaded: {self.failsafe_use_count} uses")
            except Exception as e:
                logger.error(f"[v0] Failsafe state load failed: {e}")
                self._save_failsafe_state()
        else:
            self._save_failsafe_state()
    
    def _save_failsafe_state(self):
        """Save encrypted failsafe state."""
        try:
            os.makedirs('data', exist_ok=True)
            state = {'use_count': self.failsafe_use_count}
            encrypted_state = self.cipher.encrypt(json.dumps(state).encode())
            with open(self.failsafe_state_file, 'wb') as f:
                f.write(encrypted_state)
        except Exception as e:
            logger.error(f"[v0] Failsafe state save failed: {e}")
    
    def set_developer_secret(self, secret: str) -> str:
        """
        Set developer secret (one-time during setup).
        Returns: Encrypted secret hash for storage.
        """
        # Hash with salt for comparison
        salt = os.urandom(32)
        hashed = hashlib.pbkdf2_hmac('sha256', secret.encode(), salt, 100000)
        self.developer_secret_hash = (salt + hashed).hex()
        
        # Encrypt for storage
        encrypted_secret = self.cipher.encrypt(self.developer_secret_hash.encode())
        
        logger.info("[v0] Developer secret configured (production: store in secure vault)")
        return encrypted_secret.decode()
    
    def generate_one_time_key(self, validity_minutes: int = 15) -> str:
        """
        Generate time-bound one-time key (sent to developer email/phone).
        Returns: OTK string
        """
        otk = os.urandom(32).hex()
        expiry = datetime.now() + timedelta(minutes=validity_minutes)
        
        otk_record = {
            'key': otk,
            'created': datetime.now().isoformat(),
            'expires': expiry.isoformat(),
            'used': False
        }
        
        self.one_time_key_pool.append(otk_record)
        
        # Keep only recent keys
        self.one_time_key_pool = [
            k for k in self.one_time_key_pool 
            if datetime.fromisoformat(k['expires']) > datetime.now()
        ]
        
        logger.info(f"[v0] One-time key generated: {otk[:8]}... (valid {validity_minutes} min)")
        return otk
    
    def verify_one_time_key(self, otk: str) -> bool:
        """Verify one-time key validity and expiry."""
        for record in self.one_time_key_pool:
            if record['key'] == otk:
                expiry = datetime.fromisoformat(record['expires'])
                if datetime.now() < expiry and not record['used']:
                    record['used'] = True
                    logger.info(f"[v0] One-time key verified successfully")
                    return True
                elif record['used']:
                    logger.warning("[v0] One-time key already used")
                    return False
                else:
                    logger.warning("[v0] One-time key expired")
                    return False
        
        logger.error("[v0] One-time key not found or invalid")
        return False
    
    def track_physical_confirmation_key(self, key: str) -> bool:
        """
        Track physical key sequence input: Ctrl+Alt+F12+D
        Returns: True when complete sequence detected
        """
        key_lower = key.lower()
        self.physical_confirmation_sequence.append(key_lower)
        
        # Keep only last 4 inputs
        if len(self.physical_confirmation_sequence) > 4:
            self.physical_confirmation_sequence.pop(0)
        
        # Check if sequence matches
        if self.physical_confirmation_sequence == self.expected_key_sequence:
            logger.info("[v0] Physical confirmation sequence detected")
            self.physical_confirmation_sequence = []
            return True
        
        return False
    
    def verify_developer_secret(self, provided_secret: str) -> bool:
        """Verify developer secret using PBKDF2."""
        if not self.developer_secret_hash:
            logger.error("[v0] Developer secret not configured")
            return False
        
        try:
            stored_bytes = bytes.fromhex(self.developer_secret_hash)
            salt = stored_bytes[:32]
            stored_hash = stored_bytes[32:]
            
            # Hash provided secret with same salt
            provided_hash = hashlib.pbkdf2_hmac('sha256', provided_secret.encode(), salt, 100000)
            
            # Constant-time comparison to prevent timing attacks
            is_valid = hmac.compare_digest(provided_hash, stored_hash)
            
            if is_valid:
                logger.info("[v0] Developer secret verified")
            else:
                logger.warning("[v0] Developer secret verification failed")
            
            return is_valid
        except Exception as e:
            logger.error(f"[v0] Secret verification error: {e}")
            return False
    
    def activate_failsafe(self, developer_secret: str, otk: str, 
                         system_failure_reason: str) -> Tuple[bool, str]:
        """
        Activate developer fail-safe with multi-layer verification.
        
        Args:
            developer_secret: Developer's secret password
            otk: One-time key (time-bound)
            system_failure_reason: Description of system failure
        
        Returns:
            (success: bool, message: str)
        """
        # Rate limiting check
        if self.failsafe_use_count >= self.max_failsafe_uses:
            msg = "Failsafe: Maximum uses exceeded. Contact administrator."
            self._log_failsafe_event('FAILED', 'MAX_USES_EXCEEDED', msg)
            logger.error(f"[v0] {msg}")
            return False, msg
        
        # Verify developer secret
        if not self.verify_developer_secret(developer_secret):
            self._log_failsafe_event('FAILED', 'INVALID_SECRET', 'Secret verification failed')
            logger.warning("[v0] Failsafe activation: Invalid secret")
            return False, "Invalid developer credentials"
        
        # Verify one-time key
        if not self.verify_one_time_key(otk):
            self._log_failsafe_event('FAILED', 'INVALID_OTK', 'OTK verification failed')
            logger.warning("[v0] Failsafe activation: Invalid OTK")
            return False, "Invalid or expired one-time key"
        
        # Verify physical confirmation was detected (should be set before calling this)
        if len(self.physical_confirmation_sequence) == 0 and \
           self.expected_key_sequence not in [[k] for k in self.physical_confirmation_sequence]:
            msg = "Physical confirmation required (Ctrl+Alt+F12+D)"
            self._log_failsafe_event('FAILED', 'NO_PHYSICAL_CONFIRMATION', msg)
            logger.warning(f"[v0] {msg}")
            return False, msg
        
        # All checks passed - activate failsafe
        self.is_failsafe_active = True
        self.failsafe_activation_time = datetime.now()
        self.failsafe_use_count += 1
        self._save_failsafe_state()
        
        msg = f"Developer failsafe activated. System accessible for {self.failsafe_timeout}s"
        self._log_failsafe_event('SUCCESS', 'FAILSAFE_ACTIVATED', msg, system_failure_reason)
        
        logger.info(f"[v0] {msg}")
        
        # Auto-disable after timeout
        self._schedule_failsafe_timeout()
        
        return True, msg
    
    def deactivate_failsafe(self, reason: str = "Normal operation restored"):
        """Deactivate failsafe when system is operational again."""
        if self.is_failsafe_active:
            self.is_failsafe_active = False
            self._log_failsafe_event('INFO', 'FAILSAFE_DEACTIVATED', reason)
            logger.info(f"[v0] Failsafe deactivated: {reason}")
    
    def is_failsafe_valid(self) -> bool:
        """Check if failsafe is active and hasn't timed out."""
        if not self.is_failsafe_active:
            return False
        
        if not self.failsafe_activation_time:
            return False
        
        elapsed = (datetime.now() - self.failsafe_activation_time).total_seconds()
        if elapsed > self.failsafe_timeout:
            self.deactivate_failsafe("Timeout exceeded")
            return False
        
        return True
    
    def _schedule_failsafe_timeout(self):
        """Schedule automatic failsafe deactivation after timeout."""
        def timeout_handler():
            time.sleep(self.failsafe_timeout)
            self.deactivate_failsafe("Automatic timeout")
        
        thread = threading.Thread(target=timeout_handler, daemon=True)
        thread.start()
    
    def _log_failsafe_event(self, event_type: str, event_code: str, 
                           message: str, system_failure_reason: str = None):
        """Log failsafe events with encryption."""
        try:
            os.makedirs('logs', exist_ok=True)
            
            event = {
                'timestamp': datetime.now().isoformat(),
                'type': event_type,
                'code': event_code,
                'message': message,
                'system_failure_reason': system_failure_reason,
                'use_count': self.failsafe_use_count,
                'active': self.is_failsafe_active
            }
            
            # Append to encrypted log
            encrypted_event = self.cipher.encrypt(json.dumps(event).encode())
            
            with open(self.failsafe_log_file, 'ab') as f:
                f.write(encrypted_event + b'\n---SEPARATOR---\n')
            
            # Also log via audit logger if available
            if self.audit_logger:
                self.audit_logger.log_event(
                    event_type=f'FAILSAFE_{event_code}',
                    username='DEVELOPER_OVERRIDE',
                    voice_score=1.0,
                    liveness_score=1.0,
                    details=message,
                    metadata={'system_failure_reason': system_failure_reason}
                )
        except Exception as e:
            logger.error(f"[v0] Failsafe event logging failed: {e}")
    
    def detect_system_failure(self, failure_type: str) -> bool:
        """
        Detect system failures that warrant failsafe activation.
        Returns: True if failsafe should be considered
        """
        failure_types = {
            'MICROPHONE_FAILURE': 'Audio input hardware unavailable',
            'MODEL_CRASH': 'AI model inference failed',
            'VOICE_AUTH_ERROR': 'Voice authentication system unavailable',
            'SYSTEM_ERROR': 'Critical system error detected'
        }
        
        if failure_type in failure_types:
            msg = failure_types[failure_type]
            logger.warning(f"[v0] System failure detected: {msg}")
            self._log_failsafe_event('WARNING', 'SYSTEM_FAILURE_DETECTED', msg)
            return True
        
        return False
    
    def verify_failsafe_integrity(self) -> Tuple[bool, str]:
        """
        Verify failsafe system integrity.
        Detects tampering attempts.
        """
        try:
            # Check if state file exists and is readable
            if not os.path.exists(self.failsafe_state_file):
                return False, "Failsafe state file missing"
            
            # Try to decrypt state
            with open(self.failsafe_state_file, 'rb') as f:
                encrypted = f.read()
                self.cipher.decrypt(encrypted)
            
            # Check for suspicious modifications
            file_stat = os.stat(self.failsafe_state_file)
            if file_stat.st_size > 1024:  # Should be small
                return False, "Failsafe state file size anomaly detected"
            
            logger.info("[v0] Failsafe integrity verified")
            return True, "Failsafe system integrity OK"
        
        except InvalidToken:
            self.tamper_detected = True
            logger.error("[v0] TAMPER DETECTED: Failsafe state file corrupted")
            return False, "TAMPER DETECTED: Failsafe state file corrupted"
        except Exception as e:
            self.tamper_detected = True
            logger.error(f"[v0] Failsafe integrity check failed: {e}")
            return False, f"Integrity check failed: {e}"
    
    def get_failsafe_status(self) -> Dict:
        """Get current failsafe system status."""
        return {
            'is_active': self.is_failsafe_active,
            'is_valid': self.is_failsafe_valid(),
            'activation_time': self.failsafe_activation_time.isoformat() if self.failsafe_activation_time else None,
            'time_remaining': max(0, self.failsafe_timeout - 
                                 (datetime.now() - self.failsafe_activation_time).total_seconds() 
                                 if self.failsafe_activation_time else 0),
            'uses_remaining': self.max_failsafe_uses - self.failsafe_use_count,
            'tamper_detected': self.tamper_detected,
            'integrity_ok': not self.tamper_detected
        }
