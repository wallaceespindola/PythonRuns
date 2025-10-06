import json
import sqlite3
import tkinter as tk
from tkinter import messagebox

# Initialize the in-memory SQLite database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create a table to store JSON data
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS json_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL
)
"""
)
conn.commit()

# Initialize the JSON storage in the database (if empty)
initial_data = {"data": []}
cursor.execute("INSERT INTO json_data (data) VALUES (?)", (json.dumps(initial_data),))
conn.commit()


# Function to load JSON data from the database
def load_data_from_db():
    cursor.execute("SELECT data FROM json_data WHERE id = 1")
    row = cursor.fetchone()
    if row:
        return json.loads(row[0])
    else:
        return {"data": []}


# Function to save JSON data back to the database
def save_data_to_db(data):
    cursor.execute("UPDATE json_data SET data = ? WHERE id = 1", (json.dumps(data),))
    conn.commit()


# Function to save data to the "JSON database"
def save_data():
    global data_store
    info = entry.get()
    if info:
        # Load existing data from the database
        data_store = load_data_from_db()

        # Append new data to the in-memory data store
        data_store["data"].append({"id": len(data_store["data"]) + 1, "info": info})

        # Persist updated data back to the database
        save_data_to_db(data_store)

        entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Data saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter some data.")


# Function to retrieve data from the "JSON database"
def retrieve_data():
    data_store = load_data_from_db()
    if data_store["data"]:
        result = "\n".join([f"ID: {item['id']}, Info: {item['info']}" for item in data_store["data"]])
        messagebox.showinfo("Retrieved Data", result)
    else:
        messagebox.showinfo("No Data", "No data found in the database.")


# Function to view the raw JSON data stored in the database
def view_db_data():
    # Directly query the raw JSON data from the table and print it
    cursor.execute("SELECT * FROM json_data")
    rows = cursor.fetchall()
    print("Database Content:")
    for row in rows:
        print(f"ID: {row[0]}, Data: {row[1]}")  # Print each row in the console


# Main application setup
def main():
    global entry
    # Set up the main application window
    app = tk.Tk()
    app.title("In-Memory JSON DB App")
    app.geometry("400x300")

    # Create UI elements
    label = tk.Label(app, text="Enter some data:")
    label.pack(pady=10)

    entry = tk.Entry(app, width=30)
    entry.pack(pady=5)

    save_button = tk.Button(app, text="Save Data", command=save_data)
    save_button.pack(pady=5)

    retrieve_button = tk.Button(app, text="Retrieve Data", command=retrieve_data)
    retrieve_button.pack(pady=5)

    # Button to view the raw JSON data in the console
    view_button = tk.Button(app, text="View DB Data in Console", command=view_db_data)
    view_button.pack(pady=5)

    # Start the application
    app.mainloop()

    # Close database connection when the app is closed
    conn.close()


if __name__ == "__main__":
    main()
