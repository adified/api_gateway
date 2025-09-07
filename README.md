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
