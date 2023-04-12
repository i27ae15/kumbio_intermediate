import psycopg2
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from print_pp.logging import Print

# Database connection details
source_db = {
    "host": "167.235.147.49",
    "dbname": "dk",
    "user": "dkuser",
    "password": "arPDxC47p5Ke",
}

target_db = {
    "host": "localhost",
    "dbname": "intermediate",
    "user": "postgres",
    "password": "1234",
}

errors = 0

# Connect to the source and target databases
source_conn = psycopg2.connect(**source_db)
target_conn = psycopg2.connect(**target_db)

# Retrieve the list of tables in the source database
with source_conn.cursor() as source_cur:
    source_cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = [row[0] for row in source_cur.fetchall()]

# Copy data for each table from the source to the target database

for table in tables:
    with source_conn.cursor() as source_cur:
        # Get table structure
        try:
            source_cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
            columns = [row[0] for row in source_cur.fetchall()]
            columns_str = ', '.join(columns)

            # Copy the data from the source to the target database
            with target_conn.cursor() as target_cur:
                # Create the table in the target database if it doesn't exist
                target_cur.execute(f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM {table} WITH NO DATA;")
                target_conn.commit()

                # Copy data from source to target
                try:
                    source_cur.execute(f"SELECT {columns_str} FROM {table};")
                    for row in source_cur.fetchall():
                        values = ', '.join(f'%s' for _ in row)
                        try:
                            target_cur.execute(f"INSERT INTO {table} ({columns_str}) VALUES ({values});", row)
                        except UniqueViolation as e:
                            errors += 1
                            target_conn.rollback()
                            print(f"Skipped a row in table '{table}' due to unique constraint violation: {e}")
                        except ForeignKeyViolation as e:
                            target_conn.rollback()
                            print(f"Skipped a row in table '{table}' due to foreign key constraint violation: {e}")
                            errors += 1
                        except Exception as e:
                            target_conn.rollback()
                            print(f"Skipped a row in table '{table}' due to an unknown error: {e}")
                            errors += 1
                        else:
                            try:
                                target_conn.commit()
                            except Exception as e:
                                target_conn.rollback()
                                print(f"Skipped a row in table '{table}' due to an unknown error: {e}")
                                errors += 1
                except Exception as e:
                    print(f"Skipped table '{table}' due to an unknown error: {e}")
                    errors += 1
        except Exception as e:
            print(f"Skipped table '{table}' due to an unknown error: {e}")
            errors += 1


# Close the database connections
source_conn.close()
target_conn.close()

Print('errors', errors)
