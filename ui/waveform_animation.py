"""
Advanced Animated Waveform - Real-time frequency band visualization
Shows 40 frequency bands with smooth animations and gradient colors
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QLinearGradient
import math
import numpy as np


class WaveformWidget(QWidget):
    """Enhanced with smooth animations and gradient coloring"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_recording = False
        self.audio_levels = [0.1] * 40  # 40 frequency bands
        self.smoothed_levels = [0.1] * 40  # Smoothed for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.time = 0
        self.peak_levels = [0.1] * 40  # For peak hold effect
        
        self.setMinimumHeight(180)
    
    def start_animation(self):
        """Start waveform animation during recording"""
        self.is_recording = True
        self.timer.start(33)  # ~30 FPS
    
    def stop_animation(self):
        """Stop waveform animation"""
        self.is_recording = False
        self.timer.stop()
        self.audio_levels = [0.1] * 40
        self.smoothed_levels = [0.1] * 40
        self.peak_levels = [0.1] * 40
        self.update()
    
    def set_audio_levels(self, levels):
        """Update audio levels for visualization (0-1 range)"""
        if len(levels) != len(self.audio_levels):
            levels = np.interp(
                np.linspace(0, len(levels)-1, len(self.audio_levels)),
                np.arange(len(levels)),
                levels
            )
        self.audio_levels = np.clip(levels, 0, 1).tolist()
    
    def update_animation(self):
        """Update animation frame with smooth transitions"""
        if self.is_recording:
            # Simulate realistic audio with pink noise characteristics
            for i in range(len(self.audio_levels)):
                # Decay from peak
                self.peak_levels[i] = max(self.audio_levels[i], self.peak_levels[i] * 0.95)
                
                # Smooth transitions
                target = self.audio_levels[i]
                self.smoothed_levels[i] = (
                    0.7 * self.smoothed_levels[i] + 0.3 * target
                )
                
                # Add realistic variation
                if self.is_recording:
                    variation = np.sin(self.time * 0.05 + i * 0.2) * 0.1
                    self.smoothed_levels[i] += variation
            
            self.time += 1
        self.update()
    
    def paintEvent(self, event):
        """Paint animated waveform with gradient colors"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_y = height / 2
        
        # Draw background
        painter.fillRect(self.rect(), QColor('#0a0e27'))
        
        # Draw frequency bands
        bar_width = width / len(self.smoothed_levels)
        
        for i, level in enumerate(self.smoothed_levels):
            x = i * bar_width
            
            # Clamp level
            display_level = np.clip(level, 0, 1)
            bar_height = max(0.1, display_level) * (height / 2 - 10)
            
            # Low frequencies (left) = cyan, Mid = purple, High = red
            hue_factor = i / len(self.smoothed_levels)  # 0 (left) to 1 (right)
            intensity = display_level
            
            if intensity > 0.7:
                # Red zone (high energy)
                color = QColor(
                    int(255 * intensity),
                    int(51 * (1-intensity)),
                    int(51 * (1-intensity))
                )
            elif intensity > 0.4:
                # Purple zone (medium energy)
                r = int(124 + 131 * (intensity - 0.4) / 0.3)
                g = int(58 + (intensity - 0.4) / 0.3 * 50)
                b = int(237 - 50 * (intensity - 0.4) / 0.3)
                color = QColor(r, g, b)
            else:
                # Cyan zone (low energy)
                color = QColor(0, int(217 * intensity / 0.4), int(255 * intensity / 0.4))
            
            # Draw bar with gradient
            painter.fillRect(
                x + 1, center_y - bar_height,
                bar_width - 2, bar_height * 2,
                color
            )
            
            # Draw peak indicator
            peak_height = self.peak_levels[i] * (height / 2 - 10)
            peak_color = QColor(100, 100, 100, 100)
            painter.fillRect(
                x + 1, center_y - peak_height,
                bar_width - 2, 2,
                peak_color
            )
        
        # Draw center line
        pen = QPen(QColor('#7c3aed'), 1)
        pen.setDashPattern([5, 5])
        painter.setPen(pen)
        painter.drawLine(0, center_y, width, center_y)
