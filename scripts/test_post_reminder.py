import requests
r = requests.post('http://127.0.0.1:8000/api/v1/message', json={'user_id':'u1','text':'remind me to buy milk at 6pm'})
print(r.status_code)
print(r.json())
