"""
Sivaji Security System - Main Entry Point (Enhanced with Developer Fail-Safe)
Production-grade AI voice biometric authentication with multi-biometric support
"""

import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from ui.lockscreen import SivajiLockscreen
from voice_auth.enrollment_pipeline import EnrollmentPipeline
from voice_auth.multi_biometric_verification import MultibiometricVerifier
from security.encryption import EncryptionManager
from security.developer_failsafe import DeveloperFailsafeManager
from security.audit_logger import AuditLogger
from ai_models.model_inference import ModelInference
from config.system_config import SystemConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


class FailsafeDetector:
    """Detect system failures that warrant fail-safe activation"""
    
    def __init__(self):
        self.failures = []
    
    def check_microphone(self) -> bool:
        """Check microphone availability"""
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            info = p.get_default_input_device_info()
            p.terminate()
            logger.info("[v0] Microphone check: OK")
            return True
        except Exception as e:
            logger.error(f"[v0] Microphone check failed: {e}")
            self.failures.append(('MICROPHONE_FAILURE', str(e)))
            return False
    
    def check_voice_model(self) -> bool:
        """Check voice model availability"""
        try:
            inference = ModelInference()
            assert inference.model is not None
            logger.info("[v0] Voice model check: OK")
            return True
        except Exception as e:
            logger.error(f"[v0] Voice model check failed: {e}")
            self.failures.append(('MODEL_CRASH', str(e)))
            return False
    
    def check_system(self) -> bool:
        """Check overall system health"""
        all_ok = self.check_microphone() and self.check_voice_model()
        return all_ok
    
    def has_critical_failure(self) -> tuple:
        """Check if critical failure detected"""
        if not self.check_system():
            if self.failures:
                return True, self.failures[0]
        return False, None


