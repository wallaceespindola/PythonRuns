import json
import tkinter as tk
from tkinter import messagebox

# In-memory JSON-like storage
data_store = {"data": []}  # Simulating a JSON file structure


# Function to save data to the "JSON file"
def save_data():
    info = entry.get()
    if info:
        # Append new data to the in-memory data store
        data_store["data"].append({"id": len(data_store["data"]) + 1, "info": info})

        # Persist data as a JSON string (simulating file saving)
        persist_data()

        entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Data saved successfully!")
    else:
        messagebox.showwarning("Warning", "Please enter some data.")


# Function to persist data as JSON (simulating saving to a file)
def persist_data():
    # Convert the data_store to a JSON string (you could save it to a file if needed)
    json_data = json.dumps(data_store)
    # Simulate saving this JSON string to a file (e.g., write to disk if needed)
    # Here, we'll just print it to show persistence
    print("Persisted JSON Data:", json_data)


# Function to retrieve data
def retrieve_data():
    # Read data from the in-memory JSON structure (simulating reading from a file)
    if data_store["data"]:
        result = "\n".join([f"ID: {item['id']}, Info: {item['info']}" for item in data_store["data"]])
        messagebox.showinfo("Retrieved Data", result)
    else:
        messagebox.showinfo("No Data", "No data found in the JSON file.")


# Main application setup
def main():
    global entry
    # Set up the main application window
    app = tk.Tk()
    app.title("In-Memory JSON App")
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


if __name__ == "__main__":
    main()
