"""
Advanced Liveness Detection - Prevents Voice Spoofing Attacks
Multi-factor analysis: F0 contour, spectral dynamics, echo detection, noise variability
"""

import numpy as np
from scipy import signal
import librosa


class LivenessDetector:
    """Advanced liveness detection with 5+ anti-spoofing factors"""
    
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.hop_length = 512
        
    def extract_f0_contour(self, audio):
        """Extract fundamental frequency using PYIN algorithm"""
        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio,
            fmin=librosa.note_to_hz('C2'),  # 65 Hz
            fmax=librosa.note_to_hz('C7'),  # 2093 Hz
            hop_length=self.hop_length,
            trough_threshold=0.1
        )
        return f0, voiced_flag, voiced_probs
    
    def compute_f0_statistics(self, f0, voiced_flag):
        """Compute F0 statistics for liveness scoring"""
        voiced_f0 = f0[voiced_flag]
        
        if len(voiced_f0) < 10:
            return None
        
        # Remove outliers
        q1, q3 = np.percentile(voiced_f0, [25, 75])
        iqr = q3 - q1
        voiced_f0_filtered = voiced_f0[(voiced_f0 >= q1 - 1.5*iqr) & (voiced_f0 <= q3 + 1.5*iqr)]
        
        stats = {
            'mean_f0': np.nanmean(voiced_f0_filtered),
            'std_f0': np.nanstd(voiced_f0_filtered),
            'min_f0': np.nanmin(voiced_f0_filtered),
            'max_f0': np.nanmax(voiced_f0_filtered),
            'f0_range': np.nanmax(voiced_f0_filtered) - np.nanmin(voiced_f0_filtered),
            'voiced_ratio': np.sum(voiced_flag) / len(voiced_flag),
            'f0_vibrato': self._detect_vibrato(voiced_f0_filtered),
        }
        return stats
    
    def _detect_vibrato(self, f0):
        """Detect natural vibrato in voice (sign of real voice)"""
        # Compute F0 trajectory smoothness
        f0_diff = np.diff(f0)
        vibrato_strength = np.std(f0_diff) / (np.mean(np.abs(f0_diff)) + 1e-8)
        return min(vibrato_strength, 1.0)
    
    def spectral_centroid_variation(self, audio):
        """Compute variation in spectral centroid (timbral dynamics)"""
        spec_centroid = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
        
        # High variation = real speech (natural timbral changes)
        variation = np.std(spec_centroid) / (np.mean(spec_centroid) + 1e-8)
        return min(variation, 2.0)
    
    def spectral_contrast_analysis(self, audio):
        """Analyze spectral contrast (peak-to-valley ratio in spectrum)"""
        contrast = librosa.feature.spectral_contrast(y=audio, sr=self.sample_rate)
        # Real speech has natural spectral variation
        mean_contrast = np.mean(contrast)
        return min(mean_contrast / 10, 1.0)  # Normalize
    
    def check_echo_patterns(self, audio):
        """Detect echo/reverb patterns indicative of recorded playback"""
        # Compute autocorrelation
        autocorr = np.correlate(audio, audio, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr /= (autocorr[0] + 1e-8)
        
        # Detect suspicious periodic peaks (characteristic of playback through speakers)
        peaks, properties = signal.find_peaks(autocorr[100:600], height=0.4, distance=50)
        
        if len(peaks) > 0:
            peak_heights = properties.get('peak_height', [])
            echo_score = np.mean(peak_heights) if len(peak_heights) > 0 else 0
        else:
            echo_score = 0
        
        echo_score = min(echo_score, 1.0)
        return echo_score
    
    def detect_background_noise_consistency(self, audio, frame_length=2048):
        """Real speech has varying background; playback is very consistent"""
        frames = librosa.util.frame(audio, frame_length, frame_length // 2)
        frame_energy = np.sqrt(np.sum(frames**2, axis=0))
        
        # Higher variability in background = real speech
        energy_variation = np.std(frame_energy) / (np.mean(frame_energy) + 1e-8)
        noise_liveness = min(energy_variation, 1.0)
        
        return noise_liveness
    
    def detect_clipping(self, audio, threshold=0.99):
        """Detect clipping artifacts (sign of over-amplified recording)"""
        clipping_ratio = np.sum(np.abs(audio) > threshold) / len(audio)
        # Lower clipping = more likely real
        clipping_liveness = 1.0 - min(clipping_ratio * 10, 1.0)
        return clipping_liveness
    
    def spectral_flatness_analysis(self, audio):
        """Analyze spectral flatness (entropy)"""
        spec = np.abs(librosa.stft(audio))
        flatness = librosa.feature.spectral_flatness(S=spec)
        mean_flatness = np.mean(flatness)
        # Real speech has moderate flatness (not too flat, not too peaky)
        flatness_liveness = 1.0 - abs(mean_flatness - 0.3)
        return max(min(flatness_liveness, 1.0), 0.0)
    
    def compute_liveness_score(self, audio):
        """
        Compute comprehensive liveness score (0-1, higher = more likely real)
        
        Multi-factor analysis:
        - F0 contour & vibrato variation
        - Spectral dynamics & contrast
        - Echo detection
        - Background noise variability
        - Clipping detection
        - Spectral entropy
        """
        try:
            if len(audio) < self.sample_rate:  # Less than 1 second
                return 0.2
            
            f0, voiced_flag, voiced_probs = self.extract_f0_contour(audio)
            f0_stats = self.compute_f0_statistics(f0, voiced_flag)
            
            if f0_stats is None:
                return 0.3  # Not enough voiced content
            
            # Factor 1: F0 contour variation (natural speakers have range + vibrato)
            f0_variation = min(f0_stats['f0_range'] / 150, 1.0)  # Max ~150Hz
            vibrato = f0_stats['f0_vibrato']
            f0_score = 0.6 * f0_variation + 0.4 * vibrato
            
            # Factor 2: Spectral dynamics
            spec_variation = self.spectral_centroid_variation(audio)
            spec_contrast = self.spectral_contrast_analysis(audio)
            spectral_score = 0.5 * min(spec_variation, 1.0) + 0.5 * spec_contrast
            
            # Factor 3: Echo detection (lower is better for liveness)
            echo_score = self.check_echo_patterns(audio)
            echo_liveness = 1.0 - echo_score
            
            # Factor 4: Background noise variability
            noise_liveness = self.detect_background_noise_consistency(audio)
            
            # Factor 5: Clipping artifacts
            clipping_liveness = self.detect_clipping(audio)
            
            # Factor 6: Spectral flatness
            flatness_liveness = self.spectral_flatness_analysis(audio)
            
            # Weighted combination (emphasize F0 and spectral for voice)
            liveness = (
                0.30 * f0_score +           # F0 is most discriminative
                0.25 * spectral_score +     # Spectral dynamics important
                0.20 * echo_liveness +      # Echo detection
                0.10 * noise_liveness +     # Background variation
                0.10 * clipping_liveness +  # Clipping artifacts
                0.05 * flatness_liveness    # Spectral flatness
            )
            
            return np.clip(liveness, 0, 1)
        
        except Exception as e:
            print(f"[v0] Liveness detection error: {e}")
            return 0.5  # Neutral score on error
