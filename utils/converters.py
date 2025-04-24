def student_row_to_dict(student):
  return {
    "id": student[0],
    "first_name": student[1],
    "last_name": student[2],
    "email": student[3],
    "address": student[4],
    "province": student[5],
    "country": student[6],
    "address_type": student[7],
    "status": student[8],
    "coop": student[9],
    "is_international": student[10],
    "program_id": student[11],
    "created_at": student[12],
    "updated_at": student[13],
    "is_archived": student[14],
  }