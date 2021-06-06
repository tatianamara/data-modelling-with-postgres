import psycopg2
from sql_queries import create_table_queries, drop_table_queries, files
import os

def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    except psycopg2.Error as e: 
        print("Error: Could not make connection to the Postgres database")
        print(e)
    
    conn.set_session(autocommit=True)
    
    try: 
        cur = conn.cursor()
    except psycopg2.Error as e: 
        print("Error: Could not get curser to the Database")
        print(e)
    
    # create sparkify database with UTF8 encoding
    try: 
        cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    except psycopg2.Error as e: 
        print("Error: Issue dropping database")
        print(e)
    
    try:
        cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")
    except psycopg2.Error as e: 
        print("Error: Issue creating database")
        print(e)
    
    # close connection to default database
    conn.close()    
    
    # connect to sparkify database
    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    except psycopg2.Error as e: 
        print("Error: Could not make connection to the Postgres database")
        print(e)
    
    try: 
        cur = conn.cursor()
    except psycopg2.Error as e: 
        print("Error: Could not get curser to the Database")
        print(e)
    
    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    Args:
        cur: database cursor.
        conn: database cunnection.   
    """
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables dropped succesfuly")
    except psycopg2.Error as e:
        print("Error dropping tables")
        print(e)

def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    Args:
        cur: database cursor.
        conn: database cunnection.
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()    
        print("Tables created succesfuly")
    except psycopg2.Error as e:
        print("Error creating tables")
        print(e)

def delete_csv_files():
    """
    Delete each csv file using the filepath in `files` list. 
    """
    # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
    for filePath in files:
        if os.path.exists(filePath):
            os.remove(filePath)
        else:
            print(f"Can not delete the file {filePath} as it doesn't exists")
        
def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)
    delete_csv_files()
    conn.close()


if __name__ == "__main__":
    main()