# Stylee-API

Backend API for Stylee.

### Authentication / Authorization URL

| URL        | Action           | Method  | body | Return Value |
| ------------- |:-------------:| -----:|------------- |-------------|
| /rest-auth/login/ | Login | POST | username / password | |
| /rest-auth/password/change/ | Change Password | POST |   new_password1 / new_password2 / (old_password) | |
| /rest-auth/registration/ | Create New User | POST | username / password1 / password2 / email |  |
| /rest-auth/facebook/ | authorization with Facebook | POST | access_token | token |

* Planned Stuff : registar phone

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
- /rest-auth/password/reset/
- /rest-auth/password/reset/confirm/ | Reset the password | POST |  uid / token / new_password1 / new_password2 | |
- /rest-auth/registration/verify-email/ | Verify Email | POST | key | |

# Environment
- Python 3.5 'python3 '
- virtualenv . && source bin/activate
- `pip3 install -r requirements.txt`
- git config --global credential.helper cache
