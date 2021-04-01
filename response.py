from requests import get,post,delete, patch
print(post('http://localhost:80/orders/complete', json={
"courier_id": 2,
"order_id": 33,
"complete_time": "2021-01-10T10:33:01.42Z"
}).json())