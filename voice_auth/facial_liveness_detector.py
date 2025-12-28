"""
Advanced Facial Liveness Detection
Detects blinks, head movement, eye gaze patterns, and other anti-spoofing techniques
"""

import numpy as np
import cv2
from pathlib import Path
from typing import Tuple, Dict


class FacialLivenessDetector:
    """
    Multi-factor facial liveness detection:
    - Blink detection
    - Head movement analysis
    - Eye gaze pattern analysis
    - Skin texture analysis
    - Infrared reflectance (if available)
    """
    
    def __init__(self):
        """Initialize facial liveness detector"""
        self.required_blinks = 2
        self.min_head_movement = 15  # degrees
        self.max_frame_history = 30
        self.frame_buffer = []
        self.previous_eye_aspect_ratio = None
        self.blink_count = 0
    
    def detect_blink(self, frame: np.ndarray) -> Tuple[bool, float]:
        """
        Detect eye blinks using eye aspect ratio
        Real blinks have characteristic temporal pattern
        """
        # Simplified blink detection using intensity changes
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        # Detect eye regions (simplified - in production use dlib/MediaPipe)
        height, width = gray.shape
        left_eye_region = gray[height//4:height//2, width//6:width//3]
        right_eye_region = gray[height//4:height//2, 2*width//3:5*width//6]
        
        # Calculate eye aspect ratio approximation
        left_eye_intensity = np.mean(left_eye_region)
        right_eye_intensity = np.mean(right_eye_region)
        avg_intensity = (left_eye_intensity + right_eye_intensity) / 2
        
        # Blink detected if sudden intensity drop (eyes close)
        blink_detected = False
        if self.previous_eye_aspect_ratio is not None:
            intensity_drop = self.previous_eye_aspect_ratio - avg_intensity
            if intensity_drop > 30:  # Threshold for blink
                blink_detected = True
                self.blink_count += 1
        
        self.previous_eye_aspect_ratio = avg_intensity
        return blink_detected, avg_intensity
    
    def detect_head_movement(self, frame: np.ndarray) -> Dict[str, float]:
        """
        Detect head rotation using facial landmarks
        Real faces show natural head movement; spoofed videos are rigid
        """
        # Detect face contours for head pose estimation
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        # Use Sobel operator to estimate head orientation
        sobel_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
        
        # Calculate orientation angles
        magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        angle = np.arctan2(sobel_y, sobel_x)
        
        # Average orientation vectors
        pitch = np.mean(angle) * 180 / np.pi
        roll = np.std(angle) * 10
        yaw = np.mean(magnitude) / (np.max(magnitude) + 1e-6) * 45
        
        return {
            "pitch": float(pitch),
            "roll": float(roll),
            "yaw": float(yaw),
            "total_movement": float(np.sqrt(pitch**2 + yaw**2))
        }
    
    def detect_eye_gaze(self, frame: np.ndarray) -> float:
        """
        Detect natural eye gaze patterns
        Spoofed videos have unrealistic or fixed gaze directions
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        # Detect bright spots (eye glints/reflections)
        _, bright_regions = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(bright_regions, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Count and analyze eye glint patterns
        glint_count = len(contours)
        glint_variance = np.var([cv2.contourArea(c) for c in contours]) if contours else 0
        
        # Natural gaze has 2 glints with reasonable variance
        gaze_naturalness = min(1.0, (glint_count / 2.0) * 0.5 + np.sqrt(glint_variance) / 255.0 * 0.5)
        return float(gaze_naturalness)
    
    def analyze_skin_texture(self, frame: np.ndarray) -> float:
        """
        Analyze skin texture to detect synthetic/printed faces
        Real skin has micro-texture; photos are smooth
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if len(frame.shape) == 3 else frame
        
        # Apply Laplacian filter to detect edge features
        laplacian = cv2.Laplacian(gray, cv2.CV_32F)
        texture_complexity = np.std(laplacian)
        
        # Detect periodic patterns (printed faces have regular patterns)
        fft = np.fft.fft2(gray)
        power_spectrum = np.abs(fft)**2
        
        # High entropy indicates natural texture
        texture_entropy = -np.sum(power_spectrum / np.sum(power_spectrum) * 
                                 np.log(power_spectrum / np.sum(power_spectrum) + 1e-10))
        
        # Combine metrics
        texture_score = min(1.0, (texture_complexity / 50.0) * 0.5 + (texture_entropy / 10.0) * 0.5)
        return float(texture_score)
    
    def analyze_liveness(self, frame_sequence: list) -> Dict[str, float]:
        """
        Comprehensive liveness analysis from frame sequence
        Combines multiple detection factors
        """
        if len(frame_sequence) < 5:
            return {"liveness_score": 0.0, "confidence": 0.0, "factors": {}}
        
        blink_scores = []
        head_movement_scores = []
        gaze_scores = []
        texture_scores = []
        
        for frame in frame_sequence:
            # Blink detection
            blink_detected, _ = self.detect_blink(frame)
            blink_scores.append(1.0 if blink_detected else 0.5)
            
            # Head movement
            head_movement = self.detect_head_movement(frame)
            movement_score = min(1.0, head_movement["total_movement"] / 45.0)
            head_movement_scores.append(movement_score)
            
            # Eye gaze
            gaze_score = self.detect_eye_gaze(frame)
            gaze_scores.append(gaze_score)
            
            # Skin texture
            texture_score = self.analyze_skin_texture(frame)
            texture_scores.append(texture_score)
        
        # Weighted combination
        final_liveness = (
            np.mean(blink_scores) * 0.25 +
            np.mean(head_movement_scores) * 0.25 +
            np.mean(gaze_scores) * 0.25 +
            np.mean(texture_scores) * 0.25
        )
        
        # Confidence based on consistency
        variance = np.var([blink_scores, head_movement_scores, gaze_scores, texture_scores])
        confidence = max(0.0, 1.0 - variance / 10.0)
        
        return {
            "liveness_score": float(np.clip(final_liveness, 0.0, 1.0)),
            "confidence": float(np.clip(confidence, 0.0, 1.0)),
            "factors": {
                "blink_detection": float(np.mean(blink_scores)),
                "head_movement": float(np.mean(head_movement_scores)),
                "eye_gaze": float(np.mean(gaze_scores)),
                "skin_texture": float(np.mean(texture_scores))
            }
        }
    
    def reset(self):
        """Reset detector state"""
        self.blink_count = 0
        self.previous_eye_aspect_ratio = None
        self.frame_buffer = []
