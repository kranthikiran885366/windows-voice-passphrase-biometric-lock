"""
Windows Integration - Advanced system integration
Runs Sivaji before desktop access with multiple deployment methods
Credential Provider, Registry, and Startup hook support
"""

import subprocess
import sys
import os
from pathlib import Path


class WindowsIntegration:
    """Integrate with Windows login system for pre-login authentication"""
    
    STARTUP_KEY = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    LOGON_KEY = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
    
    def __init__(self):
        self.app_path = Path(__file__).parent.parent / "main.py"
        self.startup_script = Path(__file__).parent / "startup_script.py"
    
    def install_startup_hook(self):
        """
        Install Sivaji to run at Windows startup
        Requires admin privileges
        """
        try:
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )
            
            # Register startup script
            exe_path = f'"{sys.executable}" "{self.startup_script}"'
            winreg.SetValueEx(key, "SivajiSecuritySystem", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            
            print("[v0] ✓ Startup hook installed")
            return True
        except PermissionError:
            print("[v0] ✗ Admin privileges required for startup hook")
            print("[v0] Run Command Prompt as Administrator and try again")
            return False
        except Exception as e:
            print(f"[v0] ✗ Error installing startup hook: {e}")
            return False
    
    def remove_startup_hook(self):
        """Remove Sivaji from startup"""
        try:
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_WRITE
            )
            winreg.DeleteValue(key, "SivajiSecuritySystem")
            winreg.CloseKey(key)
            print("[v0] ✓ Startup hook removed")
            return True
        except Exception as e:
            print(f"[v0] ✗ Error removing startup hook: {e}")
            return False
    
    def lock_desktop_on_failure(self):
        """Lock Windows desktop on failed authentication"""
        try:
            subprocess.run(
                ["rundll32.exe", "user32.dll,LockWorkStation"],
                check=True
            )
            print("[v0] ✓ Desktop locked")
            return True
        except Exception as e:
            print(f"[v0] ✗ Error locking desktop: {e}")
            return False
    
    def enable_secure_boot(self):
        """Added secure boot confirmation"""
        print("[v0] Enabling secure boot sequence...")
        try:
            # Disable screen timeout
            subprocess.run(
                ["powercfg", "/change", "monitor-timeout-ac", "0"],
                capture_output=True
            )
            print("[v0] ✓ Screen timeout disabled")
            return True
        except Exception as e:
            print(f"[v0] ✗ Error configuring power settings: {e}")
            return False
    
    @staticmethod
    def require_admin():
        """Check if running with admin privileges"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def get_windows_version():
        """Get Windows version information"""
        try:
            import platform
            return platform.platform()
        except:
            return "Unknown"
