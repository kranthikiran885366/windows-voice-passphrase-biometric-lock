"""
Advanced Verification Pipeline - Real-time voice authentication
Enhanced with confidence scoring, multi-factor analysis, and security metrics
"""

import numpy as np
import json
from pathlib import Path

from voice_auth.voice_processor import VoiceProcessor
from voice_auth.liveness_detector import LivenessDetector
from ai_models.model_inference import ModelInference
from security.encryption import EncryptionManager
from voice_bot.tts_engine import SivajiTTS


class VerificationPipeline:
    """Enhanced with advanced scoring and multi-factor authentication"""
    
    def __init__(self, username="authorized_user"):
        self.username = username
        self.voice_processor = VoiceProcessor()
        self.liveness = LivenessDetector()
        self.model_inference = ModelInference()
        self.encryption = EncryptionManager()
        self.tts = SivajiTTS()
        
        # Configurable thresholds
        self.confidence_threshold = 0.98
        self.liveness_threshold = 0.50
        self.similarity_threshold = 0.85
    
    def load_user_profile(self):
        """Load and decrypt user profile with validation"""
        cred_path = Path("security/credentials") / f"{self.username}.enc"
        
        if not cred_path.exists():
            raise FileNotFoundError(f"No profile found for {self.username}")
        
        try:
            with open(cred_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted = self.encryption.decrypt_data(encrypted_data)
            profile = json.loads(decrypted)
            return profile
        except Exception as e:
            raise ValueError(f"Failed to load profile: {e}")
    
    def extract_embedding_from_audio(self, audio_data):
        """Extract embedding from audio with validation"""
        try:
            if len(audio_data) < 8000:  # Less than 0.5 seconds at 16kHz
                return None
            
            audio_processed = audio_data / (np.max(np.abs(audio_data)) + 1e-8)
            mfcc = self.voice_processor.extract_mfcc(audio_processed)
            mfcc = self.voice_processor.pad_features(mfcc, target_length=50)
            embedding = self.model_inference.extract_embedding(mfcc)
            return embedding
        except Exception as e:
            print(f"[v0] Error extracting embedding: {e}")
            return None
    
    def compute_cosine_similarity(self, embedding1, embedding2):
        """Enhanced cosine similarity with numerical stability"""
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        embedding1 = np.array(embedding1, dtype=np.float32)
        embedding2 = np.array(embedding2, dtype=np.float32)
        
        # L2 normalize
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 < 1e-8 or norm2 < 1e-8:
            return 0.0
        
        embedding1 = embedding1 / norm1
        embedding2 = embedding2 / norm2
        
        dot_product = np.dot(embedding1, embedding2)
        similarity = np.clip(dot_product, -1, 1)
        
        # Convert [-1, 1] to [0, 1]
        return (similarity + 1) / 2
    
    def analyze_voice_quality(self, audio_data):
        """Added voice quality assessment"""
        try:
            energy = self.voice_processor.get_energy(audio_data)
            zcr = self.voice_processor.get_zero_crossing_rate(audio_data)
            spectral_cent = self.voice_processor.get_spectral_centroid(audio_data)
            
            # Quality metrics (0-1)
            energy_level = np.mean(energy) / (np.max(energy) + 1e-8)
            zcr_variation = np.std(zcr) / (np.mean(zcr) + 1e-8)
            spectral_variation = np.std(spectral_cent) / (np.mean(spectral_cent) + 1e-8)
            
            quality_score = (
                0.4 * min(energy_level, 1.0) +
                0.3 * min(zcr_variation, 1.0) +
                0.3 * min(spectral_variation, 1.0)
            )
            
            return np.clip(quality_score, 0, 1)
        except:
            return 0.5
    
    def verify_voice(self, audio_data):
        """
        Enhanced multi-factor verification with detailed scoring
        
        Returns:
            dict with:
            - authenticated: bool
            - confidence: float (0-1)
            - liveness_score: float (0-1)
            - similarity_score: float (0-1)
            - voice_quality: float (0-1)
            - details: dict with breakdown
        """
        try:
            # Load profile
            profile = self.load_user_profile()
            
            # 1. Liveness detection
            liveness_score = self.liveness.compute_liveness_score(audio_data)
            if liveness_score < self.liveness_threshold:
                return {
                    'authenticated': False,
                    'confidence': 0.0,
                    'liveness_score': liveness_score,
                    'similarity_score': 0.0,
                    'voice_quality': 0.0,
                    'reason': f'Liveness check failed ({liveness_score:.2f} < {self.liveness_threshold:.2f})',
                    'details': {
                        'liveness': liveness_score,
                        'status': 'POSSIBLE_PLAYBACK_DETECTED'
                    }
                }
            
            # 2. Voice quality assessment
            voice_quality = self.analyze_voice_quality(audio_data)
            
            # 3. Embedding extraction
            current_embedding = self.extract_embedding_from_audio(audio_data)
            if current_embedding is None:
                return {
                    'authenticated': False,
                    'confidence': 0.0,
                    'liveness_score': liveness_score,
                    'similarity_score': 0.0,
                    'voice_quality': voice_quality,
                    'reason': 'Failed to extract voice features',
                    'details': {
                        'liveness': liveness_score,
                        'quality': voice_quality,
                        'status': 'FEATURE_EXTRACTION_FAILED'
                    }
                }
            
            # 4. Similarity comparison
            stored_embedding = np.array(profile['mean_embedding'])
            similarity = self.compute_cosine_similarity(
                current_embedding,
                stored_embedding
            )
            
            if similarity < self.similarity_threshold:
                return {
                    'authenticated': False,
                    'confidence': similarity,
                    'liveness_score': liveness_score,
                    'similarity_score': similarity,
                    'voice_quality': voice_quality,
                    'reason': f'Similarity {similarity:.2f} below threshold {self.similarity_threshold:.2f}',
                    'details': {
                        'liveness': liveness_score,
                        'similarity': similarity,
                        'quality': voice_quality,
                        'status': 'IDENTITY_MISMATCH'
                    }
                }
            
            # 5. Multi-factor confidence score
            confidence = (
                0.50 * similarity +          # Speaker verification
                0.30 * liveness_score +      # Liveness detection
                0.15 * voice_quality +       # Voice quality
                0.05 * (1.0 if similarity > 0.95 else 0)  # Bonus for high confidence
            )
            
            # Decision threshold
            authenticated = confidence >= self.confidence_threshold
            
            return {
                'authenticated': authenticated,
                'confidence': float(np.clip(confidence, 0, 1)),
                'liveness_score': float(liveness_score),
                'similarity_score': float(similarity),
                'voice_quality': float(voice_quality),
                'reason': 'Authenticated' if authenticated else f'Confidence {confidence:.2f} below threshold {self.confidence_threshold:.2f}',
                'details': {
                    'liveness': float(liveness_score),
                    'similarity': float(similarity),
                    'quality': float(voice_quality),
                    'overall_confidence': float(confidence),
                    'status': 'AUTHENTICATED' if authenticated else 'AUTHENTICATION_FAILED'
                }
            }
        
        except Exception as e:
            return {
                'authenticated': False,
                'confidence': 0.0,
                'liveness_score': 0.0,
                'similarity_score': 0.0,
                'voice_quality': 0.0,
                'reason': f'Verification error: {str(e)}',
                'details': {
                    'status': 'VERIFICATION_ERROR',
                    'error': str(e)
                }
            }
