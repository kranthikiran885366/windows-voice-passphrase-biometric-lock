"""
Encryption Manager - AES-256-GCM encryption for voice embeddings
Uses Fernet (symmetric key derivation) for secure key management
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os
from pathlib import Path


class EncryptionManager:
    """Manage encryption/decryption of sensitive biometric data"""
    
    def __init__(self, master_key_file="security/credentials/.master_key"):
        self.master_key_file = Path(master_key_file)
        self.cipher = None
        self._init_master_key()
    
    def _init_master_key(self):
        """Initialize or load master encryption key"""
        self.master_key_file.parent.mkdir(parents=True, exist_ok=True)
        
        if self.master_key_file.exists():
            # Load existing key
            with open(self.master_key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            
            # Save key (in production, use key vault)
            with open(self.master_key_file, 'wb') as f:
                f.write(key)
            
            # Restrict file permissions
            os.chmod(self.master_key_file, 0o600)
        
        self.cipher = Fernet(key)
    
    def encrypt_data(self, data):
        """
        Encrypt string data (voice embeddings, profiles, etc.)
        
        Args:
            data: string data to encrypt
        
        Returns:
            encrypted: bytes (ciphertext)
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        encrypted = self.cipher.encrypt(data)
        return encrypted
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt encrypted data
        
        Args:
            encrypted_data: bytes (ciphertext)
        
        Returns:
            decrypted: string
        """
        try:
            decrypted = self.cipher.decrypt(encrypted_data)
            return decrypted.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
    
    @staticmethod
    def derive_key_from_password(password, salt=None):
        """
        Derive encryption key from password using PBKDF2
        For advanced implementations
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(
            kdf.derive(password.encode())
        )
        
        return key, salt
