"""
Voice Processor - MFCC Feature Extraction with Advanced Audio Analysis
Converts raw audio to 13-dimensional MFCC features for speaker recognition
Includes advanced preprocessing and feature engineering
"""

import numpy as np
import librosa
from scipy import signal
import soundfile as sf
import warnings
warnings.filterwarnings('ignore')


class VoiceProcessor:
    """Process audio into speaker recognition features with advanced techniques"""
    
    def __init__(self, sample_rate=16000, n_mfcc=13):
        self.sample_rate = sample_rate
        self.n_mfcc = n_mfcc
        self.n_fft = 2048
        self.hop_length = 512
        self.n_mels = 40
        
    def load_audio(self, audio_path):
        """Load audio file and normalize with noise floor filtering"""
        audio, sr = librosa.load(audio_path, sr=self.sample_rate)
        # Normalize
        audio = audio / (np.max(np.abs(audio)) + 1e-8)
        return audio
    
    def apply_preemphasis(self, audio, coeff=0.97):
        """Apply pre-emphasis filter to enhance high frequencies"""
        return np.append(audio[0], audio[1:] - coeff * audio[:-1])
    
    def remove_silence(self, audio, threshold=0.02):
        """Remove silence frames using energy-based VAD"""
        energy = np.sqrt(np.convolve(audio**2, np.ones(self.hop_length), mode='same'))
        energy_norm = (energy - np.min(energy)) / (np.max(energy) - np.min(energy) + 1e-8)
        voiced_frames = energy_norm > threshold
        
        # Keep audio only in voiced frames
        voiced_audio = audio[voiced_frames]
        return voiced_audio if len(voiced_audio) > 0 else audio
    
    def extract_mfcc(self, audio):
        """
        Extract MFCC features with advanced preprocessing
        Uses delta (velocity) and delta-delta (acceleration) features
        Output shape: (n_mfcc, time_steps)
        """
        # Pre-emphasis
        audio_emphasized = self.apply_preemphasis(audio)
        
        mfcc = librosa.feature.mfcc(
            y=audio_emphasized,
            sr=self.sample_rate,
            n_mfcc=self.n_mfcc,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        return mfcc
    
    def extract_spectrogram(self, audio):
        """Extract mel-scale spectrogram with perceptual scaling"""
        audio_emphasized = self.apply_preemphasis(audio)
        spec = librosa.feature.melspectrogram(
            y=audio_emphasized,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length,
            n_mels=self.n_mels
        )
        spec_db = librosa.power_to_db(spec, ref=np.max)
        return spec_db
    
    def extract_chromagram(self, audio):
        """Extract chroma features (pitch-based)"""
        chroma = librosa.feature.chroma_cqt(
            y=audio,
            sr=self.sample_rate
        )
        return chroma
    
    def extract_tempogram(self, audio):
        """Extract temporal dynamics"""
        onset_env = librosa.onset.onset_strength(y=audio, sr=self.sample_rate)
        tempo, _ = librosa.beat.beat_track(onset_env=onset_env, sr=self.sample_rate)
        return tempo
    
    def get_zero_crossing_rate(self, audio):
        """Compute zero crossing rate for voice quality assessment"""
        zcr = librosa.feature.zero_crossing_rate(audio, hop_length=self.hop_length)[0]
        return zcr
    
    def get_energy(self, audio):
        """Compute frame energy using Hamming window"""
        window = np.hamming(self.hop_length)
        energy = np.sqrt(
            np.convolve(audio**2, window, mode='same')
        )
        return energy
    
    def get_spectral_centroid(self, audio):
        """Compute spectral centroid (brightness)"""
        spec_centroid = librosa.feature.spectral_centroid(
            y=audio,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )[0]
        return spec_centroid
    
    def get_spectral_rolloff(self, audio):
        """Compute spectral rolloff (high-frequency energy)"""
        rolloff = librosa.feature.spectral_rolloff(
            y=audio,
            sr=self.sample_rate,
            n_fft=self.n_fft,
            hop_length=self.hop_length
        )[0]
        return rolloff
    
    def voice_activity_detection(self, audio, energy_threshold=0.02):
        """Advanced VAD: detect frames with voice activity"""
        energy = self.get_energy(audio)
        zcr = self.get_zero_crossing_rate(audio)
        spectral_cent = self.get_spectral_centroid(audio)
        
        # Normalize
        energy_norm = (energy - np.min(energy)) / (np.max(energy) - np.min(energy) + 1e-8)
        zcr_norm = (zcr - np.min(zcr)) / (np.max(zcr) - np.min(zcr) + 1e-8)
        spec_cent_norm = (spectral_cent - np.min(spectral_cent)) / (np.max(spectral_cent) - np.min(spectral_cent) + 1e-8)
        
        # Voice activity = combination of energy, ZCR, and spectral properties
        voice_activity = (
            (energy_norm > energy_threshold) & 
            (zcr_norm < 0.8) & 
            (spec_cent_norm > 0.2)
        )
        return voice_activity
    
    def extract_features(self, audio):
        """
        Extract complete feature set for speaker recognition
        Returns: dict with MFCC, deltas, spectral features, and statistics
        """
        # Remove silence
        audio_processed = self.remove_silence(audio)
        
        mfcc = self.extract_mfcc(audio_processed)
        spec = self.extract_spectrogram(audio_processed)
        
        # Delta and delta-delta features
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
        
        # Compute statistics
        mfcc_mean = np.mean(mfcc, axis=1)
        mfcc_std = np.std(mfcc, axis=1)
        mfcc_delta_mean = np.mean(mfcc_delta, axis=1)
        mfcc_delta2_mean = np.mean(mfcc_delta2, axis=1)
        
        # Spectral features
        spectral_cent = self.get_spectral_centroid(audio_processed)
        spectral_rolloff = self.get_spectral_rolloff(audio_processed)
        
        features = {
            'mfcc': mfcc,
            'mfcc_stats': np.concatenate([mfcc_mean, mfcc_std, mfcc_delta_mean, mfcc_delta2_mean]),
            'spec': spec,
            'mfcc_delta': mfcc_delta,
            'mfcc_delta2': mfcc_delta2,
            'spectral_centroid': spectral_cent,
            'spectral_rolloff': spectral_rolloff,
            'energy': self.get_energy(audio_processed),
            'zcr': self.get_zero_crossing_rate(audio_processed),
        }
        
        return features
    
    def pad_features(self, mfcc, target_length=50):
        """Pad or truncate MFCC to target time length"""
        if mfcc.shape[1] < target_length:
            # Pad with reflection
            pad_width = ((0, 0), (0, target_length - mfcc.shape[1]))
            mfcc = np.pad(mfcc, pad_width, mode='reflect')
        else:
            # Truncate from center
            start = (mfcc.shape[1] - target_length) // 2
            mfcc = mfcc[:, start:start + target_length]
        return mfcc
    
    def augment_audio(self, audio):
        """Data augmentation: pitch shifting and time stretching"""
        augmented_samples = []
        
        # Original
        augmented_samples.append(audio)
        
        # Pitch shift (+2 semitones)
        shifted_up = librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=2)
        augmented_samples.append(shifted_up)
        
        # Pitch shift (-2 semitones)
        shifted_down = librosa.effects.pitch_shift(audio, sr=self.sample_rate, n_steps=-2)
        augmented_samples.append(shifted_down)
        
        # Time stretch (slightly faster)
        stretched = librosa.effects.time_stretch(audio, rate=1.1)
        augmented_samples.append(stretched)
        
        return augmented_samples
