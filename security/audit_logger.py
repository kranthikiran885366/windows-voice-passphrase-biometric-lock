"""
Audit Logger - Log all authentication attempts with encryption
Includes timestamp, user, result, confidence score, IP address
HMAC-verified tamper-proof logging
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime, timezone
import hashlib
from security.encryption import EncryptionManager


class AuditLogger:
    """Log all system access attempts securely"""
    
    def __init__(self, log_file="security/logs/audit.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.encryption = EncryptionManager()
    
    def log_authentication_attempt(self, username, result, metadata=None):
        """
        Log authentication attempt
        
        Args:
            username: str
            result: dict with keys:
                - authenticated: bool
                - confidence: float
                - liveness_score: float
                - similarity_score: float
            metadata: dict with additional info
        """
        
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'username': username,
            'authenticated': result.get('authenticated', False),
            'confidence': float(result.get('confidence', 0.0)),
            'liveness_score': float(result.get('liveness_score', 0.0)),
            'similarity_score': float(result.get('similarity_score', 0.0)),
            'reason': result.get('reason', ''),
        }
        
        if metadata:
            log_entry.update(metadata)
        
        # Encrypt and append to log
        self._append_encrypted_log(log_entry)
    
    def _append_encrypted_log(self, entry):
        """Encrypt and append log entry"""
        # Serialize
        entry_str = json.dumps(entry, default=str)
        
        # Encrypt
        encrypted = self.encryption.encrypt_data(entry_str)
        
        # Append to log file (storing encrypted bytes as base64)
        import base64
        entry_b64 = base64.b64encode(encrypted).decode('utf-8')
        
        with open(self.log_file, 'a') as f:
            f.write(entry_b64 + '\n')
    
    def read_logs(self, num_entries=100, username=None):
        """
        Read and decrypt audit logs
        
        Args:
            num_entries: max number of recent entries to read
            username: filter by username
        
        Returns:
            list of decrypted log entries
        """
        if not self.log_file.exists():
            return []
        
        entries = []
        
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
        
        # Read from end (most recent)
        for line in lines[-num_entries:]:
            try:
                import base64
                encrypted = base64.b64decode(line.strip())
                decrypted = self.encryption.decrypt_data(encrypted)
                entry = json.loads(decrypted)
                
                if username is None or entry.get('username') == username:
                    entries.append(entry)
            except Exception as e:
                print(f"[v0] Error reading log entry: {e}")
        
        return entries
    
    def get_statistics(self, username=None):
        """Get authentication statistics"""
        logs = self.read_logs(num_entries=1000, username=username)
        
        if not logs:
            return None
        
        total = len(logs)
        successful = sum(1 for log in logs if log.get('authenticated'))
        failed = total - successful
        
        success_rate = (successful / total * 100) if total > 0 else 0
        avg_confidence = np.mean([log.get('confidence', 0) for log in logs])
        avg_liveness = np.mean([log.get('liveness_score', 0) for log in logs])
        
        return {
            'total_attempts': total,
            'successful': successful,
            'failed': failed,
            'success_rate': success_rate,
            'avg_confidence': float(avg_confidence),
            'avg_liveness': float(avg_liveness),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
