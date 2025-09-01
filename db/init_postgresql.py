#!/usr/bin/env python3
"""
PostgreSQL Database Initialization Script
This script initializes the PostgreSQL database with the schema and sample data.
"""
import os
import sys
sys.path.append('.')

from db.database import Database

def init_postgresql_database():
    """Initialize PostgreSQL database with schema"""
    print("Initializing PostgreSQL database...")
    
    # Set environment for PostgreSQL
    os.environ['DATABASE_TYPE'] = 'postgresql'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '5432'
    os.environ['DB_NAME'] = 'school'
    os.environ['DB_USER'] = 'schooluser'
    os.environ['DB_PASSWORD'] = 'schoolpass'
    
    try:
        db = Database()
        
        # Read and execute PostgreSQL schema
        with open('db/schema_postgresql.sql', 'r') as f:
            schema_sql = f.read()
        
        # Execute the schema
        db.execute_script(schema_sql)
        print("✅ PostgreSQL schema created successfully!")
        
        # Verify tables were created
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """
        
        tables = db.execute_query(tables_query)
        print(f"\n📋 Created tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing PostgreSQL database: {e}")
        return False

def populate_sample_data():
    """Populate PostgreSQL database with sample data"""
    print("\n🌱 Populating sample data...")
    
    try:
        db = Database()
        
        # Sample departments
        departments_data = [
            ("Computer Science",),
            ("Mathematics",),
            ("Engineering",),
        ]
        
        db.execute_many(
            "INSERT INTO departments (name) VALUES (%s)",
            departments_data
        )
        
        # Sample programs
        programs_data = [
            ("Bachelor of Computer Science", "bachelor", 1),
            ("Diploma in Software Development", "diploma", 1),
            ("Certificate in Web Development", "certificate", 1),
        ]
        
        db.execute_many(
            "INSERT INTO programs (name, type, department_id) VALUES (%s, %s, %s)",
            programs_data
        )
        
        # Sample terms
        terms_data = [
            ("Fall 2024", "2024-09-01", "2024-12-15"),
            ("Winter 2025", "2025-01-06", "2025-04-30"),
            ("Summer 2025", "2025-05-01", "2025-08-31"),
        ]
        
        db.execute_many(
            "INSERT INTO terms (name, start_date, end_date) VALUES (%s, %s, %s)",
            terms_data
        )
        
        print("✅ Sample data populated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error populating sample data: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL Database Setup")
    print("=" * 40)
    
    # Initialize schema
    schema_ok = init_postgresql_database()
    
    if schema_ok:
        # Populate sample data
        data_ok = populate_sample_data()
        
        if data_ok:
            print("\n🎉 PostgreSQL database setup complete!")
            sys.exit(0)
        else:
            print("\n⚠️  Schema created but sample data failed")
            sys.exit(1)
    else:
        print("\n❌ Database initialization failed")
        sys.exit(1)
