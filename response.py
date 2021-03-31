from requests import get,post,delete, patch



print(post('http://localhost:80/orders/assign', {'courier_id': 1}).json())