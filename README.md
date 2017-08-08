# Lockerobe-API

## Answer Create

- action: `/questions/{question_pk}/answer/`
- method: POST
- body:
```
{
    'content': {{ content }},
}
```

## Answer Update

- action: `/answers/{pk}/`
- method: POST
- body:
```
{
    'content': {{ content }},
}
```

## Answer Upvote

Upvote 상태가 토글됩니다.
- action: `/answers/upvote/` (`{% url 'quora:answer_vote_toggle' type='up' %}`)
- method: POST
- body:
```
{
    'pk': {{ answer.pk }},
}
```

# Environment

- Python 3.5
- `python3 -m venv venv`
- `pip3 install -r requirements.txt`
