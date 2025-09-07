# API Gateway

simple django API gateway with auth and rate limiting

## Setup

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
redis-server
python manage.py runserver

## Usage

make requests with your API key:

curl -H "X-API-KEY: your-key" http://127.0.0.1:8000/test/posts/1

Test it:

python test_proxy.py

## Admin

Go to `http://127.0.0.1:8000/admin/` to:

- add API keys
- configure backend services
- view request logs

Rate limit: 100 requests per hour per API key

## note

I am using a docker contaner for redis

## Future scope

Containerise the entire application

## too many requests error

❯ curl -i -H "X-API-KEY: hIezAX0-FiBIyjDXsLPYNxLomogoKjBb6Fog5hcLlIo" http://localhost:8000/test/posts/1
❯ HTTP/1.1 429 Too Many Requests
Date: Sun, 07 Sep 2025 16:56:56 GMT
Server: WSGIServer/0.2 CPython/3.9.6
Content-Type: application/json
X-Frame-Options: DENY
Content-Length: 31
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
Vary: origin

{"error": " too many requests"}%

## unauthorised error, because of wrong api key

❯ curl -i -H "X-API-KEY: hIezAX0-FiBIyjDXsLPYNxLomogoKjBb6FoghcLlIo" http://localhost:8000/test/posts/1
❯ HTTP/1.1 401 Unauthorized
Date: Sun, 07 Sep 2025 17:00:37 GMT
Server: WSGIServer/0.2 CPython/3.9.6
Content-Type: application/json
X-Frame-Options: DENY
Content-Length: 25
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
Vary: origin

{"error": "Unauthorized"}%
