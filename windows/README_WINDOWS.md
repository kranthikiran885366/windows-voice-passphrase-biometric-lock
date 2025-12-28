# Windows Integration Guide - v3.0 Enterprise Edition

<div align="center">

[![Windows](https://img.shields.io/badge/Windows-10%2F11%2FServer-blue.svg)](https://www.microsoft.com/windows/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Integration](https://img.shields.io/badge/Integration-Enterprise%20Ready-green.svg)](#)
[![Security](https://img.shields.io/badge/Security-Quantum%20Resistant-red.svg)](#)
[![Compliance](https://img.shields.io/badge/Compliance-GDPR%2FHIPAA-purple.svg)](#)

</div>

<p align="center">
  <strong>Enterprise-grade Windows integration with quantum-resistant security and zero-trust architecture</strong>
</p>

<p align="center">
  Advanced deployment guide for Windows 10/11/Server with Active Directory, Group Policy, and enterprise management features
</p>

---

## 📋 Overview

Sivaji Security System v3.0 provides enterprise-grade Windows integration with:
- **Zero-Trust Architecture**: Continuous verification and risk-based authentication
- **Active Directory Integration**: Seamless domain authentication and user management
- **Group Policy Support**: Centralized configuration and policy enforcement
- **Quantum-Resistant Security**: Post-quantum cryptography for future-proof protection
- **Multi-Modal Biometrics**: Voice, face, iris, and behavioral authentication
- **Enterprise Dashboard**: Real-time monitoring and management console
- **Compliance Framework**: GDPR, HIPAA, SOX, PCI-DSS compliance modules

---

## 🚀 Installation Methods v3.0

### Method 1: Enterprise MSI Deployment (Recommended)

<div align="center">

**Automated deployment via Group Policy with centralized management.**

</div>

**Features:**
- ✅ Silent installation with predefined configurations
- ✅ Active Directory integration
- ✅ Centralized policy management
- ✅ Automatic updates and rollback
- ✅ Compliance reporting

**Deployment Steps:**
```powershell
# Download enterprise MSI
Invoke-WebRequest -Uri "https://releases.sivaji.ai/v3.0/sivaji-enterprise.msi" -OutFile "sivaji-enterprise.msi"

# Deploy via Group Policy
msiexec /i sivaji-enterprise.msi /quiet TRANSFORMS=enterprise.mst

# Verify installation
Get-WmiObject -Class Win32_Product | Where-Object {$_.Name -like "*Sivaji*"}
```

### Method 2: Credential Provider Integration (Enterprise)

<div align="center">

**Native Windows logon replacement with biometric authentication.**

</div>

**Features:**
- ✅ True pre-login integration
- ✅ Replaces Windows password prompt
- ✅ SYSTEM-level security
- ✅ Prevents bypass attempts
- ✅ Supports smart cards and tokens

**Installation:**
```powershell
# Register credential provider
regsvr32 SivajiCredentialProvider.dll

# Configure via registry
New-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers" -Name "{SIVAJI-GUID}" -Value "Sivaji Biometric Provider"

# Enable biometric logon
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Biometrics" -Name "Enabled" -Value 1
```

### Method 3: Azure AD Integration (Cloud)

<div align="center">

**Cloud-native deployment with Azure Active Directory integration.**

</div>

**Features:**
- ✅ Azure AD conditional access
- ✅ Multi-tenant support
- ✅ Cloud-based policy management
- ✅ SSO integration
- ✅ Mobile device management

**Setup:**
```powershell
# Install Azure AD module
Install-Module AzureAD

# Connect to Azure AD
Connect-AzureAD

# Register Sivaji application
New-AzureADApplication -DisplayName "Sivaji Security System" -IdentifierUris "https://sivaji.yourdomain.com"
```

---

## ⚙️ Enterprise Configuration v3.0

### Active Directory Integration

**Domain Controller Setup:**
```powershell
# Install Sivaji AD Schema Extensions
ldifde -i -f sivaji-schema.ldif -s dc.yourdomain.com -c "DC=X" "DC=yourdomain,DC=com"

# Configure biometric attributes
Set-ADUser -Identity "username" -Add @{sivajiVoicePrint="encrypted_voiceprint_data"}

# Setup group policies
New-GPO -Name "Sivaji Security Policy" | New-GPLink -Target "OU=Users,DC=yourdomain,DC=com"
```

### Group Policy Configuration

**Administrative Templates:**
```
Computer Configuration
└─ Administrative Templates
   └─ Sivaji Security System
      ├─ Authentication Settings
      ├─ Biometric Policies
      ├─ Security Thresholds
      └─ Compliance Settings
```

**Registry Settings:**
```powershell
# Enable enterprise mode
Set-ItemProperty -Path "HKLM:\SOFTWARE\Sivaji\Security" -Name "EnterpriseMode" -Value 1

# Configure authentication timeout
Set-ItemProperty -Path "HKLM:\SOFTWARE\Sivaji\Security" -Name "AuthTimeout" -Value 30

# Set compliance level
Set-ItemProperty -Path "HKLM:\SOFTWARE\Sivaji\Security" -Name "ComplianceLevel" -Value "HIPAA"
```

### Environment Variables v3.0

Create `config/enterprise.env`:
```env
# Core Settings
SIVAJI_MODE=ENTERPRISE
SIVAJI_VERSION=3.0
SIVAJI_LICENSE_KEY=your_enterprise_license_key

# Security Settings
SIVAJI_QUANTUM_CRYPTO=enabled
SIVAJI_ZERO_TRUST=enabled
SIVAJI_COMPLIANCE_MODE=GDPR_HIPAA

# Performance Settings
SIVAJI_GPU_ACCELERATION=enabled
SIVAJI_EDGE_COMPUTING=enabled
SIVAJI_CACHE_SIZE=1024MB

# Integration Settings
SIVAJI_AD_INTEGRATION=enabled
SIVAJI_AZURE_AD=enabled
SIVAJI_SSO_PROVIDER=SAML2

# Monitoring Settings
SIVAJI_TELEMETRY=enabled
SIVAJI_AUDIT_LEVEL=VERBOSE
SIVAJI_SIEM_ENDPOINT=https://siem.yourdomain.com
```

---

## 🆕 New Security Features (v2.1)

### Master Key Management
- 🔐 Centralized credential storage in `security/credentials/.master_key`
- 🔒 Enhanced encryption for all sensitive data
- 🔄 Secure key rotation capabilities

### Failsafe State Management
- 💾 Encrypted system state backup in `data/failsafe_state.enc`
- 🆘 Disaster recovery capabilities
- ✅ System integrity verification

### Enhanced Speaker Model
- 🤖 Improved AI model accuracy
- ⚡ Better performance optimization
- 📉 Reduced false positives

---

## 🚀 Updated Installation Commands

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

---

## 🔧 Troubleshooting

<div align="center">

| Issue | Cause | Solution |
|-------|-------|----------|
| **System runs Sivaji but then shows logon screen** | Startup method runs too late | Use Method 3 (Custom Credential Provider) |
| **"Access Denied" when running installer** | Insufficient privileges | Right-click Python prompt → "Run as Administrator" |
| **Sivaji doesn't start on boot** | Script/registry issues | Check Startup folder, Python path, registry key |
| **Keyboard shortcuts still work** | PyQt5 runs in user mode | Use Method 3 for kernel-level control |

</div>

---

## 🛡️ Security Notes

<div align="center">

### ⚠️ Current Implementation (Method 1-2):
- Runs at user privilege level
- System keys (Ctrl+Alt+Del, Alt+Tab) can bypass
- For demonstration and testing

### 🔒 For Production Deployment:
- Implement Method 3 (Credential Provider DLL)
- Runs at SYSTEM level (kernel-mode)
- Handles all Windows logon events
- Prevents all bypass methods

</div>

---

## 🔄 Development vs. Production

<div align="center">

| Aspect | Development (Methods 1-2) | Production (Method 3) |
|--------|---------------------------|----------------------|
| **Setup** | Quick testing | Secure pre-login authentication |
| **Compilation** | No compilation needed | Kernel-level integration |
| **Compatibility** | Works on all systems | Prevents direct OS bypass |
| **Security** | Basic protection | Requires code signing |

</div>

---

## 🗑️ Reverting Windows Integration

To remove Sivaji from startup:

```bash
python main.py --windows-uninstall
```

Or manually:

1. Remove shortcut from Startup folder
2. Delete registry key if Method 2
3. Restart system

---

## 🧪 Testing

### Test 1: Verify Startup Execution
1. Restart Windows
2. Sivaji should appear before desktop
3. Speak sentence to authenticate

### Test 2: Verify Lockout
1. Fail authentication 3 times
2. System should lock for 15 minutes
3. Check audit logs

### Test 3: Verify Audit Trail
```bash
python scripts/check_audit_logs.py
```

---

## 📚 References

<div align="center">

- [Windows Logon Architecture](https://docs.microsoft.com/en-us/windows/win32/secauthn/logon-architecture)
- [Credential Providers](https://docs.microsoft.com/en-us/windows/win32/secauthn/credential-providers-in-windows-vista)
- [PyQt5 on Windows](https://doc.qt.io/qt-5/windows-deployment.html)

</div>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

```
MIT License - Copyright (c) 2025 Sivaji Security System
```

---

<div align="center">

**Last Updated**: January 2025 | **Version**: 3.0 (Enterprise Edition with Quantum-Resistant Security)

</div>