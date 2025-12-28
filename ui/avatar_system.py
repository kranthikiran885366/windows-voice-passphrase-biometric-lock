"""
3D Animated Avatar System for Security
Provides cinematic feedback during authentication
Uses OpenGL-based 3D rendering
"""

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtOpenGL import QGLWidget
import math


class Avatar3DWidget(QGLWidget):
    """
    3D OpenGL-based avatar for authentication feedback
    Shows emotional states: neutral, listening, analyzing, approved, denied, locked
    """
    
    authentication_status_changed = pyqtSignal(str)  # "neutral", "listening", "analyzing", "approved", "denied", "locked"
    
    def __init__(self, parent=None):
        """Initialize 3D avatar widget"""
        from PyQt5.QtOpenGL import QGLFormat
        fmt = QGLFormat()
        fmt.setVersion(2, 1)
        fmt.setProfile(QGLFormat.CoreProfile)
        super().__init__(fmt, parent)
        # Avatar state
        self.state = "neutral"
        self.animation_time = 0
        self.animation_speed = 0.05
        # Rotation angles (head movement)
        self.head_rotation_x = 0
        self.head_rotation_y = 0
        self.head_rotation_z = 0
        # Eye parameters
        self.left_eye_blink = 0  # 0 to 1
        self.right_eye_blink = 0
        self.eye_rotation_x = 0
        self.eye_rotation_y = 0
        # Color state
        self.state_color = [0.0, 1.0, 1.0]  # Cyan default
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update)
        self.animation_timer.start(16)  # 60 FPS
    
    def initializeGL(self):
        """Initialize OpenGL settings"""
        try:
            from OpenGL.GL import glClearColor, glEnable, glDepthFunc, GL_DEPTH_TEST, GL_LESS
            glClearColor(0.05, 0.05, 0.15, 1.0)  # Dark background
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
        except ImportError:
            pass
    
    def resizeGL(self, w: int, h: int):
        """Handle window resize"""
        try:
            from OpenGL.GL import glViewport
            glViewport(0, 0, w, h)
        except ImportError:
            pass
    
    def paintGL(self):
        """Render the avatar"""
        try:
            from OpenGL.GL import (
                glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
                glMatrixMode, GL_PROJECTION, GL_MODELVIEW,
                glLoadIdentity, glTranslatef, glRotatef, glColor3f,
                gluPerspective
            )
            from OpenGL.GLU import gluPerspective
            
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Setup projection
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, self.width() / max(1, self.height()), 0.1, 100)
            
            # Setup view
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -3)
            
            # Update animation
            self._update_animation()
            
            # Draw avatar based on state
            if self.state == "listening":
                self._draw_listening_avatar()
            elif self.state == "analyzing":
                self._draw_analyzing_avatar()
            elif self.state == "approved":
                self._draw_approved_avatar()
            elif self.state == "denied":
                self._draw_denied_avatar()
            elif self.state == "locked":
                self._draw_locked_avatar()
            else:
                self._draw_neutral_avatar()
        
        except ImportError:
            # Fallback: render 2D representation
            self._draw_2d_fallback()
    
    def _update_animation(self):
        """Update animation time and state"""
        self.animation_time += self.animation_speed
        if self.animation_time > 2 * math.pi:
            self.animation_time = 0
    
    def _draw_neutral_avatar(self):
        """Draw neutral avatar state (at rest)"""
        try:
            from OpenGL.GL import glRotatef, glColor3f, glBegin, glEnd, GL_TRIANGLES, glVertex3f
            
            # Slight idle animation
            idle_rotation = 5 * math.sin(self.animation_time)
            glRotatef(idle_rotation, 0, 1, 0)
            
            # Draw head (cyan sphere)
            glColor3f(*self.state_color)
            self._draw_sphere(0, 0, 0, 0.5, 16, 16)
            
            # Draw eyes
            self._draw_eyes(True)
        except ImportError:
            pass
    
    def _draw_listening_avatar(self):
        """Draw listening state (tilted head, animated)"""
        try:
            from OpenGL.GL import glRotatef, glColor3f
            
            # Head tilt
            listening_tilt = 15 * math.sin(self.animation_time * 0.5)
            glRotatef(listening_tilt, 0, 0, 1)
            
            # Pulsing color (cyan to bright cyan)
            pulse = 0.5 + 0.5 * math.sin(self.animation_time * 2)
            color = [0.0 * pulse, 1.0, 1.0 * (0.5 + 0.5 * pulse)]
            glColor3f(*color)
            
            self._draw_sphere(0, 0, 0, 0.5, 16, 16)
            self._draw_eyes(False)  # Eyes tracking sound
        except ImportError:
            pass
    
    def _draw_analyzing_avatar(self):
        """Draw analyzing state (rotating, pulsing)"""
        try:
            from OpenGL.GL import glRotatef, glColor3f
            
            # Rotating head
            rotation = 30 * (self.animation_time % (2 * math.pi)) / (2 * math.pi)
            glRotatef(rotation, 0, 1, 0)
            
            # Pulsing yellow/orange (analyzing)
            pulse = 0.5 + 0.5 * math.sin(self.animation_time * 3)
            color = [1.0, 0.8 * pulse, 0.0]
            glColor3f(*color)
            
            self._draw_sphere(0, 0, 0, 0.52, 16, 16)
            self._draw_eyes(False)
        except ImportError:
            pass
    
    def _draw_approved_avatar(self):
        """Draw approved state (happy, green)"""
        try:
            from OpenGL.GL import glRotatef, glColor3f
            
            # Slight head nod
            nod = 10 * math.sin(self.animation_time)
            glRotatef(nod, 1, 0, 0)
            
            # Green color
            glColor3f(0.2, 1.0, 0.2)
            self._draw_sphere(0, 0, 0, 0.5, 16, 16)
            
            # Happy eyes
            self._draw_happy_eyes()
        except ImportError:
            pass
    
    def _draw_denied_avatar(self):
        """Draw denied state (angry, red)"""
        try:
            from OpenGL.GL import glRotatef, glColor3f
            
            # Head shake
            shake = 15 * math.sin(self.animation_time * 2)
            glRotatef(shake, 0, 1, 0)
            
            # Red color
            glColor3f(1.0, 0.2, 0.2)
            self._draw_sphere(0, 0, 0, 0.5, 16, 16)
            
            # Angry eyes
            self._draw_angry_eyes()
        except ImportError:
            pass
    
    def _draw_locked_avatar(self):
        """Draw locked state (serious, dark red)"""
        try:
            from OpenGL.GL import glRotatef, glColor3f
            
            # Static, slight forward tilt
            glRotatef(10, 1, 0, 0)
            
            # Dark red color
            glColor3f(0.8, 0.1, 0.1)
            self._draw_sphere(0, 0, 0, 0.5, 16, 16)
            
            # Locked eyes (X pattern)
            self._draw_locked_eyes()
        except ImportError:
            pass
    
    def _draw_sphere(self, x: float, y: float, z: float, radius: float, lats: int, lons: int):
        """Draw a sphere using OpenGL"""
        try:
            from OpenGL.GL import glTranslatef, glPopMatrix, glPushMatrix, glBegin, glEnd, GL_TRIANGLE_STRIP, glVertex3f
            
            glPushMatrix()
            glTranslatef(x, y, z)
            
            glBegin(GL_TRIANGLE_STRIP)
            for i in range(lats + 1):
                lat0 = math.pi * (-0.5 + float(i - 1) / lats)
                lat1 = math.pi * (-0.5 + float(i) / lats)
                
                for j in range(lons + 1):
                    lng = 2 * math.pi * float(j - 1) / lons
                    
                    x0 = math.cos(lat0) * math.cos(lng)
                    y0 = math.sin(lat0)
                    z0 = math.cos(lat0) * math.sin(lng)
                    
                    x1 = math.cos(lat1) * math.cos(lng)
                    y1 = math.sin(lat1)
                    z1 = math.cos(lat1) * math.sin(lng)
                    
                    glVertex3f(x0 * radius, y0 * radius, z0 * radius)
                    glVertex3f(x1 * radius, y1 * radius, z1 * radius)
            
            glEnd()
            glPopMatrix()
        except ImportError:
            pass
    
    def _draw_eyes(self, blink: bool):
        """Draw neutral eyes"""
        try:
            from OpenGL.GL import glColor3f, glBegin, glEnd, GL_QUADS, glVertex3f, glTranslatef, glPopMatrix, glPushMatrix
            
            # Simple eye quads
            glColor3f(0.2, 0.2, 0.2)
            
            # Left eye
            glBegin(GL_QUADS)
            glVertex3f(-0.15, 0.1, 0.51)
            glVertex3f(-0.05, 0.1, 0.51)
            glVertex3f(-0.05, 0.2, 0.51)
            glVertex3f(-0.15, 0.2, 0.51)
            glEnd()
            
            # Right eye
            glBegin(GL_QUADS)
            glVertex3f(0.05, 0.1, 0.51)
            glVertex3f(0.15, 0.1, 0.51)
            glVertex3f(0.15, 0.2, 0.51)
            glVertex3f(0.05, 0.2, 0.51)
            glEnd()
        except ImportError:
            pass
    
    def _draw_happy_eyes(self):
        """Draw happy eyes (curved)"""
        pass
    
    def _draw_angry_eyes(self):
        """Draw angry eyes"""
        pass
    
    def _draw_locked_eyes(self):
        """Draw locked eyes (X pattern)"""
        pass
    
    def _draw_2d_fallback(self):
        """Fallback 2D rendering (doesn't use OpenGL)"""
        pass
    
    def set_state(self, state: str):
        """Set avatar animation state"""
        state_map = {
            "neutral": [0.0, 1.0, 1.0],
            "listening": [0.0, 1.0, 1.0],
            "analyzing": [1.0, 0.8, 0.0],
            "approved": [0.2, 1.0, 0.2],
            "denied": [1.0, 0.2, 0.2],
            "locked": [0.8, 0.1, 0.1]
        }
        
        if state in state_map:
            self.state = state
            self.state_color = state_map[state]
            self.animation_time = 0
            self.authentication_status_changed.emit(state)
