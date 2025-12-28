"""
Lockout Manager - Track failed attempts and apply lockouts
After 3 failures, system locks for configurable time
"""

import json
from pathlib import Path
from datetime import datetime, timedelta, timezone


class LockoutManager:
    """Manage failed attempt tracking and security lockouts"""
    
    def __init__(self, lockout_file="security/lockout.json", max_attempts=3, lockout_duration_minutes=15):
        self.lockout_file = Path(lockout_file)
        self.lockout_file.parent.mkdir(parents=True, exist_ok=True)
        self.max_attempts = max_attempts
        self.lockout_duration = timedelta(minutes=lockout_duration_minutes)
        self.lockout_data = self._load_lockout_data()
    
    def _load_lockout_data(self):
        """Load lockout state from file"""
        if self.lockout_file.exists():
            try:
                with open(self.lockout_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_lockout_data(self):
        """Save lockout state to file"""
        with open(self.lockout_file, 'w') as f:
            json.dump(self.lockout_data, f, indent=2)
    
    def record_failed_attempt(self, username):
        """Record a failed authentication attempt"""
        if username not in self.lockout_data:
            self.lockout_data[username] = {
                'failed_attempts': 0,
                'last_attempt': None,
                'locked_until': None
            }
        
        self.lockout_data[username]['failed_attempts'] += 1
        self.lockout_data[username]['last_attempt'] = datetime.now(timezone.utc).isoformat()
        
        # Check if should lock
        if self.lockout_data[username]['failed_attempts'] >= self.max_attempts:
            lock_until = (datetime.now(timezone.utc) + self.lockout_duration).isoformat()
            self.lockout_data[username]['locked_until'] = lock_until
        
        self._save_lockout_data()
    
    def record_successful_attempt(self, username):
        """Reset failed attempts on successful authentication"""
        if username in self.lockout_data:
            self.lockout_data[username]['failed_attempts'] = 0
            self.lockout_data[username]['locked_until'] = None
        
        self._save_lockout_data()
    
    def is_locked(self, username):
        """Check if user is currently locked out"""
        if username not in self.lockout_data:
            return False
        
        locked_until = self.lockout_data[username].get('locked_until')
        if not locked_until:
            return False
        
        lock_time = datetime.fromisoformat(locked_until)
        if datetime.now(timezone.utc) > lock_time:
            # Lockout expired
            self.lockout_data[username]['locked_until'] = None
            self._save_lockout_data()
            return False
        
        return True
    
    def get_lockout_time_remaining(self, username):
        """Get remaining lockout time in seconds"""
        if username not in self.lockout_data:
            return 0
        
        locked_until = self.lockout_data[username].get('locked_until')
        if not locked_until:
            return 0
        
        lock_time = datetime.fromisoformat(locked_until)
        remaining = lock_time - datetime.now(timezone.utc)
        
        return max(0, int(remaining.total_seconds()))
    
    def get_failed_attempts(self, username):
        """Get number of failed attempts"""
        if username not in self.lockout_data:
            return 0
        return self.lockout_data[username]['failed_attempts']
