**Integrating JWT with Django Rest Framework**

**1. Install Dependencies**

Install the required packages using pip:

```bash
pip install djangorestframework djangorestframework-simplejwt
```

**2. Update Django Settings**

**Add `rest_framework_simplejwt` to `INSTALLED_APPS`**

In your `settings.py` file, add `rest_framework` and `rest_framework_simplejwt` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    # other apps
    'rest_framework',
    'rest_framework_simplejwt',
]
```

**Configure REST Framework to Use JWT**

Set up Django Rest Framework to use JWT authentication by adding the following to your `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
```

**Configure JWT Settings**

Customize JWT settings as needed. Add the following to your `settings.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your_secret_key',
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
```

**3. Create Token Views**

Add URL patterns for token obtain and refresh views:

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # other urls
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**4. Obtain and Pass JWT Token**

To obtain a JWT token, send a POST request to the `/api/token/` endpoint with user credentials:

**Request:**

```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**

```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

Store the access token on the client (e.g., in local storage or a cookie) and include it in the Authorization header for subsequent API requests:

```http
Authorization: Bearer your_access_token
```

**5. Use JWT Token in Session**

To use the JWT token in the user session, set it as a cookie:

```python
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

def set_jwt_cookie(request):
    user = request.user
    refresh = RefreshToken.for_user(user)
    response = JsonResponse({'message': 'JWT Token set in cookie'})
    response.set_cookie(
        key='jwt_access_token',
        value=str(refresh.access_token),
        httponly=True,  # Helps mitigate XSS attacks
        secure=True,    # Use only over HTTPS
        samesite='Strict'  # Prevents cross-site requests
    )
    return response
```

**Summary**

1. Install `djangorestframework-simplejwt`.
2. Configure Django settings for JWT.
3. Create token obtain and refresh views.
4. Obtain the JWT token by sending user credentials to `/api/token/`.
5. Use the JWT token in your client application.

For more information, refer to the [Django Rest Framework Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/).

