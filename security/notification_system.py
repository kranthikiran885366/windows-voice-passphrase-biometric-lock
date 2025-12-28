"""
Multi-Channel Notification System
Sends alerts via Email, SMS, and system notifications
"""

import json
import smtplib
from pathlib import Path
from datetime import datetime
from typing import List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class NotificationSystem:
    """
    Send notifications via multiple channels:
    - Email
    - SMS (Twilio)
    - Push notifications
    - System notifications
    """
    
    def __init__(self, config_path: str = "security/notification_config.json"):
        """Initialize notification system"""
        self.config = self._load_config(config_path)
        self.notification_queue = []
        self.email_enabled = self.config.get("email_enabled", False)
        self.sms_enabled = self.config.get("sms_enabled", False)
    
    def _load_config(self, config_path: str) -> dict:
        """Load notification configuration"""
        default_config = {
            "email_enabled": False,
            "email_smtp_server": "smtp.gmail.com",
            "email_smtp_port": 587,
            "email_from": "sivaji-security@example.com",
            "email_app_password": "",
            
            "sms_enabled": False,
            "sms_provider": "twilio",
            "sms_account_sid": "",
            "sms_auth_token": "",
            "sms_from_number": "",
            
            "push_notifications": True,
            "system_notifications": True,
            
            "alert_recipients": {
                "admin_emails": [],
                "admin_phones": [],
                "owner_email": ""
            },
            
            "alert_templates": {
                "UNAUTHORIZED_ACCESS": "Unauthorized access attempt detected",
                "SYSTEM_LOCKED": "System locked due to multiple failed attempts",
                "CRITICAL_THREAT": "Critical threat detected on your account",
                "AUTHENTICATION_SUCCESS": "Successful authentication on your device"
            }
        }
        
        if Path(config_path).exists():
            with open(config_path) as f:
                loaded = json.load(f)
                default_config.update(loaded)
        
        return default_config
    
    def send_alert(self, alert_type: str, details: dict = None) -> bool:
        """
        Send alert via configured channels
        
        Args:
            alert_type: One of UNAUTHORIZED_ACCESS, SYSTEM_LOCKED, CRITICAL_THREAT, etc.
            details: Additional alert details
        
        Returns:
            True if sent successfully
        """
        alert_message = self.config["alert_templates"].get(alert_type, alert_type)
        
        success = True
        
        # Send via email
        if self.email_enabled:
            if not self._send_email(alert_type, alert_message, details):
                success = False
        
        # Send via SMS
        if self.sms_enabled:
            if not self._send_sms(alert_type, alert_message, details):
                success = False
        
        # System notification
        if self.config.get("system_notifications", True):
            self._show_system_notification(alert_type, alert_message)
        
        return success
    
    def _send_email(self, alert_type: str, message: str, details: dict = None) -> bool:
        """Send email alert"""
        try:
            smtp_server = self.config["email_smtp_server"]
            smtp_port = self.config["email_smtp_port"]
            sender = self.config["email_from"]
            password = self.config["email_app_password"]
            recipients = self.config["alert_recipients"]["admin_emails"]
            
            if not recipients or not password:
                return False
            
            # Create email
            msg = MIMEMultipart()
            msg["From"] = sender
            msg["To"] = ", ".join(recipients)
            msg["Subject"] = f"SIVAJI ALERT: {alert_type}"
            
            # Build email body
            body = f"""
SIVAJI SECURITY ALERT
{'=' * 50}

Alert Type: {alert_type}
Timestamp: {datetime.now().isoformat()}
Message: {message}

Details:
{json.dumps(details, indent=2) if details else "No additional details"}

{'=' * 50}
This is an automated alert from your Sivaji Security System.
Do not reply to this email.
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"[v0] Failed to send email: {str(e)}")
            return False
    
    def _send_sms(self, alert_type: str, message: str, details: dict = None) -> bool:
        """Send SMS alert via Twilio"""
        try:
            # Requires: pip install twilio
            from twilio.rest import Client
            
            account_sid = self.config["sms_account_sid"]
            auth_token = self.config["sms_auth_token"]
            from_number = self.config["sms_from_number"]
            recipients = self.config["alert_recipients"]["admin_phones"]
            
            if not account_sid or not auth_token or not recipients:
                return False
            
            client = Client(account_sid, auth_token)
            
            sms_body = f"SIVAJI: {alert_type} - {message}"
            
            for recipient in recipients:
                client.messages.create(
                    body=sms_body,
                    from_=from_number,
                    to=recipient
                )
            
            return True
        
        except ImportError:
            print("[v0] Twilio not installed. Install with: pip install twilio")
            return False
        except Exception as e:
            print(f"[v0] Failed to send SMS: {str(e)}")
            return False
    
    def _show_system_notification(self, title: str, message: str):
        """Show system notification"""
        try:
            import platform
            
            if platform.system() == "Windows":
                self._show_windows_notification(title, message)
            elif platform.system() == "Darwin":
                self._show_macos_notification(title, message)
            elif platform.system() == "Linux":
                self._show_linux_notification(title, message)
        
        except Exception as e:
            print(f"[v0] Failed to show system notification: {str(e)}")
    
    def _show_windows_notification(self, title: str, message: str):
        """Show Windows notification"""
        try:
            from win10toast import ToastNotifier
            notifier = ToastNotifier()
            notifier.show_toast(title, message, duration=10)
        except ImportError:
            pass
    
    def _show_macos_notification(self, title: str, message: str):
        """Show macOS notification"""
        try:
            import subprocess
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script])
        except:
            pass
    
    def _show_linux_notification(self, title: str, message: str):
        """Show Linux notification (D-Bus)"""
        try:
            import subprocess
            subprocess.run(["notify-send", title, message])
        except:
            pass
    
    def queue_notification(self, alert_type: str, details: dict = None):
        """Queue notification for batch sending"""
        notification = {
            "type": alert_type,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "sent": False
        }
        self.notification_queue.append(notification)
    
    def flush_notifications(self) -> int:
        """Send all queued notifications"""
        sent_count = 0
        for notification in self.notification_queue:
            if not notification["sent"]:
                if self.send_alert(notification["type"], notification["details"]):
                    notification["sent"] = True
                    sent_count += 1
        
        return sent_count
