#!/usr/bin/env bash

BASE_URL="http://127.0.0.1:5000"

get_resource() {
  local resource=$1
  local id=$2
  local keyword=$3

  if [ -n "$id" ]; then
    curl -s "$BASE_URL/$resource/$id" | jq
  elif [ "$keyword" == "active" ]; then
    curl -s "$BASE_URL/$resource?active_only=true" | jq
  else
    curl -s "$BASE_URL/$resource" | jq
  fi
}

post_resource() {
  local resource=$1
  local data=$2
  curl -X POST "$BASE_URL/$resource" \
    -H "Content-Type: application/json" \
    -d "$data" | jq
}

put_resource() {
  local resource=$1
  local data=$2
  curl -X PUT "$BASE_URL/$resource" \
    -H "Content-Type: application/json" \
    -d "$data"
}

patch_resource() {
  local resource=$1
  local data=$2
  curl -X PATCH "$BASE_URL/$resource" \
    -H "Content-Type: application/json" \
    -d "$data"
}

students_post='[
  {
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
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice.smith@example.com",
    "address": "456 Oak Ave",
    "city": "Springfield",
    "province": "BC",
    "country": "Canada",
    "address_type": "permanent",
    "is_international": 0,
    "program_id": 2
  }
]'

students_put='[
  {
    "id": 1,
    "status": "inactive",
    "coop": 0
  },
  {
    "id": 2,
    "status": "inactive",
    "coop": 0
  }
]'


students_patch='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'


instructors_post='[
  {
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "janesmith@example.com",
    "address": "789 Elm St",
    "province": "BC",
    "employment": "full-time",
    "status": "active",
    "department_id": 1
  },
  {
    "first_name": "Bob",
    "last_name": "Brown",
    "email": "bob.brown@example.com",
    "address": "321 Pine St",
    "province": "AB",
    "employment": "part-time",
    "status": "active",
    "department_id": 2
  }
]'

instructors_patch='{
  "ids": [1, 2],
  "status": "inactive",
  "updated_at": "2025-07-20"
}'

departments_post='[
  {
    "name": "Computer Science"
  },
  {
    "name": "Mathematics"
  }
]'

departments_patch='{
  "ids": [1, 2],
  "is_archived": 1,
  "updated_at": "2025-07-20"
}'

programs_post='[
  {
    "name": "Software Engineering",
    "type": "bachelor",
    "department_id": 1
  },
  {
    "name": "Data Science",
    "type": "certificate",
    "department_id": 2
  }
]'

programs_patch='{
  "ids": [1, 2],
  "is_archived": 1,
  "updated_at": "2025-07-20"
}'

courses_post='[
  {
    "title": "Intro to Programming",
    "code": "CS101",
    "term_id": 1,
    "department_id": 1
  },
  {
    "title": "Data Structures",
    "code": "CS102",
    "term_id": 1,
    "department_id": 1
  }
]'

courses_patch='{
  "ids": [1, 2],
  "is_archived": 1,
  "updated_at": "2025-07-20"
}'

terms_post='[
  {
    "name": "Fall 2025",
    "start_date": "2025-09-01",
    "end_date": "2025-12-15"
  },
  {
    "name": "Winter 2026",
    "start_date": "2026-01-05",
    "end_date": "2026-04-20"
  }
]'

terms_patch='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'

enrollments_post='[
  {
    "student_id": 1,
    "course_id": 1,
    "grade": "A"
  },
  {
    "student_id": 2,
    "course_id": 2,
    "grade": "B+"
  }
]'

enrollments_patch='{
  "ids": [1, 2],
  "grade": "A-",
  "updated_at": "2025-07-20"
}'

assignments_post='[
  {
    "instructor_id": 1,
    "course_id": 1
  },
  {
    "instructor_id": 2,
    "course_id": 2
  }
]'

assignments_patch='{
  "ids": [1, 2],
  "is_archived": 1,
  "updated_at": "2025-07-20"
}'

course_schedule_post='[
  {
    "course_id": 1,
    "day": "Monday",
    "time": "10:00-12:00",
    "room": "Room 101"
  },
  {
    "course_id": 2,
    "day": "Wednesday",
    "time": "14:00-16:00",
    "room": "Room 202"
  }
]'

course_schedule_patch='{
  "ids": [1, 2],
  "is_archived": 1,
  "updated_at": "2025-07-20"
}'

usage() {
  echo "Usage: $0 {read|create|update|archive} resource [id]"
  echo "Example: $0 read students"
  echo "Example: $0 read students 1"
  echo "Example: $0 create students students_post"
  echo "Example: $0 update students students_put"
  echo "Example: $0 archive students students_patch"
  exit 1
}

# Check at least 2 args
if [ $# -lt 2 ]; then
  usage
fi

method=$1
resource=$2
id=$3
keyword=$4

case "$method" in
  read)
    get_resource "$resource" "$id" "$keyword"
    ;;
  create)
    var_name="${resource}_post"
    data="${!var_name}"
    if [ -z "$data" ]; then
      echo "No POST data defined for resource '$resource'"
      exit 1
    fi
    post_resource "$resource" "$data"
    ;;
  update)
    var_name="${resource}_put"
    data="${!var_name}"
    if [ -z "$data" ]; then
      echo "No PUT data defined for resource '$resource'"
      exit 1
    fi
    put_resource "$resource" "$data"
    ;;
  archive)
    var_name="${resource}_patch"
    data="${!var_name}"
    if [ -z "$data" ]; then
      echo "No PATCH data defined for resource '$resource'"
      exit 1
    fi
    patch_resource "$resource" "$data"
    ;;
  *)
    usage
    ;;
esac
