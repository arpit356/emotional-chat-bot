import requests
try:
    r = requests.post('http://127.0.0.1:8000/api/v1/message', json={'user_id':'u1','text':'hello from test'})
    print('status', r.status_code)
    print(r.json())
except Exception as e:
    print('error', e)
