"""
Enrollment Pipeline - Collect voice samples and train user profile
User speaks 5 sentences, system extracts and encrypts voice embeddings
"""

import numpy as np
from pathlib import Path
import json
import soundfile as sf

from voice_auth.voice_processor import VoiceProcessor
from ai_models.model_inference import ModelInference
from security.encryption import EncryptionManager
from voice_bot.tts_engine import SivajiTTS


class EnrollmentPipeline:
    """Manage user voice enrollment"""
    
    ENROLLMENT_SENTENCES = [
        "The quick brown fox jumps over the lazy dog",
        "Sivaji is the most advanced security system ever created",
        "My voice is my password and my identity",
        "Authentication complete and system is now accessible",
        "Unauthorized users will be denied immediate access"
    ]
    
    def __init__(self, username="authorized_user", debug=False):
        self.username = username
        self.debug = debug
        self.voice_processor = VoiceProcessor()
        self.model_inference = ModelInference()
        self.encryption = EncryptionManager()
        self.tts = SivajiTTS()
        
        # Setup directories
        self.enrollment_dir = Path("enrollment_data") / username
        self.enrollment_dir.mkdir(parents=True, exist_ok=True)
        
    def record_sample(self, sentence_idx, audio_data):
        """Store recorded audio sample"""
        sample_path = self.enrollment_dir / f"sample_{sentence_idx}.wav"
        sf.write(sample_path, audio_data, self.voice_processor.sample_rate)
        return sample_path
    
    def extract_embedding_from_audio(self, audio_data):
        """Extract speaker embedding from audio using trained model"""
        try:
            # Process audio
            audio_processed = audio_data / (np.max(np.abs(audio_data)) + 1e-8)
            
            # Extract features
            mfcc = self.voice_processor.extract_mfcc(audio_processed)
            mfcc = self.voice_processor.pad_features(mfcc, target_length=50)
            
            # Get embedding from model (last layer before classification)
            embedding = self.model_inference.extract_embedding(mfcc)
            
            return embedding
        except Exception as e:
            print(f"Error extracting embedding: {e}")
            return None
    
    def create_user_profile(self, embeddings):
        """
        Create user voice profile from multiple embeddings
        Stores mean embedding and covariance matrix
        """
        embeddings = np.array(embeddings)
        
        profile = {
            'username': self.username,
            'enrollment_date': str(np.datetime64('now')),
            'num_samples': len(embeddings),
            'mean_embedding': embeddings.mean(axis=0).tolist(),
            'std_embedding': embeddings.std(axis=0).tolist(),
            'embedding_dim': embeddings.shape[1],
        }
        
        return profile
    
    def save_encrypted_profile(self, profile):
        """Encrypt and save user profile"""
        encrypted_profile = self.encryption.encrypt_data(
            json.dumps(profile, default=float)
        )
        
        cred_path = Path("security/credentials") / f"{self.username}.enc"
        cred_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(cred_path, 'wb') as f:
            f.write(encrypted_profile)
        
        print(f"\n✓ User profile saved (encrypted): {cred_path}")
    
    def run_enrollment(self):
        """Run complete enrollment process"""
        print("\n" + "="*60)
        print(f"ENROLLMENT: {self.username}")
        print("="*60)
        print("\nYou will speak 5 sentences to create your voice profile.")
        print("Speak clearly and naturally.\n")
        
        embeddings = []
        
        for i, sentence in enumerate(self.ENROLLMENT_SENTENCES, 1):
            print(f"\n[{i}/5] Speak this sentence:")
            print(f'     "{sentence}"')
            print("\nPress ENTER when ready to record (recording will be 5 seconds)...")
            input()
            
            # Simulate recording (in real implementation, use PyAudio)
            print(f"Recording... (this would record 5 seconds of audio)")
            
            # For demo, generate synthetic audio
            audio_data = np.random.randn(16000 * 5) * 0.1  # 5 seconds @ 16kHz
            
            # Save sample
            self.record_sample(i-1, audio_data)
            
            # Extract embedding
            embedding = self.extract_embedding_from_audio(audio_data)
            if embedding is not None:
                embeddings.append(embedding)
                print(f"✓ Sample {i} processed")
            else:
                print(f"✗ Failed to process sample {i}")
        
        if len(embeddings) >= 3:
            # Create and save profile
            profile = self.create_user_profile(embeddings)
            self.save_encrypted_profile(profile)
            
            self.tts.speak(
                "Enrollment successful. Your voice profile has been created. "
                "You can now use the system."
            )
            print("\n✓ Enrollment complete!")
        else:
            print("\n✗ Enrollment failed: not enough valid samples")
