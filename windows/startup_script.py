"""
Startup Script - Executed before desktop access
Launches Sivaji authentication
"""

import sys
from pathlib import Path
import subprocess

def main():
    """Execute Sivaji authentication at startup"""
    project_root = Path(__file__).parent.parent
    main_script = project_root / "main.py"
    
    print("\n" + "="*60)
    print("SIVAJI SECURITY SYSTEM - STARTUP")
    print("="*60)
    print("\nInitializing voice biometric authentication...")
    
    try:
        # Run main authentication
        result = subprocess.run(
            [sys.executable, str(main_script), "--mode", "auth"],
            check=False
        )
        
        # Return code 0 = authentication success
        if result.returncode == 0:
            print("✓ Authentication successful. Proceeding to desktop...")
            return True
        else:
            print("✗ Authentication failed. Desktop access denied.")
            # Lock desktop
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            return False
    
    except Exception as e:
        print(f"✗ Error during startup: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
