# Windows 10/11 Integration Guide - v2.1

[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Integration](https://img.shields.io/badge/Integration-Pre--Login-green.svg)](#)

## Overview

Sivaji Security System can be integrated with Windows login to provide pre-desktop authentication with enhanced security features including master key management and encrypted failsafe state.

## Installation Methods

### Method 1: Startup Script (Easiest)

Runs Sivaji after Windows loads but before user gains desktop access.

**Steps:**
1. Open Startup folder: `Win + R` → `shell:startup`
2. Create shortcut to `startup_script.py`
3. Test by restarting Windows

**Advantages:**
- Easy to implement
- No registry modifications needed
- Works on standard user accounts

**Disadvantages:**
- Runs after OS initialization
- User can see desktop briefly during load

### Method 2: Registry Run Key (Intermediate)

Launches Sivaji early in Windows startup via Run registry key.

**Steps:**
1. Run as Administrator
2. Execute: `python main.py --windows-install`
3. System will register startup hook

**Registry Location:**
\`\`\`
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
\`\`\`

### Method 3: Custom Logon Provider (Advanced)

True pre-login integration - replaces Windows logon UI.

**Requirements:**
- C++ DLL for credential provider
- Registry modifications
- Admin + SYSTEM privileges

**Implementation:**
See `SYSTEM_ARCHITECTURE.md` for credential provider design.

## Configuration

### Environment Variables

Create `windows/.env`:
\`\`\`
SIVAJI_LOGON_TIMEOUT=60
SIVAJI_LOCKOUT_DURATION=900
SIVAJI_DISABLE_BYPASS=true
\`\`\`

### Group Policy (Enterprise)

For domain-joined computers:

1. Open `gpedit.msc`
2. Navigate to: `Computer Configuration > Windows Settings > Scripts > Startup`
3. Add startup script pointing to `startup_script.py`

## Troubleshooting

### System runs Sivaji but then shows logon screen

**Cause:** Startup method runs too late

**Solution:** Use Method 3 (Custom Credential Provider) for true pre-login

### "Access Denied" when running installer

**Solution:** Right-click Python prompt → "Run as Administrator"

### Sivaji doesn't start on boot

**Check:**
1. Script is in user's Startup folder
2. Python path is correct
3. No import errors: `python startup_script.py`
4. Registry key exists (if Method 2)

### Keyboard shortcuts still work (Alt+Tab, Ctrl+Alt+Del)

**Limitation:** PyQt5 lockscreen runs in user mode, cannot intercept system keys

**Workaround:** For maximum security, use Method 3 (kernel-level control)

## Security Notes

⚠️ **Current Implementation (Method 1-2):**
- Runs at user privilege level
- System keys (Ctrl+Alt+Del, Alt+Tab) can bypass
- For demonstration and testing

⚠️ **For Production Deployment:**
- Implement Method 3 (Credential Provider DLL)
- Runs at SYSTEM level (kernel-mode)
- Handles all Windows logon events
- Prevents all bypass methods

## Development vs. Production

### Development (Methods 1-2)
- Quick testing
- No compilation needed
- Works on all systems

### Production (Method 3)
- Secure pre-login authentication
- Kernel-level integration
- Prevents direct OS bypass
- Requires code signing

## Reverting Windows Integration

To remove Sivaji from startup:

\`\`\`bash
python main.py --windows-uninstall
\`\`\`

Or manually:

1. Remove shortcut from Startup folder
2. Delete registry key if Method 2
3. Restart system

## Testing

### Test 1: Verify Startup Execution
1. Restart Windows
2. Sivaji should appear before desktop
3. Speak sentence to authenticate

### Test 2: Verify Lockout
1. Fail authentication 3 times
2. System should lock for 15 minutes
3. Check audit logs

### Test 3: Verify Audit Trail
\`\`\`bash
python scripts/check_audit_logs.py
\`\`\`

## References

- [Windows Logon Architecture](https://docs.microsoft.com/en-us/windows/win32/secauthn/logon-architecture)
- [Credential Providers](https://docs.microsoft.com/en-us/windows/win32/secauthn/credential-providers-in-windows-vista)
- [PyQt5 on Windows](https://doc.qt.io/qt-5/windows-deployment.html)

## New Security Features (v2.1)

### Master Key Management
- Centralized credential storage in `security/credentials/.master_key`
- Enhanced encryption for all sensitive data
- Secure key rotation capabilities

### Failsafe State Management
- Encrypted system state backup in `data/failsafe_state.enc`
- Disaster recovery capabilities
- System integrity verification

### Enhanced Speaker Model
- Improved AI model accuracy
- Better performance optimization
- Reduced false positives

## Updated Installation Commands

### Initialize Security System
```bash
# First-time setup with new security features
python main.py --mode setup-developer-secret
python main.py --mode init-master-key
python main.py --mode backup-system-state
```

### Windows Integration with Enhanced Security
```bash
# Install with new security features
python main.py --windows-install --enable-master-key
```

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

```
MIT License - Copyright (c) 2025 Sivaji Security System
```