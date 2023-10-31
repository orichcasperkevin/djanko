# djanko
 Djanko is a Django app that brings passkey authentication by Hanko (https://www.hanko.io/) to your django projects.

 ## PyPI
 `pip install -i https://test.pypi.org/simple/ djanko`  
 
  Dont worry, this is a test account, A real pyPI account on the works

## Quick start
-----------

1. Add "djanko" to your `INSTALLED_APPS` setting like this:

  `  INSTALLED_APPS = [
        ...,
        "djanko",
    ]
  `

2. Add the djanko authentication class to your Rest framework default classes::

    `REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'djanko.authentication.HankoAuthentication',
        ]
    }
   `

4. Add your hanko API URL and audience claim to your `settings.py` :
    `
    HANKO_API_URL = config('HANKO_URL')
    HANKO_JWT_AUDIENCE_CLAIM = 'localhost'
  `

3. Include the djanko URLconf in your project urls.py like this::

    `path('djanko/',include('djanko.api.urls')),`

4. Run ``python manage.py migrate`` to create the polls models.

5. Start the development server and visit `http://127.0.0.1:8000/`.


6. You will now have the `/djanko/sign-up/` url available to you, use it to create users in your system using the bearer token obtained from your hanko frontend elements :
   
```

    curl --request POST \
    --url http://localhost:8000/djanko/sign-up/ \
    --header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUyYzU4MWZhLThmZGQtNDYxOC1iMmU4LWJjN2Q4YWJmZDFkYiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsibG9jYWxob3N0Il0sImV4cCI6MTY5ODc0NjI3NywiaWF0IjoxNjk4NzQyNjc3LCJzdWIiOiIzM2Y4ZTAwZi01YjU1LTRkNGUtOTAwYi1jZTNjMWUwMmRiOTYifQ.K9BEUDMSOjcSJzm4udK7stN-0I3x9SgH6bcuAoxafeqXgh2ZDEfopZuAZJDgc-ZgVoA6V1RaXNPi0cu_2_yV2IYiDba0TOBjnO3Q-fu04YCbh2zoC_wNBZ69Y5CoCFCNpIQ185iHRznMNemaARAwAYBjrtv1kLy1bZ36R0nDfgvZg68fnt_p3n5zjxftFsKPocJgYMGCNbV0VUT3bTju-tQQNqdmg4dYN8WuXrfticA2okexOBKKbbxMyCb_-GI1JxWTwsD_hOkG-0CLXI-lsDUo-foAPKfOEOqO6A2avZgQEJX2ro1tvMheRF9HrFGUK48fxoZ_WXEJfg8shN1T9PsbY8ekwONYfYab8wymawD0B1hxYnl09GRhBNCBiAMPpQX7cK8gfcDn4SIvJVVB6H5g-y3wuZj59_qWyhCXYVxnouC8B69i2ivwRdPJdEIgzIGmQxnsaP3g1mMa50Vt7fpUq-a4J-8NJeafqzxa2AOYfoEwBC9o84GIANW6f0r0ZNfu821axY6zT7F7LsA2s_wd1l1jerA7ayY1oRtqWGZMgqeOh448uaJgLjW2pFvwdtU4SVCTAl06ji50_txdCUQ4j6WB4gxKUpa8L6HQYAMDJZyzaSwcH6MBBDzuU2GqBlpERyKcnLugFhOUvww68UCzaAUbJenwW7j8aB6_mZw)==' \
    --header 'Content-Type: application/json' \
    --data '{
        "username":"John_doe",
        "email":"johnDoe59@example.com",
        "first_name":"John",
        "last_name":"Doe"
    }'
```

8. Now every DRF endpoint will be authenticated using hanko passkeys. Enjoy
