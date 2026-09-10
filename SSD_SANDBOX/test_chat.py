import urllib.request
req = urllib.request.Request('http://127.0.0.1:8000/api/user-message', method='POST', headers={'Content-Type': 'application/json'}, data=b'{"message": "test manual", "username": "Admin", "hash": "test1"}')
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(e)
