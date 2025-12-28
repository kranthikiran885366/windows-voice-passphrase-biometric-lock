# Windows 10/11 Integration Guide

## Pre-Login Authentication

This guide covers integrating Sivaji with Windows logon to provide security before the user gains desktop access.

## Method Comparison

| Method | Privilege | Timing | Bypass Possible | Complexity |
|--------|-----------|--------|-----------------|------------|
| **1: Startup Script** | User | Post-login | Yes (Alt+Tab) | Low ✅ |
| **2: Registry Run Key** | Admin | Early boot | Yes (system keys) | Medium |
| **3: Credential Provider** | System | Pre-login | No | High |

## Method 1: Startup Script (Recommended for Testing)

### Setup

**Step 1: Create Startup Shortcut**

1. Open: `C:\Users\<YourUsername>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
2. Right-click → New → Shortcut
3. Target: `python "C:\path\to\sivaji\startup_script.py"`
4. Name: "Sivaji Security System"
5. Finish

**Step 2: Test on Reboot**

\`\`\`
Press: Win + R
Type: shutdown /r /t 60 /c "Testing Sivaji"
Press: Enter

[System reboots in 60 seconds]
[Sivaji appears before desktop loads]
[Authenticate with voice]
[Desktop loads on success]
\`\`\`

**Advantages:**
✅ No admin required
✅ Easy to test
✅ No registry modifications
✅ Easy to uninstall (delete shortcut)

**Disadvantages:**
⚠️ System hotkeys can bypass
⚠️ Desktop briefly visible during load
⚠️ Runs after OS initialization

---

## Method 2: Registry Run Key (Intermediate)

### Setup

**Step 1: Run as Administrator**

1. Right-click Command Prompt → Run as Administrator
2. Paste:
\`\`\`bash
python "C:\path\to\sivaji\main.py" --windows-install
\`\`\`

**Step 2: Verify Installation**

1. Open: `regedit` (Registry Editor)
2. Navigate: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
3. Verify entry: `SivajiSecuritySystem` = `python "C:\...\startup_script.py"`

**Step 3: Test**

\`\`\`
Restart computer
Sivaji appears earlier than Method 1
Authenticate with voice
\`\`\`

**Advantages:**
✅ Runs earlier than Startup folder
✅ System-wide (not user-specific)
✅ Persists across user logouts

**Disadvantages:**
⚠️ Requires admin privileges
⚠️ System keys still can bypass
⚠️ Harder to uninstall

### Uninstall

\`\`\`bash
# As Administrator
python "C:\path\to\sivaji\main.py" --windows-uninstall
\`\`\`

---

## Method 3: Custom Credential Provider (Production)

### Overview

A Credential Provider is a Windows component that handles user logon. Custom providers can replace or augment the default logon UI.

### Architecture

\`\`\`
┌──────────────────────────────────┐
│      Windows Logon UI            │
│   (Credential Provider)          │
│                                  │
│  [Sivaji Voice Auth]             │
│  🎤 "Speak sentence..."          │
│                                  │
│  [Standard Logon as backup]      │
└──────────────────────────────────┘
        ↓
    [Success]
        ↓
┌──────────────────────────────────┐
│   Userenv.exe (Profile Loading)  │
│   Desktop Startup                │
└──────────────────────────────────┘
\`\`\`

### Implementation (Advanced)

**Components Needed:**

1. **C++ DLL** (`SivajiProvider.dll`)
   - Implements `ICredentialProvider` COM interface
   - Embedded TensorFlow for model inference
   - Uses Windows Crypto API for encryption

2. **Python Wrapper** (optional)
   - Calls C++ DLL via ctypes
   - Handles file I/O and logging

3. **Registry Installation**
   - Register DLL in: `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers`

### C++ Skeleton

\`\`\`cpp
// SivajiProvider.h
#include <credentialprovider.h>

class SivajiCredentialProvider : public ICredentialProvider {
public:
    // Constructor
    SivajiCredentialProvider();
    
    // ICredentialProvider methods
    HRESULT GetFieldDescriptorCount(DWORD* pdwCount);
    HRESULT GetFieldDescriptorAt(DWORD dwIndex, CREDENTIAL_PROVIDER_FIELD_DESCRIPTOR** ppcpfd);
    HRESULT GetCredentialCount(DWORD* pdwCount, DWORD* pdwDefault, BOOL* pbAutoLogonWithDefault);
    HRESULT GetCredentialAt(DWORD dwIndex, ICredentialProviderCredential** ppcpc);
    
private:
    // Voice authentication
    int VerifyVoiceAuthentication();
    
    // TensorFlow inference
    int RunModelInference(float* mfcc_features);
};
\`\`\`

### Registration

\`\`\`bash
# As Administrator in System32 folder
regsvr32 SivajiProvider.dll

# Then set as active provider:
# HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\
# {CLSID_OF_SIVAJI} = "Sivaji Voice Authentication"
\`\`\`

**Advantages:**
✅ Pre-login (runs before logon UI)
✅ No system key bypass possible
✅ Kernel-level security
✅ Production-grade integration

**Disadvantages:**
⚠️ Requires C++ expertise
⚠️ Must be code-signed
⚠️ Requires compilation & testing
⚠️ OS-specific (Windows only)

---

## Group Policy Deployment (Enterprise)

For deploying across multiple Windows machines in a domain:

### Step 1: Create Group Policy Object

\`\`\`
Open: Group Policy Management Console (gpmc.msc)
Navigate: Forest > Domains > YOUR_DOMAIN > Group Policy Objects
Right-click: New
Name: "Sivaji Voice Authentication"
\`\`\`

### Step 2: Configure Startup Script

\`\`\`
Edit Policy:
  Computer Configuration
    → Windows Settings
    → Scripts (Startup/Shutdown)
    → Startup
    → Add Script

Script Path: \\file-server\scripts\startup_script.py
\`\`\`

### Step 3: Link to Organizational Unit

\`\`\`
Right-click: YOUR_OU
Link: Sivaji Voice Authentication GPO
Enforce: Yes (prevent override)
\`\`\`

### Step 4: Test Deployment

\`\`\`
On domain machine:
  gpupdate /force  (refresh policies)
  shutdown /r      (reboot to test)
\`\`\`

---

## Troubleshooting

### Issue: Sivaji Doesn't Start on Boot

**Check 1: Startup Folder**
\`\`\`bash
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
# Verify Sivaji shortcut exists
\`\`\`

**Check 2: Registry Entry (Method 2)**
\`\`\`bash
regedit
# Navigate to Run key and verify entry
\`\`\`

**Check 3: Event Viewer**
\`\`\`
Event Viewer → Windows Logs → System
Look for errors related to python.exe or startup scripts
\`\`\`

### Issue: Keyboard Still Works (Alt+Tab, Ctrl+Alt+Del)

**Cause**: User-mode application cannot intercept system keys

**Solution for Testing**: Use Method 1 (shortcut) only in test environment

**Solution for Production**: Implement Method 3 (Credential Provider at SYSTEM privilege)

### Issue: Desktop Visible Before Sivaji Appears

**Cause**: Method 1 runs after OS initialization

**Solutions**:
1. Use Method 2 (Registry Run Key) for earlier execution
2. Use Method 3 (Credential Provider) for pre-login
3. Disable "Fast Startup" (may not help much)

### Issue: "Access Denied" When Running Installer

**Solution**: Right-click Command Prompt → "Run as Administrator"

### Issue: Python Path Not Found

**Solution**: Use full path to Python executable

\`\`\`bash
# Instead of:
python main.py --windows-install

# Use:
"C:\Program Files\Python311\python.exe" "C:\path\to\sivaji\main.py" --windows-install
\`\`\`

---

## Configuration

### Environment Variables

Create `windows\.env`:

\`\`\`
# Startup behavior
SIVAJI_LOGON_TIMEOUT=60
SIVAJI_STARTUP_DELAY=5000

# Security
SIVAJI_LOCKOUT_DURATION=900
SIVAJI_MAX_ATTEMPTS=3

# Appearance
SIVAJI_FULLSCREEN=true
SIVAJI_DISABLE_TASKBAR=true
SIVAJI_DISABLE_KEYS=true

# Logging
SIVAJI_AUDIT_LOG_PATH=C:\Users\Public\Logs\SivajiAudit.log
SIVAJI_DEBUG=false
\`\`\`

---

## Security Hardening

### For Production Deployment

1. **Code Signing**
   \`\`\`
   Sign DLL with EV certificate
   Verify signatures before execution
   \`\`\`

2. **BitLocker Integration**
   \`\`\`
   Encrypt system drive with BitLocker
   Store encryption key in TPM
   Sivaji runs before BitLocker unlock
   \`\`\`

3. **TPM 2.0 Support**
   \`\`\`
   Store encryption keys in TPM
   Prevents key extraction from disk
   \`\`\`

4. **Secure Boot**
   \`\`\`
   Ensure UEFI Secure Boot enabled
   Only signed bootloaders and drivers load
   \`\`\`

5. **Windows Defender Integration**
   \`\`\`
   Register credential provider with Defender
   Exclude from scanning (prevent interference)
   \`\`\`

---

## Migration from Testing to Production

### Phase 1: Pilot (1-10 Users)
- Use Method 1 (Startup Script)
- Gather user feedback
- Refine enrollment process

### Phase 2: Early Adoption (10-100 Users)
- Deploy via Method 2 (Registry Run Key)
- Monitor audit logs
- Conduct security testing

### Phase 3: Production (100+ Users)
- Develop and deploy Credential Provider (Method 3)
- Full security audit
- IT support training
- User documentation

---

## Support & Troubleshooting

### Common Questions

**Q: Can I use Sivaji on Windows 10 Home Edition?**
A: Yes, all methods work on Home edition. Method 3 (Credential Provider) may require additional permissions.

**Q: What if I forget my voice?**
A: Enroll a new voice print. Old authentication disabled.

**Q: Can I have multiple users?**
A: Yes, each user has separate voice profile. Stored encrypted in `security/credentials/`

**Q: Is Ctrl+Alt+Del bypassed?**
A: In Method 1-2 (user mode): Ctrl+Alt+Del shows logon screen
In Method 3 (system mode): Ctrl+Alt+Del is handled by Sivaji

---

## References

- [Windows Credential Providers](https://docs.microsoft.com/en-us/windows/win32/secauthn/credential-providers-in-windows-vista)
- [MSDN: ICredentialProvider Interface](https://docs.microsoft.com/en-us/windows/win32/api/credentialprovider/nn-credentialprovider-icredentialprovider)
- [Windows Logon Architecture](https://docs.microsoft.com/en-us/windows/win32/secauthn/logon-architecture)
- [Group Policy Deployment](https://learn.microsoft.com/en-us/windows/client-management/group-policy-overview)
