import psycopg2
import psycopg2.extras

# Connect to the PostgreSQL database
def connect_to_database():
    connection = psycopg2.connect(
        host="your-host",
        database="your-database",
        user="your-user",
        password="your-password"
    )
    return connection

# Create the database table
def create_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    create_table_query = '''
        CREATE TABLE IF NOT EXISTS used_invoices (
            r_hash VARCHAR(64) PRIMARY KEY,
            used BOOLEAN NOT NULL DEFAULT FALSE
        )
    '''

    cursor.execute(create_table_query)
    connection.commit()

    cursor.close()
    connection.close()

# Set 'used' to True if r_hash matches any value in the database
def set_used(r_hash):
    connection = connect_to_database()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    select_query = '''
        SELECT r_hash FROM your_table_name WHERE r_hash = %(r_hash)s
    '''
    cursor.execute(select_query, {'r_hash': r_hash})

    if cursor.rowcount > 0:
        update_query = '''
            UPDATE your_table_name SET used = TRUE WHERE r_hash = %(r_hash)s
        '''
        cursor.execute(update_query, {'r_hash': r_hash})
        connection.commit()

    cursor.close()
    connection.close()