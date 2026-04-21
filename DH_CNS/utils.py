import random

p = 23
g = 5

def generate_private_key():
    return random.randint(1, 10)

def generate_public_key(private_key):
    return pow(g, private_key, p)

def generate_shared_key(other_public, private_key):
    return pow(other_public, private_key, p)

def encrypt(msg, key):
    return ''.join(chr(ord(c) ^ key) for c in msg)

def decrypt(msg, key):
    return encrypt(msg, key)

def validate_message(msg):
    if not msg.strip():
        return "error", "⚠ Empty message not allowed"
    return "ok", None