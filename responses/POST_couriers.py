from requests import get,post,delete, patch
print(post('http://127.0.0.1:8080/couriers', json={
  "data": [
    {
      "courier_id": 1,
      "courier_type": "car",
      "regions": [1, 2, 3],
      "working_hours": ['09:00-12:00', '14:00-16:00', '17:00-19:00']
    },
    {
      "courier_id": 2,
      "courier_type": "bike",
      "regions": [1, 2, 3],
      "working_hours": ['09:00-18:00']
    },
    {
      "courier_id": 3,
      "courier_type": "foot",
      "regions": [1, 2, 3],
      "working_hours": ['09:00-18:00']
    }
  ]
}).json())