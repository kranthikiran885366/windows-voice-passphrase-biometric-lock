"""
Advanced Iris Recognition using Deep Learning
Extracts unique iris pattern embeddings for biometric authentication
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path


class IrisRecognitionModel:
    """
    CNN-based iris recognition with 256-D embeddings
    Uses specialized segmentation for iris region extraction
    """
    
    def __init__(self, embedding_dim: int = 256, model_path: str = None):
        """Initialize iris recognition model"""
        self.embedding_dim = embedding_dim
        self.model = None
        self.segmentation_model = None
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        else:
            self._build_architecture()
    
    def _build_architecture(self):
        """Build advanced iris recognition CNN"""
        inputs = keras.Input(shape=(64, 512, 1), name="iris_input")
        
        # Iris-specific feature extraction
        x = layers.Conv2D(32, 3, padding="same", activation="relu")(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(2)(x)
        
        x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(2)(x)
        
        # Multi-scale feature fusion
        x1 = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
        x2 = layers.Conv2D(128, 5, padding="same", activation="relu")(x)
        x = layers.Concatenate()([x1, x2])
        x = layers.BatchNormalization()(x)
        x = layers.MaxPooling2D(2)(x)
        
        x = layers.Conv2D(256, 3, padding="same", activation="relu")(x)
        x = layers.BatchNormalization()(x)
        
        # Global context
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(512, activation="relu")(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.4)(x)
        
        # Iris embedding
        embeddings = layers.Dense(self.embedding_dim, name="iris_embedding")(x)
        embeddings = layers.Lambda(
            lambda x: tf.nn.l2_normalize(x, axis=1),
            name="iris_normalization"
        )(embeddings)
        
        self.model = keras.Model(inputs=inputs, outputs=embeddings)
        self._build_segmentation_model()
    
    def _build_segmentation_model(self):
        """Build iris segmentation model"""
        inputs = keras.Input(shape=(64, 512, 1))
        
        # Encoder
        enc1 = layers.Conv2D(16, 3, padding="same", activation="relu")(inputs)
        enc1 = layers.MaxPooling2D(2)(enc1)
        
        enc2 = layers.Conv2D(32, 3, padding="same", activation="relu")(enc1)
        enc2 = layers.MaxPooling2D(2)(enc2)
        
        # Decoder
        dec1 = layers.UpSampling2D(2)(enc2)
        dec1 = layers.Conv2D(16, 3, padding="same", activation="relu")(dec1)
        
        dec2 = layers.UpSampling2D(2)(dec1)
        dec2 = layers.Conv2D(1, 1, padding="same", activation="sigmoid")(dec2)
        
        self.segmentation_model = keras.Model(inputs=inputs, outputs=dec2)
    
    def extract_embedding(self, iris_image: np.ndarray) -> np.ndarray:
        """Extract 256-D iris embedding"""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        iris_image = self._preprocess_iris(iris_image)
        iris_image = np.expand_dims(iris_image, axis=0)
        
        embedding = self.model.predict(iris_image, verbose=0)
        return embedding[0]
    
    def segment_iris(self, image: np.ndarray) -> np.ndarray:
        """Segment iris region from eye image"""
        if self.segmentation_model is None:
            raise ValueError("Segmentation model not initialized")
        
        image = self._preprocess_iris(image)
        image = np.expand_dims(image, axis=0)
        
        mask = self.segmentation_model.predict(image, verbose=0)[0]
        return np.squeeze(mask)
    
    def _preprocess_iris(self, image: np.ndarray) -> np.ndarray:
        """Preprocess iris image to 64x512 (unwrapped iris)"""
        if image.shape != (64, 512, 1):
            if len(image.shape) == 2:
                image = np.expand_dims(image, axis=-1)
            
            import cv2
            image = cv2.resize(image, (512, 64))
        
        image = image.astype(np.float32) / 255.0
        return image
    
    def save_model(self, model_path: str):
        """Save models to disk"""
        if self.model:
            self.model.save(f"{model_path}/iris_embedding_model.h5")
        if self.segmentation_model:
            self.segmentation_model.save(f"{model_path}/iris_segmentation_model.h5")
    
    def load_model(self, model_path: str):
        """Load models from disk"""
        model_file = Path(model_path) / "iris_embedding_model.h5"
        seg_file = Path(model_path) / "iris_segmentation_model.h5"
        
        if model_file.exists():
            self.model = keras.models.load_model(str(model_file))
        if seg_file.exists():
            self.segmentation_model = keras.models.load_model(str(seg_file))
