```python 
# yourapp/helpers.py

import requests
from django.conf import settings

class InAppNotificationClient:
    def __init__(self):
        self.base_url = settings.WEBSOCKET_SERVICE_URL

    def send_message(self, title, message, user_id):
        send_message_url = self.base_url+"/send-message"
        send_message_url += "&message=" + message
        send_message_url += "&title=" + title
        send_message_url += "&user_id" + user_id
        try:
            response = requests.post(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
```

Usage Example
```python
InAppNotificationClient().send_message(
    title='Title exmaple', 
    message='message example.',
    user_id='23'
)
```