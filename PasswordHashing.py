import hashlib

def hash_password(password):
    """Hash the password using SHA-256."""
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    return sha256.hexdigest()

def verify_password(stored_password_hash, provided_password):
    """Verify a provided password against the stored hash."""
    # Hash the provided password using the same method
    sha256 = hashlib.sha256()
    sha256.update(provided_password.encode("utf-8"))
    # Check if the newly hashed password matches the stored hash
    return sha256.hexdigest() == stored_password_hash
