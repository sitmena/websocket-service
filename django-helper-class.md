```python 
# yourapp/helpers.py

import requests
from django.conf import settings

class FastAPIClient:
    def __init__(self):
        self.base_url = settings.WEBSOCKET_SERVICE

    def send_message(self, token: str, message: str):
        url = f"{self.base_url}/send-message"
        payload = {
            'token': token,
            'message': message
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

```