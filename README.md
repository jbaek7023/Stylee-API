# Lockerobe-API

Backend API for Lockerobe.

## Login with credential
- action: `/api-token-auth/`
- method: POST
- body:
```
{
  'username' : {{ username }},
  'password' : {{ password }},
}
```
- test:
`curl -X POST -d "username=jbaek7023&password=!Jj8803838" http://localhost:8000/api-token-auth/`
```
{"token":"ey-ee"}
```

## Authenticate with user's Token
- action: `any url`
- test:
`curl -H "Authorization: JWT <token>" http://localhost:8000/protected-url/`

## Answer Create

- action: `/questions/{question_pk}/answer/`
- method: POST
- body:
```
{
    'content': {{ content }},
}
```

# Environment

- Python 3.5 'python3 '
- virtualenv . && source bin/activate
- `pip3 install -r requirements.txt`
- git config --global credential.helper cache
