#!/usr/bin/env python3
"""
Database Migration Utility
This script helps migrate data from SQLite to PostgreSQL
"""
import os
import sys
sys.path.append('.')

from db.database import Database

def migrate_sqlite_to_postgresql():
    """Migrate data from SQLite to PostgreSQL"""
    print("Migrating data from SQLite to PostgreSQL...")
    
    # First, check if SQLite database exists
    sqlite_db_path = "db/school.db"
    if not os.path.exists(sqlite_db_path):
        print("❌ SQLite database not found. No data to migrate.")
        return False
    
    try:
        # Create SQLite database instance
        os.environ['DATABASE_TYPE'] = 'sqlite'
        sqlite_db = Database()
        
        # Create PostgreSQL database instance
        os.environ['DATABASE_TYPE'] = 'postgresql'
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '5432'
        os.environ['DB_NAME'] = 'school'
        os.environ['DB_USER'] = 'schooluser'
        os.environ['DB_PASSWORD'] = 'schoolpass'
        pg_db = Database()
        
        # Define tables in dependency order
        tables = [
            'departments',
            'programs', 
            'students',
            'instructors',
            'terms',
            'courses',
            'enrollments',
            'assignments',
            'course_schedule'
        ]
        
        migration_success = True
        
        for table in tables:
            try:
                print(f"📋 Migrating {table}...")
                
                # Get data from SQLite
                sqlite_data = sqlite_db.execute_query(f"SELECT * FROM {table}")
                
                if not sqlite_data:
                    print(f"  ✅ {table}: No data to migrate")
                    continue
                
                # Clear existing data in PostgreSQL table
                pg_db.execute_query(f"DELETE FROM {table}")
                
                # Get column names (excluding id for SERIAL columns)
                columns = list(sqlite_data[0].keys())
                non_id_columns = [col for col in columns if col != 'id']
                
                # Prepare INSERT statement
                placeholders = ', '.join(['%s'] * len(non_id_columns))
                column_names = ', '.join(non_id_columns)
                insert_query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
                
                # Prepare data for insertion
                insert_data = []
                for row in sqlite_data:
                    row_data = tuple(row[col] for col in non_id_columns)
                    insert_data.append(row_data)
                
                # Insert data into PostgreSQL
                pg_db.execute_many(insert_query, insert_data)
                
                print(f"  ✅ {table}: Migrated {len(insert_data)} records")
                
            except Exception as e:
                print(f"  ❌ {table}: Migration failed - {e}")
                migration_success = False
        
        return migration_success
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def compare_data_counts():
    """Compare record counts between SQLite and PostgreSQL"""
    print("\n📊 Comparing data counts...")
    
    try:
        # SQLite counts
        os.environ['DATABASE_TYPE'] = 'sqlite'
        sqlite_db = Database()
        
        # PostgreSQL counts
        os.environ['DATABASE_TYPE'] = 'postgresql'
        pg_db = Database()
        
        tables = [
            'departments', 'programs', 'students', 'instructors', 
            'terms', 'courses', 'enrollments', 'assignments', 'course_schedule'
        ]
        
        print(f"{'Table':<15} {'SQLite':<10} {'PostgreSQL':<10} {'Status'}")
        print("-" * 50)
        
        for table in tables:
            try:
                sqlite_count = sqlite_db.execute_query(f"SELECT COUNT(*) as count FROM {table}")[0]['count']
                pg_count = pg_db.execute_query(f"SELECT COUNT(*) as count FROM {table}")[0]['count']
                
                status = "✅ Match" if sqlite_count == pg_count else "❌ Mismatch"
                print(f"{table:<15} {sqlite_count:<10} {pg_count:<10} {status}")
                
            except Exception as e:
                print(f"{table:<15} {'Error':<10} {'Error':<10} ❌ {e}")
        
    except Exception as e:
        print(f"Error comparing data: {e}")

if __name__ == "__main__":
    print("Database Migration Utility")
    print("=" * 40)
    
    migration_ok = migrate_sqlite_to_postgresql()
    
    if migration_ok:
        compare_data_counts()
        print("\n🎉 Migration completed successfully!")
    else:
        print("\n❌ Migration failed")
        sys.exit(1)
