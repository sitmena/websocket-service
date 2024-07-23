To connect to a WebSocket service using JWT for authentication in JavaScript, and to handle token refresh, follow this guide. The process involves:

1. **Establishing the WebSocket connection**
2. **Handling authentication with JWT**
3. **Refreshing the token when needed**

Here's a step-by-step guide:

### 1. Establishing the WebSocket Connection

To establish a WebSocket connection, you'll need to include the JWT token in the connection request. This usually involves setting up a WebSocket connection with an appropriate URL.

**Example WebSocket Connection:**

```javascript
// Assuming you have the token stored in localStorage
const accessToken = localStorage.getItem('access_token');

// Create a WebSocket connection
const socket = new WebSocket('wss://your-websocket-url/', {
    headers: {
        'Authorization': `Bearer ${accessToken}`
    }
});

socket.onopen = () => {
    console.log('WebSocket connection opened');
};

socket.onmessage = (event) => {
    console.log('Message from server', event.data);
};

socket.onerror = (error) => {
    console.error('WebSocket error', error);
};

socket.onclose = () => {
    console.log('WebSocket connection closed');
};
```

### 2. Handling Authentication with JWT

When connecting to the WebSocket, include the JWT in the `Authorization` header. However, the WebSocket protocol itself doesn't directly support headers. Instead, you can pass the token as part of the URL query string or use a custom handshake mechanism.

**Example with URL Query String:**

```javascript
// Add token to the query string
const socket = new WebSocket(`wss://your-websocket-url/?token=${accessToken}`);
```

### 3. Refreshing the Token

Since WebSocket connections are long-lived, you'll need a strategy to handle token expiration and refresh the token as needed.

**Example Refresh Token Strategy:**

1. **Set Up Token Refresh Logic:**

   Use a function to refresh the JWT token when it expires. You'll likely need a function to handle token requests.

   ```javascript
   async function refreshToken() {
       try {
           const response = await fetch('https://your-api-url/api/token/refresh/', {
               method: 'POST',
               headers: {
                   'Content-Type': 'application/json',
               },
               body: JSON.stringify({
                   refresh: localStorage.getItem('refresh_token')
               })
           });
           const data = await response.json();
           if (response.ok) {
               localStorage.setItem('access_token', data.access);
               return data.access;
           } else {
               throw new Error('Failed to refresh token');
           }
       } catch (error) {
           console.error('Token refresh error:', error);
       }
   }
   ```

2. **Reconnect WebSocket with New Token:**

   If the WebSocket connection is closed due to token expiration, you'll need to reconnect with the new token.

   ```javascript
   function setupWebSocket() {
       const accessToken = localStorage.getItem('access_token');

       const socket = new WebSocket(`wss://your-websocket-url/?token=${accessToken}`);

       socket.onopen = () => {
           console.log('WebSocket connection opened');
       };

       socket.onmessage = (event) => {
           console.log('Message from server', event.data);
       };

       socket.onerror = async (error) => {
           console.error('WebSocket error', error);

           // If the error is due to authentication failure, refresh the token
           if (error.message.includes('401')) {
               const newToken = await refreshToken();
               if (newToken) {
                   setupWebSocket(); // Reconnect with new token
               }
           }
       };

       socket.onclose = () => {
           console.log('WebSocket connection closed');
       };
   }

   // Initial WebSocket setup
   setupWebSocket();
   ```

3. **Handling Token Expiration on the Client Side:**

   You should monitor token expiration on the client side and refresh tokens accordingly. This might involve intercepting errors or handling specific messages from the server indicating token expiration.

**Summary**

- **Establish WebSocket Connection:** Include JWT in URL query or headers if possible.
- **Refresh Token:** Use a refresh token endpoint to obtain a new access token.
- **Reconnect with New Token:** Reconnect WebSocket with the new token if the connection is closed due to authentication issues.

By implementing these steps, you can maintain a secure and functional WebSocket connection with JWT authentication and handle token refresh seamlessly.