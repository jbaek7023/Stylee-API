# Lockerobe-API

Backend API for Lockerobe. 


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
