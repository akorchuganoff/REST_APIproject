from requests import get,post,delete, patch

print(post('http://localhost:80/orders', json={
  "data": [
    {
      "order_id": 1,
      "weight": 0.23,
      "region": 12,
      "delivery_hours": '09:00-18:00'
    },
    {
      "order_id": 2,
      "weight": 0.23,
      "region": 12,
      "delivery_hours": '09:00-18:00'
    }
  ]
}).json())