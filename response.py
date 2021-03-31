from requests import get,post,delete, patch

# print(delete('http://localhost:80/couriers/1').json())
print(post('http://localhost:80/couriers', {
  "data": [
    {
      "courier_id": 2,
      "courier_type": "car",
      "regions": '123',
      "working_hours": '09:00-18:00'
    }
  ]
}).json())

# print(post('http://localhost:80/couriers', {'data': [[1, 2], [2, 3], [3, 4]]}).json())
# print(get('http://localhost:80/couriers').json())
# print(delete('http://localhost:80/couriers/1').json())