import hashlib

def encrypt(password):
    hash = hashlib.sha256(password.encode()).hexdigest()
    return hash

a = encrypt("siddharth18")

print(a)
    
    