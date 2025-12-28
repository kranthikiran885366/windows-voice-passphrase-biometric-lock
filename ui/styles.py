"""
Cinematic Styling - Sivaji Security System UI Theme
Dark theme with neon accents
"""

STYLESHEET = """
    /* Main window */
    QMainWindow, QWidget {
        background-color: #0a0e27;
        color: #e0e0e0;
    }
    
    /* Title labels */
    QLabel#titleLabel {
        font-size: 48px;
        font-weight: bold;
        color: #00d9ff;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* Status text */
    QLabel#statusLabel {
        font-size: 24px;
        color: #7c3aed;
        font-weight: bold;
        margin: 20px 0;
    }
    
    /* Random sentence to speak */
    QLabel#sentenceLabel {
        font-size: 18px;
        color: #00d9ff;
        padding: 20px;
        border: 2px solid #7c3aed;
        border-radius: 8px;
        background-color: #0f1535;
        font-style: italic;
    }
    
    /* Microphone indicator */
    QLabel#micLabel {
        font-size: 64px;
        color: #00d9ff;
    }
    
    /* Messages */
    QLabel#messageLabel {
        font-size: 14px;
        color: #b0b0b0;
        margin: 20px;
        padding: 10px;
    }
    
    /* Status indicator */
    QLabel#statusIndicator {
        font-size: 12px;
        color: #00d9ff;
        margin: 5px;
    }
    
    /* Success message */
    QLabel#successLabel {
        font-size: 32px;
        color: #00ff66;
        font-weight: bold;
    }
    
    /* Error/Denial message */
    QLabel#errorLabel {
        font-size: 28px;
        color: #ff3333;
        font-weight: bold;
    }
"""

# Color palette
COLORS = {
    'background': '#0a0e27',
    'primary_accent': '#00d9ff',      # Cyan
    'secondary_accent': '#7c3aed',    # Violet
    'success': '#00ff66',              # Green
    'error': '#ff3333',                # Red
    'text_primary': '#e0e0e0',
    'text_secondary': '#b0b0b0',
}
