import logging
import requests

class NotificationTool:
    def __init__(self, channels=None):
        self.channels = channels or [
            {"type": "console", "enabled": True}
        ]
    
    def send_notification(self, message, level="info"):
        """Send notification through all enabled channels"""
        for channel in self.channels:
            if channel.get("enabled", False):
                if channel["type"] == "console":
                    self._send_console(message, level)
                elif channel["type"] == "webhook":
                    self._send_webhook(message, channel.get("url"))
    
    def _send_console(self, message, level="info"):
        """Send notification to console"""
        if level == "error":
            logging.error(message)
        elif level == "warning":
            logging.warning(message)
        else:
            logging.info(message)
    
    def _send_webhook(self, message, webhook_url):
        """Send notification to webhook"""
        if not webhook_url:
            return
        
        try:
            payload = {
                "message": message
            }
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            logging.info(f"Webhook notification sent successfully")
        except Exception as e:
            logging.error(f"Failed to send webhook notification: {str(e)}")
