#!/usr/bin/env bash


# curl -s "http://127.0.0.1:5000/students"

# curl -s "http://127.0.0.1:5000/students/10"

curl -X POST http://127.0.0.1:5000/students \
  -H "Content-Type: application/json" \
  -d '{
        "first_name": "John",
        "last_name": "Doe",
        "email": "johnd@example.com",
        "address": "123 Main St",
        "city": "Anytown",
        "province": "ON",
        "country": "Canada",
        "address_type": "local",
        "is_international": 1,
        "program_id": 1
      }'

# curl -s -X PUT "http://127.0.0.1:5000/students/1" \
#      -H "Content-Type: application/json" \
#      -d '{
#            "name": "John Doe",
#            "age": 20,
#            "major": "Computer Science"
#          }'

