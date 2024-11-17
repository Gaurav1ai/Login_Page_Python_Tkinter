import tkinter as tk
from tkinter import messagebox
import json
import os

# File path for JSON storage
DATA_FILE = "users.json"

# Ensure the JSON file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# Backend API Functions
def load_users():
    """Load user data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    """Save user data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    """Register a new user."""
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = password
    save_users(users)
    return True, "Registration successful!"

def login_user(username, password):
    """Authenticate user."""
    users = load_users()
    if username in users and users[username] == password:
        return True, "Login successful!"
    return False, "Invalid username or password."

# GUI Implementation
def sign_up():
    """Handle user registration."""
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    success, message = register_user(username, password)
    if success:
        messagebox.showinfo("Success", message)
        switch_to_login()
    else:
        messagebox.showerror("Error", message)

def log_in():
    """Handle user login."""
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    success, message = login_user(username, password)
    if success:
        messagebox.showinfo("Success", message)
    else:
        messagebox.showerror("Error", message)

def switch_to_login():
    """Switch to login screen."""
    title_label.config(text="Login")
    submit_button.config(text="Login", command=log_in)
    switch_button.config(text="Don't have an account? Sign Up", command=switch_to_sign_up)

def switch_to_sign_up():
    """Switch to sign-up screen."""
    title_label.config(text="Sign Up")
    submit_button.config(text="Sign Up", command=sign_up)
    switch_button.config(text="Already have an account? Login", command=switch_to_login)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Login/Sign Up")
root.geometry("300x200")
root.resizable(False, False)

# Widgets
title_label = tk.Label(root, text="Login", font=("Arial", 16))
title_label.pack(pady=10)

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

submit_button = tk.Button(root, text="Login", command=log_in)
submit_button.pack(pady=10)

switch_button = tk.Button(root, text="Don't have an account? Sign Up", command=switch_to_sign_up)
switch_button.pack()

# Run the Tkinter loop
root.mainloop()
