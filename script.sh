#!/usr/bin/env bash


# curl -s "http://127.0.0.1:5000/students"

# curl -s "http://127.0.0.1:5000/students/10"

curl -X POST http://127.0.0.1:5000/students \
  -H "Content-Type: application/json" \
  -d '[{
        "first_name": "John",
        "last_name": "Doe",
        "email": "joh@example.com",
        "address": "123 Main St",
        "city": "Anytown",
        "province": "ON",
        "country": "Canada",
        "address_type": "local",
        "is_international": 1,
        "program_id": 1
      },
      {
        "first_name": "",
        "last_name": "Smith",
        "email": "alice.smi@example.com",
        "address": "456 Oak Ave",
        "city": "Springfield",
        "province": "BC",
        "country": "Canada",
        "address_type": "permanent",
        "is_international": 0,
        "program_id": 2
      }]'


# curl -X PUT http://127.0.0.1:5000/students \
#   -H "Content-Type: application/json" \
#   -d '[{
#         "id": 1,
#         "first_name": "Alice",
#         "last_name": "Smith",
#         "email": "alice.smi@example.com",
#         "address": "456 Oak Ave",
#         "city": "Springfield",
#         "province": "BC",
#         "country": "Canada",
#         "address_type": "permanent",
#         "is_international": 0,
#         "program_id": 2
#       }]'

# curl -X PATCH http://localhost:5000/students \
#   -H "Content-Type: application/json" \
#   -d '{"ids": [2]}'
