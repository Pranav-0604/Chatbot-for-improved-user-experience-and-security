import tkinter as tk
from tkinter import messagebox
import random
import subprocess

# User credentials (for testing)
correct_username = "admin"
correct_password = "password"

# Function to generate a random captcha
def generate_captcha():
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    captcha = ''.join(random.choice(chars) for _ in range(6))
    return captcha

# Function to validate the login details
def validate_login():
    username = entry_username.get()
    password = entry_password.get()
    entered_captcha = entry_captcha.get()

    if username != correct_username or password != correct_password:
        messagebox.showerror("Login Failed", "Invalid username or password")
    elif entered_captcha != captcha_label.cget("text"):
        messagebox.showerror("Captcha Error", "Captcha does not match")
        refresh_captcha()
    else:
        messagebox.showinfo("Login Success", "Login successful!")
        # Run chatbot.py file
        subprocess.run(["python", "./chatbot.py"])

# Function to refresh captcha
def refresh_captcha():
    new_captcha = generate_captcha()
    captcha_label.config(text=new_captcha)

# Function for forgot password
def forgot_password():
    email = entry_email.get()
    if email:
        messagebox.showinfo("Password Reset", "A password reset link has been sent to your mail id.")
    else:
        messagebox.showerror("Input Error", "Please enter your mail id.")

# Function to open forgot password window
def open_forgot_password_window():
    forgot_window = tk.Toplevel(root)
    forgot_window.title("Forgot Password")
    forgot_window.geometry("300x100")
    forgot_window.config(bg='light yellow')
    
    tk.Label(forgot_window, text="Enter your mail id:", bg='light yellow').pack(pady=5)
    
    global entry_email
    entry_email = tk.Entry(forgot_window)
    entry_email.pack(pady=5)

    submit_button = tk.Button(forgot_window, text="Submit", command=forgot_password)
    submit_button.pack(pady=5)

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("350x400")  # Increased the window height to 400
root.config(bg='light yellow')  # Set background color to light yellow

# Username label and entry field
tk.Label(root, text="Username:", bg='light yellow').pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# Password label and entry field
tk.Label(root, text="Password:", bg='light yellow').pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# Captcha label and entry field
captcha_label = tk.Label(root, text=generate_captcha(), font=("Helvetica", 14), bg='light yellow')
captcha_label.pack(pady=5)

tk.Label(root, text="Enter Captcha:", bg='light yellow').pack(pady=5)
entry_captcha = tk.Entry(root)
entry_captcha.pack(pady=5)

# Refresh captcha button
refresh_button = tk.Button(root, text="Refresh Captcha", command=refresh_captcha)
refresh_button.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=validate_login)
login_button.pack(pady=5)

# Forgot Password button
forgot_button = tk.Button(root, text="Forgot Password", command=open_forgot_password_window)
forgot_button.pack(pady=5)

# Start the GUI event loop
root.mainloop()
