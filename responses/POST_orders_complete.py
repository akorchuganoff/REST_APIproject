from requests import post
print(post('http://127.0.0.1:8080/orders/complete', json={
"courier_id": 1,
"order_id": 4,
"complete_time": "2021-04-04T09:50:01.42Z"
}).json())
# {'assign_time': '2021-04-03 18:45:40.681067+00:00', 'order': [{'id': 1}, {'id': 2}, {'id': 3}, {'id': 4}, {'id': 5}, {'id': 6}, {'id': 7}, {'id': 8}, {'id': 11}]}