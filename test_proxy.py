import requests

API_KEY = "EQQudkProp8F5bwJHKB8SttEDugCDSCHgJ3t85PpKZc"
GATEWAY_URL = "http://127.0.0.1:8000/test/posts/1"

print("proxied request demo")

# make request through api gateway
headers = {"X-API-KEY": API_KEY}

try:
    response = requests.get(GATEWAY_URL, headers=headers, stream=True)
    print(f"Status Code: {response.status_code}")
    print("proxying is working.")
    
except Exception as e:
    print(f"Error: {e}")
    print("make sure django server is running")

print("rate limiting demo")

for i in range(1, 110):
    try:
        response = requests.get(GATEWAY_URL, headers=headers, stream=True)
        print(f"request {i}: status {response.status_code}")
        if response.status_code == 429:
            print(f"rate limited")
    except Exception as e:
        print(f"request {i}: error {e}")