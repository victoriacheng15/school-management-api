#!/usr/bin/env python3
"""
Test PostgreSQL compatibility for updated models
"""

import os
import sys

sys.path.append(".")

from app.models.student import (
    student_db_read_all,
    student_db_insert,
    student_db_read_by_id,
    student_db_update,
    student_db_archive,
)


def test_student_model_postgresql():
    """Test student model with PostgreSQL"""
    print("Testing Student Model with PostgreSQL...")

    # Set environment for PostgreSQL
    os.environ["DATABASE_TYPE"] = "postgresql"
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_NAME"] = "school"
    os.environ["DB_USER"] = "schooluser"
    os.environ["DB_PASSWORD"] = "schoolpass"

    try:
        # Test read all
        print("📋 Testing read all students...")
        students = student_db_read_all()
        print(f"✅ Found {len(students)} students")

        # Test insert
        print("➕ Testing insert student...")
        student_data = (
            "John",
            "Doe",
            "john.doe@example.com",
            "123 Main St",
            "Toronto",
            "ON",
            "Canada",
            "local",
            "active",
            False,
            False,
            1,  # program_id = 1
        )

        new_id = student_db_insert(student_data)
        print(f"✅ Inserted student with ID: {new_id}")

        if new_id:
            # Test read by id
            print(f"🔍 Testing read student by ID {new_id}...")
            student = student_db_read_by_id(new_id)
            print(f"✅ Found student: {student['first_name']} {student['last_name']}")

            # Test update
            print(f"✏️ Testing update student ID {new_id}...")
            updated_data = (
                "John",
                "Smith",
                "john.smith@example.com",
                "456 Oak St",
                "Vancouver",
                "BC",
                "Canada",
                "local",
                "active",
                True,
                False,
                1,
            )
            updated_count = student_db_update(new_id, updated_data)
            print(f"✅ Updated {updated_count} student(s)")

            # Test archive
            print(f"🗄️ Testing archive student ID {new_id}...")
            archived_count = student_db_archive(new_id)
            print(f"✅ Archived {archived_count} student(s)")

        print("\n🎉 All student model tests passed!")
        return True

    except Exception as e:
        print(f"❌ Student model test failed: {e}")
        return False


if __name__ == "__main__":
    print("PostgreSQL Model Compatibility Test")
    print("=" * 40)

    success = test_student_model_postgresql()

    if success:
        print("\n✅ Model compatibility test passed!")
        sys.exit(0)
    else:
        print("\n❌ Model compatibility test failed!")
        sys.exit(1)
