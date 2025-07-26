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
    -d "$data" | jq
}

patch_resource() {
  local resource=$1
  local data=$2
  curl -X PATCH "$BASE_URL/$resource" \
    -H "Content-Type: application/json" \
    -d "$data" | jq
}

create_students='[
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

update_students='[
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

archive_students='{
  "ids": [3, 4]
}'

create_instructors='[
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

update_instructors='[
  { "id": 1, "status": "inactive" },
  { "id": 2, "status": "inactive" }
]'

archive_instructors='{
  "ids": [3, 4]
}'

create_departments='[
  {
    "name": "Computer Science"
  },
  {
    "name": "Mathematics"
  }
]'

archive_departments='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'

create_programs='[
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

archive_programs='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'

create_courses='[
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

archive_courses='{
  "ids": [1, 2],
  
  "updated_at": "2025-07-20"
}'

create_terms='[
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

archive_terms='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'

create_enrollments='[
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

archive_enrollments='{
  "ids": [1, 2],
  "grade": "A-",
  "updated_at": "2025-07-20"
}'

create_assignments='[
  {
    "instructor_id": 1,
    "course_id": 1
  },
  {
    "instructor_id": 2,
    "course_id": 2
  }
]'

archive_assignments='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'

create_course_schedule='[
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

archive_course_schedule='{
  "ids": [1, 2],
  "updated_at": "2025-07-20"
}'

usage() {
  echo "Usage: $0 {read|create|update|archive} resource [id] [keyword]"
  echo "Examples:"
  echo "  $0 read students"
  echo "  $0 read students 1"
  echo "  $0 read students  active"
  echo "  $0 create students create_students"
  echo "  $0 update students update_students"
  echo "  $0 archive students archive_students"
  exit 1
}

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
    var_name="create_${resource}"
    data="${!var_name}"
    if [ -z "$data" ]; then
      echo "No POST data defined for resource '$resource'"
      exit 1
    fi
    post_resource "$resource" "$data"
    ;;
  update)
    var_name="update_${resource}"
    data="${!var_name}"
    if [ -z "$data" ]; then
      echo "No PUT data defined for resource '$resource'"
      exit 1
    fi
    put_resource "$resource" "$data"
    ;;
  archive)
    var_name="archive_${resource}"
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
