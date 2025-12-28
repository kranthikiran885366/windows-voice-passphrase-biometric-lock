"""
Sivaji Audio Responses - Cinematic messages library
Enhanced with contextual responses and security notifications
"""

RESPONSES = {
    'welcome': {
        'text': "Welcome to the Sivaji Security System. Voice biometric authentication activated.",
        'lang': 'en',
        'priority': 'high'
    },
    'authentication_start': {
        'text': "Authentication sequence initiated. Speak the sentence displayed on screen.",
        'lang': 'en',
        'priority': 'high'
    },
    'listening': {
        'text': "Listening. Recording your voice biometric.",
        'lang': 'en',
        'priority': 'medium'
    },
    'analyzing': {
        'text': "Analyzing voice patterns. Comparing against enrolled profile.",
        'lang': 'en',
        'priority': 'medium'
    },
    'success': {
        'text': "Authentication successful. Voice verified. Welcome. System access granted.",
        'lang': 'en',
        'priority': 'high',
        'sentiment': 'positive'
    },
    'failure': {
        'text': "Unauthorized access detected. You are not permitted to use this system.",
        'lang': 'en',
        'priority': 'high',
        'sentiment': 'negative'
    },
    'failure_attempt_2': {
        'text': "Second unauthorized access attempt detected. One more attempt before lockout.",
        'lang': 'en',
        'priority': 'critical',
        'sentiment': 'negative'
    },
    'lockout': {
        'text': "Security violation confirmed. System locked for 15 minutes. Multiple unauthorized access attempts detected.",
        'lang': 'en',
        'priority': 'critical',
        'sentiment': 'negative'
    },
    'liveness_failed': {
        'text': "Liveness check failed. Possible recorded audio detected. Voice must be real-time.",
        'lang': 'en',
        'priority': 'high',
        'sentiment': 'negative'
    },
    'low_confidence': {
        'text': "Voice confidence below threshold. Please try again with clear pronunciation.",
        'lang': 'en',
        'priority': 'high'
    },
    'background_noise': {
        'text': "High background noise detected. Please reduce noise and try again.",
        'lang': 'en',
        'priority': 'medium'
    },
    'goodbye': {
        'text': "Session terminated. Sivaji Security System standing by.",
        'lang': 'en',
        'priority': 'medium'
    },
    'system_ready': {
        'text': "Sivaji Security System online. Ready for voice authentication.",
        'lang': 'en',
        'priority': 'high'
    },
    'enrollment_success': {
        'text': "Enrollment successful. Your voice profile has been created. System is now protected.",
        'lang': 'en',
        'priority': 'high',
        'sentiment': 'positive'
    },
    'enrollment_start': {
        'text': "Voice enrollment mode activated. You will speak 5 sentences to create your security profile.",
        'lang': 'en',
        'priority': 'high'
    }
}


def get_response(key):
    """Enhanced with validation and metadata access"""
    if key in RESPONSES:
        return RESPONSES[key].get('text', '')
    return f"[System Error: Unknown response key '{key}']"


def get_response_data(key):
    """Get full response data including priority and sentiment"""
    return RESPONSES.get(key, {})


def get_by_priority(priority='high'):
    """Get all responses of a given priority level"""
    return {k: v for k, v in RESPONSES.items() if v.get('priority') == priority}
