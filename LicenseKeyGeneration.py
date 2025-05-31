import uuid
import random
import string
import hashlib
from datetime import datetime, timedelta

def get_device_id():
    device_id = hex(uuid.getnode())
    return device_id.upper()

def generate_license_key(period_days):
    device_id = get_device_id()
    expiry_date = (datetime.now() + timedelta(days=period_days)).strftime('%Y-%m-%d')
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    combined = f"{device_id}-{expiry_date}-{key}"
    checksum = hashlib.sha256(combined.encode()).hexdigest().upper()[:8]
    license_key = f"{combined}-{checksum}"
    return license_key

def validate_license_key(license_key):
    try:
        device_id, expiry_date, key, checksum = license_key.split('-')
        if device_id != get_device_id():
            return False
        if datetime.now() > datetime.strptime(expiry_date, '%Y-%m-%d'):
            return False
        combined = f"{device_id}-{expiry_date}-{key}"
        expected_checksum = hashlib.sha256(combined.encode()).hexdigest().upper()[:8]
        if checksum != expected_checksum:
            return False
        return True
    except ValueError:
        return False

# Generate a new license key
license_key = generate_license_key(30)
print(f"Generated License Key: {license_key}")

# Validate the generated license key
is_valid = validate_license_key(license_key)
print(f"License Key Valid: {is_valid}")
