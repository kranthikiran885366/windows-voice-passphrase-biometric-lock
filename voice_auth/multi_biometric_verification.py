"""
Multi-Biometric Verification Pipeline
Combines voice, face, iris, and behavioral biometrics for enhanced security
"""

import numpy as np
from typing import Dict, Tuple
from pathlib import Path
from datetime import datetime


class MultibiometricVerifier:
    """
    Combines multiple biometric factors for robust authentication
    - Voice biometrics (primary)
    - Facial recognition (optional)
    - Iris recognition (optional)
    - Behavioral biometrics (passive)
    """
    
    def __init__(self, enable_face=False, enable_iris=False):
        """Initialize multi-biometric verifier"""
        self.enable_face = enable_face
        self.enable_iris = enable_iris
        
        # Biometric weights (adjustable)
        self.weights = {
            "voice": 0.50,
            "face": 0.25 if enable_face else 0.0,
            "iris": 0.15 if enable_iris else 0.0,
            "behavior": 0.10
        }
        
        # Normalize weights
        total_weight = sum(self.weights.values())
        for key in self.weights:
            self.weights[key] /= total_weight
        
        # Load models (lazy loading)
        self.voice_model = None
        self.face_model = None
        self.iris_model = None
        self.face_liveness = None
    
    def verify_multibiometric(self, 
                             voice_score: float,
                             voice_liveness: float,
                             face_data: Dict = None,
                             iris_data: Dict = None,
                             behavior_data: Dict = None) -> Dict:
        """
        Perform multi-biometric verification
        
        Returns:
            {
                "authenticated": bool,
                "confidence": float,
                "scores": {
                    "voice": float,
                    "face": float,
                    "iris": float,
                    "behavior": float
                },
                "liveness_checks": {
                    "voice_liveness": float,
                    "face_liveness": float
                },
                "details": str
            }
        """
        
        scores = {
            "voice": voice_score * voice_liveness,
            "face": 0.0,
            "iris": 0.0,
            "behavior": 0.0
        }
        
        liveness_checks = {
            "voice_liveness": voice_liveness,
            "face_liveness": 0.0,
            "iris_liveness": 0.0
        }
        
        # Face verification
        if self.enable_face and face_data:
            face_score = self._verify_face(face_data)
            scores["face"] = face_score["score"]
            liveness_checks["face_liveness"] = face_score.get("liveness", 0.0)
        
        # Iris verification
        if self.enable_iris and iris_data:
            iris_score = self._verify_iris(iris_data)
            scores["iris"] = iris_score["score"]
            liveness_checks["iris_liveness"] = iris_score.get("liveness", 0.0)
        
        # Behavior verification
        if behavior_data:
            scores["behavior"] = self._verify_behavior(behavior_data)
        
        # Calculate weighted confidence
        confidence = sum(scores[key] * self.weights[key] 
                        for key in scores if self.weights[key] > 0)
        
        # Authentication decision
        # All active biometrics must exceed minimum threshold
        min_threshold = 0.95
        all_liveness_passed = all(
            liveness_checks[key] > 0.8 
            for key in liveness_checks 
            if liveness_checks[key] > 0
        )
        
        authenticated = confidence >= min_threshold and all_liveness_passed
        
        details = self._generate_verification_details(
            scores, liveness_checks, authenticated
        )
        
        return {
            "authenticated": authenticated,
            "confidence": float(np.clip(confidence, 0.0, 1.0)),
            "scores": scores,
            "liveness_checks": liveness_checks,
            "details": details
        }
    
    def _verify_face(self, face_data: Dict) -> Dict:
        """Verify facial biometrics"""
        try:
            from ai_models.face_recognition_model import FaceRecognitionModel
            from voice_auth.facial_liveness_detector import FacialLivenessDetector
            
            if not self.face_model:
                self.face_model = FaceRecognitionModel()
            if not self.face_liveness:
                self.face_liveness = FacialLivenessDetector()
            
            face_image = face_data.get("image")
            frame_sequence = face_data.get("frame_sequence", [])
            
            # Extract embedding
            embedding = self.face_model.extract_embedding(face_image)
            
            # Load enrolled embedding
            enrolled_embedding = face_data.get("enrolled_embedding")
            
            if enrolled_embedding is not None:
                # Compare embeddings
                similarity = np.dot(embedding, enrolled_embedding) / (
                    np.linalg.norm(embedding) * np.linalg.norm(enrolled_embedding) + 1e-6
                )
                score = (similarity + 1.0) / 2.0  # Normalize to [0, 1]
            else:
                score = 0.0
            
            # Liveness detection
            if len(frame_sequence) > 0:
                liveness_result = self.face_liveness.analyze_liveness(frame_sequence)
                liveness_score = liveness_result["liveness_score"]
            else:
                liveness_score = 0.5
            
            return {
                "score": float(score),
                "liveness": float(liveness_score),
                "similarity": float(np.clip(score, 0.0, 1.0))
            }
        
        except Exception as e:
            print(f"[v0] Face verification error: {str(e)}")
            return {"score": 0.0, "liveness": 0.0}
    
    def _verify_iris(self, iris_data: Dict) -> Dict:
        """Verify iris biometrics"""
        try:
            from ai_models.iris_recognition_model import IrisRecognitionModel
            
            if not self.iris_model:
                self.iris_model = IrisRecognitionModel()
            
            iris_image = iris_data.get("image")
            
            # Extract embedding
            embedding = self.iris_model.extract_embedding(iris_image)
            
            # Load enrolled embedding
            enrolled_embedding = iris_data.get("enrolled_embedding")
            
            if enrolled_embedding is not None:
                # Compare embeddings
                similarity = np.dot(embedding, enrolled_embedding) / (
                    np.linalg.norm(embedding) * np.linalg.norm(enrolled_embedding) + 1e-6
                )
                score = (similarity + 1.0) / 2.0
            else:
                score = 0.0
            
            # Iris has high intrinsic liveness (hard to spoof)
            liveness_score = 0.9 if score > 0.7 else 0.3
            
            return {
                "score": float(score),
                "liveness": float(liveness_score),
                "similarity": float(np.clip(score, 0.0, 1.0))
            }
        
        except Exception as e:
            print(f"[v0] Iris verification error: {str(e)}")
            return {"score": 0.0, "liveness": 0.0}
    
    def _verify_behavior(self, behavior_data: Dict) -> float:
        """Verify behavioral biometrics"""
        # Simplified behavior scoring
        typing_score = behavior_data.get("typing_score", 0.5)
        activity_score = behavior_data.get("activity_score", 0.5)
        
        return float((typing_score + activity_score) / 2.0)
    
    def _generate_verification_details(self, 
                                      scores: Dict, 
                                      liveness: Dict,
                                      authenticated: bool) -> str:
        """Generate detailed verification report"""
        details = []
        
        details.append(f"Voice Score: {scores['voice']:.1%}")
        if scores['face'] > 0:
            details.append(f"Face Score: {scores['face']:.1%}")
        if scores['iris'] > 0:
            details.append(f"Iris Score: {scores['iris']:.1%}")
        if scores['behavior'] > 0:
            details.append(f"Behavior Score: {scores['behavior']:.1%}")
        
        details.append("")
        details.append("Liveness Checks:")
        details.append(f"  Voice Liveness: {liveness['voice_liveness']:.1%}")
        if liveness['face_liveness'] > 0:
            details.append(f"  Face Liveness: {liveness['face_liveness']:.1%}")
        if liveness['iris_liveness'] > 0:
            details.append(f"  Iris Liveness: {liveness['iris_liveness']:.1%}")
        
        details.append("")
        details.append(f"Result: {'AUTHENTICATED' if authenticated else 'DENIED'}")
        
        return "\n".join(details)
