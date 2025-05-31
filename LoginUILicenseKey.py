import uuid
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

# Function to generate a unique identifier (license key)
def generate_license_key():
    unique_id = str(uuid.uuid4())
    return unique_id.upper()  # Convert to uppercase

# Function to generate start and expiry dates for the license key
def generate_license_dates(period_days):
    start_date = datetime.today()
    expiry_date = start_date + timedelta(days=period_days)
    return start_date, expiry_date

# Function to encrypt the license key
def encrypt_license_key(key):
    key = key.encode()
    cipher_suite = Fernet.generate_key()
    cipher = Fernet(cipher_suite)
    encrypted_key = cipher.encrypt(key)
    return encrypted_key, cipher_suite

# Function to validate the license key
def validate_license_key(license_key, start_date, expiry_date, device_id, encrypted_key, cipher_suite):
    try:
        # Decrypt license key
        cipher = Fernet(cipher_suite)
        decrypted_key = cipher.decrypt(encrypted_key)
        decrypted_key = decrypted_key.decode()

        # Check license key validity
        if decrypted_key == license_key:
            today = datetime.today()
            if start_date <= today <= expiry_date:
                # Check device ID
                if get_device_id() == device_id:
                    # Calculate remaining days
                    remaining_days = (expiry_date - today).days
                    return True, remaining_days
                else:
                    return False, 0
            else:
                return False, 0
        else:
            return False, 0
    
    except Exception as e:
        print(f"Validation error: {e}")
        return False, 0

# Function to get device ID (example)
def get_device_id():
    # Example device ID, replace with actual logic to get device ID
    return "106C677B-6FDB-4A3E-8503-DBF00E1F76A7"

# Function to handle login button click event
def login():
    # Get user input
    license_key = license_key_entry.get()
    device_id = device_id_entry.get()

    # Example: Period of 30 days for the license key
    period_days = 30
    start_date, expiry_date = generate_license_dates(period_days)
    
    # Generate and encrypt license key
    encrypted_key, cipher_suite = encrypt_license_key(license_key)

    # Validate license key
    valid, remaining_days = validate_license_key(license_key, start_date, expiry_date, device_id, encrypted_key, cipher_suite)

    # Display dashboard if valid
    if valid:
        dashboard_window = Toplevel(root)
        dashboard_window.title("Dashboard")

        # Display information
        Label(dashboard_window, text=f"License Key: {license_key}").pack()
        Label(dashboard_window, text=f"Start Date: {start_date}").pack()
        Label(dashboard_window, text=f"Expiry Date: {expiry_date}").pack()
        Label(dashboard_window, text=f"Device ID: {device_id}").pack()
        Label(dashboard_window, text=f"Encrypted Key: {encrypted_key}").pack()
        Label(dashboard_window, text=f"License key is valid. {remaining_days} days left until expiry.").pack()

    else:
        messagebox.showerror("Error", "Invalid license key or device ID.")

# Main application window
root = Tk()
root.title("Login")

# License Key label and entry
Label(root, text="License Key:").pack()
license_key_entry = Entry(root, width=30)
license_key_entry.pack()

# Device ID label and entry
Label(root, text="Device ID:").pack()
device_id_entry = Entry(root, width=30)
device_id_entry.pack()

# Login button
login_button = Button(root, text="Login", command=login)
login_button.pack()

# Start the main loop
root.mainloop()
