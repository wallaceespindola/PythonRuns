"""
Instructions:

You'll need to set up a connection to a PostgreSQL database before running the app.

Prerequisites:
Python 3.x installed.
Tkinter (comes with Python).
psycopg2 package to connect Python with PostgreSQL.

Install it using:
pip install psycopg2

PostgreSQL installed and running on your machine. You’ll need a database to connect to.

Database Setup
Make sure you have a PostgreSQL database created and a user with the necessary permissions.

Below is a basic setup command. Log into PostgreSQL:
psql -U postgres

Create a database and user:

CREATE DATABASE testdb;
CREATE USER testuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;
"""

import tkinter as tk
from tkinter import messagebox

import psycopg2

# Database connection settings
DB_NAME = "testdb"
DB_USER = "testuser"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"


def connectDB():
    # Initialize database connection
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS data (
            id SERIAL PRIMARY KEY,
            info TEXT NOT NULL
        )
        """
        )
        conn.commit()
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        exit(1)


# Function to save data
def save_data():
    info = entry.get()
    if info:
        try:
            cursor.execute("INSERT INTO data (info) VALUES (%s)", (info,))
            conn.commit()
            entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
    else:
        messagebox.showwarning("Warning", "Please enter some data.")


# Function to retrieve data
def retrieve_data():
    try:
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        result = "\n".join([f"ID: {row[0]}, Info: {row[1]}" for row in rows])
        if result:
            messagebox.showinfo("Retrieved Data", result)
        else:
            messagebox.showinfo("No Data", "No data found in the database.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve data: {e}")


def main():
    # Set up the main application window
    app = tk.Tk()
    app.title("PostgreSQL Database App")
    app.geometry("400x200")

    # Create UI elements
    label = tk.Label(app, text="Enter some data:")
    label.pack(pady=10)

    entry = tk.Entry(app, width=30)
    entry.pack(pady=5)

    db_button = tk.Button(app, text="Connect DB", command=connectDB)
    db_button.pack(pady=5)

    save_button = tk.Button(app, text="Save Data", command=save_data)
    save_button.pack(pady=5)

    retrieve_button = tk.Button(app, text="Retrieve Data", command=retrieve_data)
    retrieve_button.pack(pady=5)

    # Start the application
    app.mainloop()

    # Close database connection when the app is closed
    conn.close()


if __name__ == "__main__":
    main()
