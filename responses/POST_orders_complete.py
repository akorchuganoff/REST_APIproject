from requests import post
print(post('http://130.193.55.13:8080/orders/complete', json={
"courier_id": 1,
"order_id": 9,
"complete_time": "2021-04-04T11:50:01.42Z"
}).json())

# {'order_id': 1}
# {'order_id': 2}
# {'message': 'Bad Request'}