import sqlite3
import tkinter as tk
from tkinter import messagebox

# Initialize database connection
# Using ":memory:" to create an in-memory database
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

# Create a table in the in-memory database
cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    info TEXT NOT NULL
)
''')
conn.commit()

# Define the entry variable globally to be used inside functions
entry = None

# Function to save data
def save_data():
    global entry
    info = entry.get()
    if info:
        cursor.execute('INSERT INTO data (info) VALUES (?)', (info,))
        conn.commit()
        entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Data saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter some data.")

# Function to retrieve data
def retrieve_data():
    cursor.execute('SELECT * FROM data')
    rows = cursor.fetchall()
    result = "\n".join([f"ID: {row[0]}, Info: {row[1]}" for row in rows])
    if result:
        messagebox.showinfo("Retrieved Data", result)
    else:
        messagebox.showinfo("No Data", "No data found in the database.")

def main():
    global entry
    # Set up the main application window
    app = tk.Tk()
    app.title("In-Memory Database App")
    app.geometry("400x200")

    # Create UI elements
    label = tk.Label(app, text="Enter some data:")
    label.pack(pady=10)

    entry = tk.Entry(app, width=30)
    entry.pack(pady=5)

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
