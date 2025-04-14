import psycopg2
import csv
from config import load_config as config

def create_table():
    command = '''
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
    )
    '''
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cur:
            cur.execute(command)
            conn.commit()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    sql = "INSERT INTO phonebook (name, phone) VALUES (%s, %s)"
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, phone))
            conn.commit()

def insert_from_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        with psycopg2.connect(**config()) as conn:
            with conn.cursor() as cur:
                for row in reader:
                    print(f"Inserting row: {row}")  
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
                conn.commit()
                print("✅ Done inserting from CSV!")


def update_data():
    name = input("Enter the name to update: ")
    new_phone = input("Enter the new phone number: ")
    sql = "UPDATE phonebook SET phone = %s WHERE name = %s"
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (new_phone, name))
            conn.commit()

def query_by_name_prefix():
    prefix = input("Enter name prefix to search: ")
    sql = "SELECT * FROM phonebook WHERE name LIKE %s"
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (prefix + '%',))
            rows = cur.fetchall()
            for row in rows:
                print(row)

def delete_by_name():
    name = input("Enter the name to delete: ")
    sql = "DELETE FROM phonebook WHERE name = %s"
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name,))
            conn.commit()

def show_all():
    sql = "SELECT * FROM phonebook"
    with psycopg2.connect(**config()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            print("\n📞 All Contacts:")
            for row in rows:
                print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")


def main():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update phone by name")
        print("4. Query by name prefix")
        print("5. Delete by name")
        print("0. Exit")
        print("6. Show all records")  


        choice = input("Choose an option: ")

        if choice == '1':
            insert_from_console()
        elif choice == '2':
            filename = input("Enter CSV file path: ")
            insert_from_csv(filename)
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_by_name_prefix()
        elif choice == '5':
            delete_by_name()
        elif choice == '6':
            show_all()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
