import uuid
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# Function to get device ID (example)
def get_device_id():
    # Example device ID, replace with actual logic to get device ID
    return "106C677B-6FDB-4A3E-8503-DBF00E1F76A7"

# Generate a unique identifier (license key)
def generate_license_key():
    unique_id = str(uuid.uuid4())
    return unique_id.upper()  # Convert to uppercase

# Add start and expiry dates to the license key
def generate_license_dates(period_days):
    start_date = datetime.today()
    expiry_date = start_date + timedelta(days=period_days)
    return start_date, expiry_date

# Encrypt the license key
def encrypt_license_key(key):
    key = key.encode()
    cipher_suite = Fernet.generate_key()
    cipher = Fernet(cipher_suite)
    encrypted_key = cipher.encrypt(key)
    return encrypted_key, cipher_suite

# Decrypt the license key
def decrypt_license_key(encrypted_key, cipher_suite):
    cipher = Fernet(cipher_suite)
    decrypted_key = cipher.decrypt(encrypted_key)
    return decrypted_key.decode()

# Example validation function
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
                    print(f"License key is valid. {remaining_days} days left until expiry.")
                    return True
                else:
                    print("Device ID mismatch.")
                    return False
            else:
                print("License key has expired.")
                return False
        else:
            print("License key mismatch.")
            return False
    
    except Exception as e:
        print(f"Validation error: {e}")
        return False

# Example usage
license_key = generate_license_key()
period_days = 30  # Period of 4 days
start_date, expiry_date = generate_license_dates(period_days)
device_id = get_device_id()
encrypted_key, cipher_suite = encrypt_license_key(license_key)

print(f"License Key: {license_key}")
print(f"Start Date: {start_date}")
print(f"Expiry Date: {expiry_date}")
print(f"Device ID: {device_id}")
print(f"Encrypted Key: {encrypted_key}")

# Example validation
valid = validate_license_key(license_key, start_date, expiry_date, device_id, encrypted_key, cipher_suite)
print(f"Is Valid: {valid}")