def main():
    """Main entry point for Sivaji Security System"""
    
    parser = argparse.ArgumentParser(
        description="Sivaji Security System - AI Voice Biometric Authentication"
    )
    parser.add_argument(
        "--mode",
        choices=["auth", "enroll", "config", "test", "setup-developer-secret", 
                 "request-otk", "check-failsafe-status", "disable-failsafe"],
        default="auth",
        help="Run mode"
    )
    parser.add_argument(
        "--username",
        default="authorized_user",
        help="Username for enrollment mode"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--config",
        default="config/system_config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--enable-face",
        action="store_true",
        help="Enable facial recognition biometric"
    )
    parser.add_argument(
        "--enable-iris",
        action="store_true",
        help="Enable iris recognition biometric"
    )
    parser.add_argument(
        "--failure-type",
        help="System failure type for OTK request"
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load system configuration
    config = SystemConfig.load_from_file(args.config)
    
    # Initialize encryption and audit logging
    encryption_manager = EncryptionManager()
    audit_logger = AuditLogger()
    
    # Initialize developer fail-safe
    failsafe = DeveloperFailsafeManager(
        encryption_key=encryption_manager.get_encryption_key(),
        audit_logger=audit_logger
    )
    
    print("\n" + "="*70)
    print("SIVAJI SECURITY SYSTEM - AI Voice Biometric Authentication")
    print("="*70)
    print(f"Mode: {args.mode.upper()}")
    print(f"Active Biometrics: {', '.join(config.get_active_biometrics())}")
    print("="*70 + "\n")
    
    if args.mode == "setup-developer-secret":
        print("DEVELOPER FAIL-SAFE SETUP")
        print("-" * 70)
        secret = input("Enter new developer secret (hidden): ")
        confirm = input("Confirm secret (hidden): ")
        
        if secret == confirm and len(secret) >= 12:
            encrypted_secret = failsafe.set_developer_secret(secret)
            print(f"\nDeveloper secret configured successfully!")
            print("Store this encrypted hash securely:")
            print(encrypted_secret)
            print("\nFail-safe is now active. Request OTKs when needed:")
            print("  python main.py --mode request-otk --failure-type MICROPHONE_FAILURE")
        else:
            print("ERROR: Secrets don't match or too short (min 12 chars)")
    
    elif args.mode == "request-otk":
        print("DEVELOPER ONE-TIME KEY REQUEST")
        print("-" * 70)
        
        failure_type = args.failure_type or input("System failure type: ")
        
        # Verify failsafe integrity
        is_ok, msg = failsafe.verify_failsafe_integrity()
        if not is_ok:
            print(f"ERROR: {msg}")
            return
        
        # Detect system failure
        if failsafe.detect_system_failure(failure_type):
            otk = failsafe.generate_one_time_key(validity_minutes=15)
            print(f"\n✓ One-time key generated successfully!")
            print(f"  Key: {otk}")
            print(f"  Valid for: 15 minutes")
            print(f"  Single-use only")
            print(f"\nTo activate fail-safe:")
            print(f"  1. Run the system and wait for failure prompt")
            print(f"  2. Enter developer secret")
            print(f"  3. Press Ctrl+Alt+F12+D (physical confirmation)")
            print(f"  4. Enter the OTK above")
        else:
            print("ERROR: System failure not detected or invalid type")
    
    elif args.mode == "check-failsafe-status":
        print("DEVELOPER FAIL-SAFE STATUS")
        print("-" * 70)
        
        # Verify failsafe integrity
        is_ok, msg = failsafe.verify_failsafe_integrity()
        print(f"Integrity: {'OK' if is_ok else 'TAMPERED'}")
        if not is_ok:
            print(f"  ⚠ {msg}")
        
        status = failsafe.get_failsafe_status()
        print(f"\nStatus:")
        print(f"  Active: {status['is_active']}")
        print(f"  Valid: {status['is_valid']}")
        print(f"  Time Remaining: {status['time_remaining']:.0f}s")
        print(f"  Uses Remaining: {status['uses_remaining']}")
        print(f"  Tamper Detected: {status['tamper_detected']}")
        print(f"  Integrity OK: {status['integrity_ok']}")
    
    elif args.mode == "disable-failsafe":
        print("DISABLE DEVELOPER FAIL-SAFE")
        print("-" * 70)
        
        if failsafe.is_failsafe_active:
            secret = input("Enter developer secret to confirm: ")
            if failsafe.verify_developer_secret(secret):
                failsafe.deactivate_failsafe("Manual disable via CLI")
                print("✓ Fail-safe deactivated")
            else:
                print("✗ Invalid developer secret")
        else:
            print("Fail-safe not currently active")
    
    elif args.mode == "enroll":
        print("VOICE BIOMETRIC ENROLLMENT")
        print("-" * 70)
        enrollment = EnrollmentPipeline(
            username=args.username,
            debug=args.debug,
            enable_face=args.enable_face,
            enable_iris=args.enable_iris
        )
        enrollment.run_enrollment()
    
    elif args.mode == "config":
        print("SYSTEM CONFIGURATION")
        print("-" * 70)
        print("\nCurrent Configuration:")
        from dataclasses import asdict
        config_dict = {
            "security": asdict(config.security),
            "biometric": asdict(config.biometric),
            "ui": asdict(config.ui),
            "notification": asdict(config.notification)
        }
        print(json.dumps(config_dict, indent=2))
        
        response = input("\nDo you want to modify settings? (y/n): ")
        if response.lower() == 'y':
            config.security.max_failed_attempts = int(
                input("Max failed attempts (default 5): ") or 5
            )
            config.security.lockout_duration_minutes = int(
                input("Lockout duration in minutes (default 30): ") or 30
            )
            config.biometric.enable_face = input("Enable face recognition? (y/n): ").lower() == 'y'
            config.biometric.enable_iris = input("Enable iris recognition? (y/n): ").lower() == 'y'
            config.notification.enable_email = input("Enable email alerts? (y/n): ").lower() == 'y'
            
            config.save_to_file(args.config)
            print("\n✓ Configuration saved!")
    
    elif args.mode == "test":
        print("SYSTEM TEST & DIAGNOSTICS")
        print("-" * 70)
        run_system_tests(config, args.debug, failsafe)
    
    else:  # Default auth mode
        print("VOICE BIOMETRIC AUTHENTICATION")
        print("-" * 70)
        
        detector = FailsafeDetector()
        has_failure, failure_info = detector.has_critical_failure()
        
        if has_failure:
            failure_type, failure_detail = failure_info
            print(f"\n⚠ SYSTEM FAILURE DETECTED")
            print(f"Type: {failure_type}")
            print(f"Details: {failure_detail}")
            print(f"\nDeveloper fail-safe available.")
            print(f"To activate emergency access:")
            print(f"  1. Request one-time key:")
            print(f"     python main.py --mode request-otk --failure-type {failure_type}")
            print(f"  2. Enter developer secret when prompted")
            print(f"  3. Press Ctrl+Alt+F12+D (physical confirmation)")
            print(f"  4. Enter the provided one-time key")
            
            # Check failsafe integrity
            is_ok, msg = failsafe.verify_failsafe_integrity()
            if not is_ok:
                print(f"\n✗ CRITICAL: Fail-safe system integrity compromised!")
                print(f"  {msg}")
                return
            
            print(f"\nFail-safe system integrity: OK")
            return
        
        # Normal authentication flow
        lockscreen = SivajiLockscreen(
            enable_face=args.enable_face or config.biometric.enable_face,
            enable_iris=args.enable_iris or config.biometric.enable_iris,
            failsafe_manager=failsafe  # Pass failsafe to lockscreen
        )
        lockscreen.show()
        sys.exit(lockscreen.exec_())


def run_system_tests(config: SystemConfig, debug: bool = False, failsafe = None):
    """Run system diagnostics and tests"""
    from dataclasses import asdict
    
    tests = {
        "Audio I/O": test_audio_io,
        "Voice Model": test_voice_model,
        "Encryption": test_encryption,
        "Storage": test_storage,
        "Failsafe Integrity": lambda: test_failsafe_integrity(failsafe),
    }
    
    if config.biometric.enable_face:
        tests["Face Model"] = test_face_model
    
    if config.biometric.enable_iris:
        tests["Iris Model"] = test_iris_model
    
    results = {}
    for test_name, test_func in tests.items():
        try:
            test_func()
            results[test_name] = "PASSED"
            print(f"✓ {test_name}: PASSED")
        except Exception as e:
            results[test_name] = f"FAILED: {str(e)}"
            print(f"✗ {test_name}: FAILED - {str(e)}")
    
    print("\n" + "-"*70)
    print("Test Summary:")
    passed = sum(1 for r in results.values() if r == "PASSED")
    total = len(results)
    print(f"  Passed: {passed}/{total}")
    for test, result in results.items():
        status = "PASS" if result == "PASSED" else "FAIL"
        print(f"  {test}: {status}")


def test_audio_io():
    """Test audio input/output"""
    import pyaudio
    p = pyaudio.PyAudio()
    info = p.get_default_input_device_info()
    p.terminate()
    assert info is not None


def test_voice_model():
    """Test voice model loading"""
    from ai_models.model_inference import ModelInference
    inference = ModelInference()
    assert inference.model is not None


def test_face_model():
    """Test face model loading"""
    from ai_models.face_recognition_model import FaceRecognitionModel
    model = FaceRecognitionModel()
    assert model.model is not None


def test_iris_model():
    """Test iris model loading"""
    from ai_models.iris_recognition_model import IrisRecognitionModel
    model = IrisRecognitionModel()
    assert model.model is not None


def test_encryption():
    """Test encryption system"""
    from security.encryption import EncryptionManager
    enc = EncryptionManager()
    test_data = b"test data"
    encrypted = enc.encrypt_data(test_data)
    decrypted = enc.decrypt_data(encrypted)
    assert test_data == decrypted


def test_storage():
    """Test storage and file system"""
    Path("enrollments").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    assert Path("enrollments").exists()
    assert Path("logs").exists()


def test_failsafe_integrity(failsafe):
    """Test fail-safe system integrity"""
    if failsafe is None:
        raise Exception("Fail-safe manager not initialized")
    
    is_ok, msg = failsafe.verify_failsafe_integrity()
    assert is_ok, msg


if __name__ == "__main__":
    main()
