from requests import post
print(post('http://0.0.0.0:8080/orders/complete', json={
"courier_id": 1,
"order_id": 2,
"complete_time": "2021-04-04T11:50:01.42Z"
}).json())