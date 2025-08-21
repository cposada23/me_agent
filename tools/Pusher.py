import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

class Pusher:
    """
    A class to handle push notifications using Pusher service.
    """
    
    def __init__(self):
        """
        Initialize Pusher with credentials from environment variables or parameters.
        """
        self.pushover_user = os.getenv('PUSHOVER_USER')
        self.pushover_token = os.getenv('PUSHOVER_TOKEN')
        
        # Validate required credentials
        if not all([self.pushover_user, self.pushover_token]):
            raise ValueError(
                "Missing Pusher credentials. Please set PUSHOVER_USER and PUSHOVER_TOKEN in your .env file or in your environment variables."
            )
        
        self.base_url = f"https://api.pushover.net/1/messages.json"
        self.logger = logging.getLogger(__name__)
    
    def push_notification(self, message: str) -> Dict[str, Any]:
        """
        Send a push notification to the user.

        Args:
            message: The message to send to the user

        Returns:
            dict: {'status_code': int, 'response': dict or str} on success,
                  or {'error': str} on failure.
        """
        try:
            # Prepare the payload
            payload = {
                'user': self.pushover_user,
                'token': self.pushover_token,
                'message': message
            }

            # Make the API request
            response = requests.post(
                self.base_url,
                data=payload
            )

            try:
                response_data = response.json()
            except Exception:
                response_data = response.text

            return {
                'status_code': response.status_code,
                'response': response_data
            }

        except requests.exceptions.RequestException as e:
            return {'error': f"Network error while sending notification: {str(e)}"}
        except Exception as e:
            return {'error': f"Unexpected error while sending notification: {str(e)}"}
