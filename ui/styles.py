"""
Cinematic Styling - Security System UI Theme
Dark theme with neon accents
"""

STYLESHEET = """
    /* Main window */
    QMainWindow, QWidget {
        background-color: #0a0e27;
        color: #e0e0e0;
    }

    /* Glassmorphism panel for auth */
    .glass-panel {
        background: rgba(20, 24, 50, 0.7);
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1.5px solid rgba(0, 217, 255, 0.18);
        padding: 32px 40px;
        margin: 0 0 32px 0;
    }

    /* Title labels */
    QLabel#titleLabel {
        font-size: 54px;
        font-weight: 900;
        color: #00d9ff;
        text-transform: uppercase;
        letter-spacing: 4px;
        text-shadow: 0 2px 16px #00d9ff88;
        margin-bottom: 8px;
    }

    /* Status text */
    QLabel#statusLabel {
        font-size: 28px;
        color: #7c3aed;
        font-weight: bold;
        margin: 24px 0 12px 0;
        letter-spacing: 1.5px;
        text-shadow: 0 1px 8px #7c3aed55;
    }

    /* Random sentence to speak */
    QLabel#sentenceLabel {
        font-size: 20px;
        color: #00d9ff;
        padding: 18px 24px;
        border: 2px solid #7c3aed;
        border-radius: 12px;
        background-color: #0f1535cc;
        font-style: italic;
        margin-bottom: 12px;
        box-shadow: 0 2px 12px #00d9ff22;
        transition: border 0.3s, color 0.3s;
    }

    /* Microphone indicator */
    QLabel#micLabel {
        font-size: 72px;
        color: #00d9ff;
        text-shadow: 0 2px 16px #00d9ff55;
        margin: 12px 0;
    }

    /* Messages */
    QLabel#messageLabel {
        font-size: 16px;
        color: #b0b0b0;
        margin: 18px 0 10px 0;
        padding: 12px 18px;
        border-radius: 8px;
        background: rgba(30, 30, 60, 0.4);
        box-shadow: 0 1px 8px #0002;
    }

    /* Status indicator */
    QLabel#statusIndicator {
        font-size: 14px;
        color: #00d9ff;
        margin: 8px 0;
    }

    /* Success message */
    QLabel#successLabel {
        font-size: 32px;
        color: #00ff66;
        font-weight: bold;
        text-shadow: 0 2px 12px #00ff6688;
    }

    /* Error/Denial message */
    QLabel#errorLabel {
        font-size: 28px;
        color: #ff3333;
        font-weight: bold;
        text-shadow: 0 2px 12px #ff333388;
    }

    /* Modern button */
    QPushButton {
        background: linear-gradient(90deg, #7c3aed 0%, #00d9ff 100%);
        color: #fff;
        padding: 14px 36px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 1.5px;
        box-shadow: 0 2px 12px #00d9ff33;
        transition: background 0.3s, box-shadow 0.3s, transform 0.2s;
    }
    QPushButton:hover {
        background: linear-gradient(90deg, #00d9ff 0%, #7c3aed 100%);
        box-shadow: 0 4px 24px #00d9ff66;
        transform: scale(1.04);
    }
    QPushButton:pressed {
        background: #5c27a0;
        box-shadow: 0 1px 4px #7c3aed88;
        transform: scale(0.98);
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
