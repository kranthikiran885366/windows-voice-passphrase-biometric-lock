"""
Model Inference - Load pre-trained model and extract speaker embeddings
"""

import numpy as np
import tensorflow as tf
from pathlib import Path
from ai_models.speaker_model import create_speaker_recognition_model, create_embedding_extractor_model


class ModelInference:
    """Perform inference for speaker recognition"""
    
    def __init__(self, model_path=None):
        # Prefer new Keras format, fallback to .h5 if needed
        keras_path = Path("ai_models/models/speaker_recognition.keras")
        h5_path = Path("ai_models/models/speaker_recognition.h5")
        if model_path:
            self.model_path = Path(model_path)
        elif keras_path.exists():
            self.model_path = keras_path
        else:
            self.model_path = h5_path
        self.full_model = None
        self.embedding_model = None
        self.model = None  # Ensure self.model is always defined
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained model or create new one"""
        if self.model_path.exists():
            try:
                self.full_model = tf.keras.models.load_model(self.model_path)
                # Ensure model is built by calling it with dummy data
                dummy_input = np.zeros((1, 13, 50, 1), dtype=np.float32)
                self.full_model(dummy_input)
                self.embedding_model = create_embedding_extractor_model(self.full_model)
                self.model = self.full_model  # Ensure self.model is set after loading
                print(f"✓ Model loaded from {self.model_path}")
            except Exception as e:
                print(f"Failed to load model: {e}. Creating new model...")
                self._create_default_model()
        else:
            self._create_default_model()
    
    def _create_default_model(self):
        """Create default model if none exists"""
        self.full_model = create_speaker_recognition_model(
            input_shape=(13, 50),
            num_speakers=1
        )
        self.embedding_model = create_embedding_extractor_model(self.full_model)
        self.model = self.full_model  # Ensure self.model is set after creating default
        # Compile
        self.full_model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        print("✓ Default model created")
    
    def extract_embedding(self, mfcc_features):
        """
        Extract 512-dimensional speaker embedding from MFCC features
        
        Args:
            mfcc_features: (n_mfcc, time_steps) array
        
        Returns:
            embedding: (512,) array
        """
        try:
            # Add batch and channel dimensions: (1, 13, 50, 1)
            mfcc_input = np.expand_dims(np.expand_dims(mfcc_features, 0), -1)
            
            # Extract embedding
            embedding = self.embedding_model.predict(mfcc_input, verbose=0)
            return embedding[0]  # Return first (only) sample
        
        except Exception as e:
            print(f"Error extracting embedding: {e}")
            return None
    
    def predict_speaker(self, mfcc_features):
        """Predict speaker class and confidence"""
        try:
            mfcc_input = np.expand_dims(np.expand_dims(mfcc_features, 0), -1)
            predictions = self.full_model.predict(mfcc_input, verbose=0)
            confidence = np.max(predictions[0])
            predicted_class = np.argmax(predictions[0])
            return predicted_class, confidence
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None, 0.0
    
    def save_model(self, save_path=None):
        """Save trained model"""
        path = save_path or self.model_path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.full_model.save(path)
        print(f"✓ Model saved to {path}")
