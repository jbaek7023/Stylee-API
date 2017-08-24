# Stylee-API

Backend API for Stylee.

### Authentication / Authorization URL

| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /rest-auth/login/ | Login | POST | username / password | |
| /rest-auth/password/reset/ | Send token for Reset password | POST | email |uid / token |
| /rest-auth/password/reset/confirm/ | Reset the password | POST |  uid / token / new_password1 / new_password2 | |
| /rest-auth/password/change/ | change password | POST |   new_password1 / new_password2 / (old_password) | |
| /rest-auth/registration/ | Register | POST | username / password1 / password2 / email |  |
| /rest-auth/registration/verify-email/ | Verify Email | POST | key | |
| /rest-auth/facebook/ | authorization with Facebook | POST | access_token | token |

### Menu URL
| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /profile/detail | Get Profile Information | GET |  |  |

### Stylebook URL
| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /profile/<id>/ | Get user's Profile information | GET |  |  |

### Wardrobe URL
| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /example/<id>/ | Get user's Profile information | GET |  |  |

### Notification URL
| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /example/<id>/ | Get user's Profile information | GET |  |  |

### Feed URL
| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /example/<id>/ | Get user's Profile information | GET |  |  |

### Reference :
- django-rest-auth: http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html

#### Unused URL
- /rest-auth/logout.
- /rest-auth/user/ (GET, PUT, PATCH)

# Environment
- Python 3.5 'python3 '
- virtualenv . && source bin/activate
- `pip3 install -r requirements.txt`
- git config --global credential.helper cache
