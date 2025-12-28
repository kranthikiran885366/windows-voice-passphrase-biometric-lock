"""
Speaker Recognition Model Architecture
CNN+LSTM for speaker identification from voice spectrograms
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


def create_speaker_recognition_model(input_shape=(13, 50), num_speakers=1):
    """
    Create CNN+LSTM model for speaker recognition
    
    Args:
        input_shape: (n_mfcc, time_steps) = (13, 50)
        num_speakers: number of speakers (1 for binary auth, >1 for multi-speaker)
    
    Returns:
        Keras model
    """
    
    model = keras.Sequential([
        # Input: (batch, 13, 50, 1)
        layers.Input(shape=input_shape + (1,)),
        # CNN Blocks for spectro-temporal feature extraction
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        # Reshape for LSTM
        layers.Reshape((-1, 128)),  # (batch, time, features)
        # LSTM for temporal dynamics
        layers.LSTM(256, return_sequences=True),
        layers.Dropout(0.3),
        layers.LSTM(128),
        layers.Dropout(0.3),
        # Speaker embedding (512-dim vector)
        layers.Dense(512, activation='relu', name='speaker_embedding'),
        layers.BatchNormalization(),
        # Classification head
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_speakers + 1, activation='softmax', name='speaker_classification')
    ])
    # Build model by calling it once with dummy input
    import numpy as np
    dummy_input = np.zeros((1,) + input_shape + (1,), dtype=np.float32)
    model(dummy_input)
    return model


def create_embedding_extractor_model(full_model):
    """
    Create model that extracts speaker embeddings (last hidden layer)
    """
    embedding_layer = keras.Model(
        inputs=full_model.input,
        outputs=full_model.get_layer('speaker_embedding').output
    )
    return embedding_layer


def create_triplet_loss_model(input_shape=(13, 50)):
    """
    Create model using Triplet Loss for speaker recognition
    Better for open-set speaker identification
    """
    
    def build_encoder():
        encoder = keras.Sequential([
            layers.Input(shape=input_shape + (1,)),
            layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.Dense(128, activation='relu'),
            layers.Dense(64),  # Embedding without activation
            layers.Lambda(lambda x: tf.math.l2_normalize(x, axis=1))
        ])
        return encoder
    
    # Anchor, positive, negative inputs
    anchor_input = keras.Input(shape=input_shape + (1,))
    positive_input = keras.Input(shape=input_shape + (1,))
    negative_input = keras.Input(shape=input_shape + (1,))
    
    encoder = build_encoder()
    
    anchor_embedding = encoder(anchor_input)
    positive_embedding = encoder(positive_input)
    negative_embedding = encoder(negative_input)
    
    output = keras.layers.concatenate([
        anchor_embedding,
        positive_embedding,
        negative_embedding
    ])
    
    model = keras.Model(
        inputs=[anchor_input, positive_input, negative_input],
        outputs=output,
        name='triplet_loss_model'
    )
    
    return model, encoder
