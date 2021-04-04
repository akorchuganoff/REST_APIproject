from requests import get,post,delete, patch
print(post('http://127.0.0.1:8080/orders/assign', {'courier_id': 1}).json())