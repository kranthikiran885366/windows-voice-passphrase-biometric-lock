"""
Advanced Facial Recognition with Deep Learning
Uses CNN for face embedding extraction and liveness detection
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path
import json


class FaceRecognitionModel:
    """
    CNN-based face recognition with liveness detection
    Extracts 128-D face embeddings using deep neural network
    """
    
    def __init__(self, embedding_dim: int = 128, model_path: str = None):
        """Initialize face recognition model"""
        self.embedding_dim = embedding_dim
        self.model = None
        self.liveness_model = None
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            self._build_architecture()
    
    def _build_architecture(self):
        """Build advanced CNN architecture for face recognition"""
        # Base feature extraction (ResNet-like blocks)
        inputs = keras.Input(shape=(224, 224, 3), name="face_input")
        
        # Conv Block 1: 224 -> 112
        x = layers.Conv2D(64, 7, strides=2, padding="same")(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)
        
        # Residual Block 2: 112 -> 56
        for _ in range(2):
            x = self._residual_block(x, 64)
        x = layers.MaxPooling2D(2, strides=2)(x)
        
        # Residual Block 3: 56 -> 28
        for _ in range(2):
            x = self._residual_block(x, 128)
        x = layers.MaxPooling2D(2, strides=2)(x)
        
        # Residual Block 4: 28 -> 14
        for _ in range(2):
            x = self._residual_block(x, 256)
        x = layers.MaxPooling2D(2, strides=2)(x)
        
        # Global Average Pooling
        x = layers.GlobalAveragePooling2D()(x)
        
        # Dense layers for embedding
        x = layers.Dense(512, activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        
        x = layers.Dense(256, activation="relu")(x)
        x = layers.BatchNormalization()(x)
        
        # L2 normalized embedding
        embeddings = layers.Dense(self.embedding_dim, name="embeddings")(x)
        embeddings = layers.Lambda(
            lambda x: tf.nn.l2_normalize(x, axis=1),
            name="embedding_normalization"
        )(embeddings)
        
        self.model = keras.Model(inputs=inputs, outputs=embeddings)
        
        # Build liveness detection head
        self._build_liveness_model()
    
    def _residual_block(self, x, filters: int):
        """Residual block for feature extraction"""
        shortcut = x
        
        x = layers.Conv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        
        x = layers.Conv2D(filters, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        # Channel-wise attention
        channel_attention = layers.GlobalAveragePooling2D(keepdims=True)(x)
        channel_attention = layers.Dense(filters // 16, activation="relu")(channel_attention)
        channel_attention = layers.Dense(filters, activation="sigmoid")(channel_attention)
        x = layers.Multiply()([x, channel_attention])
        
        if shortcut.shape[-1] != filters:
            shortcut = layers.Conv2D(filters, 1, padding="same")(shortcut)
        
        x = layers.Add()([x, shortcut])
        x = layers.ReLU()(x)
        return x
    
    def _build_liveness_model(self):
        """Build liveness detection sub-model"""
        inputs = keras.Input(shape=(224, 224, 3))
        
        # Lightweight liveness detection network
        x = layers.Conv2D(32, 5, padding="same", activation="relu")(inputs)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Conv2D(64, 5, padding="same", activation="relu")(x)
        x = layers.MaxPooling2D(2)(x)
        x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
        x = layers.MaxPooling2D(2)(x)
        
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(256, activation="relu")(x)
        x = layers.Dropout(0.3)(x)
        liveness_score = layers.Dense(1, activation="sigmoid", name="liveness")(x)
        
        self.liveness_model = keras.Model(inputs=inputs, outputs=liveness_score)
    
    def extract_embedding(self, face_image: np.ndarray) -> np.ndarray:
        """Extract 128-D embedding from face image"""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        # Preprocess image
        face_image = self._preprocess_face(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        
        # Extract embedding
        embedding = self.model.predict(face_image, verbose=0)
        return embedding[0]
    
    def detect_liveness(self, face_image: np.ndarray) -> float:
        """Detect if face is alive (1.0) or spoofed (0.0)"""
        if self.liveness_model is None:
            raise ValueError("Liveness model not initialized")
        
        face_image = self._preprocess_face(face_image)
        face_image = np.expand_dims(face_image, axis=0)
        
        liveness_score = self.liveness_model.predict(face_image, verbose=0)[0][0]
        return float(liveness_score)
    
    def _preprocess_face(self, image: np.ndarray) -> np.ndarray:
        """Preprocess face image to 224x224"""
        if image.shape != (224, 224, 3):
            import cv2
            image = cv2.resize(image, (224, 224))
        
        # Normalize to [-1, 1]
        image = image.astype(np.float32) / 127.5 - 1.0
        return image
    
    def save_model(self, model_path: str):
        """Save model to disk"""
        if self.model:
            self.model.save(f"{model_path}/face_embedding_model.h5")
        if self.liveness_model:
            self.liveness_model.save(f"{model_path}/face_liveness_model.h5")
    
    def load_model(self, model_path: str):
        """Load model from disk"""
        model_file = Path(model_path) / "face_embedding_model.h5"
        liveness_file = Path(model_path) / "face_liveness_model.h5"
        
        if model_file.exists():
            self.model = keras.models.load_model(str(model_file))
        if liveness_file.exists():
            self.liveness_model = keras.models.load_model(str(liveness_file))
