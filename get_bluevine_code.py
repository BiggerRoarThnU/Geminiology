import hmac
import hashlib
import time
import struct
import base64

def get_totp_token(secret):
    # Ensure the secret is in the correct format (remove spaces and uppercase)
    secret = secret.replace(' ', '').upper()
    
    # Bluevine/Google Authenticator use base32
    # Add padding if necessary
    missing_padding = len(secret) % 8
    if missing_padding != 0:
        secret += '=' * (8 - missing_padding)
        
    key = base64.b32decode(secret)
    
    # Standard TOTP is based on 30-second intervals
    msg = struct.pack(">Q", int(time.time()) // 30)
    
    # Generate the HMAC-SHA1 hash
    h = hmac.new(key, msg, hashlib.sha1).digest()
    
    # Perform dynamic truncation
    offset = h[19] & 0xf
    code = (struct.unpack(">I", h[offset:offset+4])[0] & 0x7fffffff) % 1000000
    
    return '{:06d}'.format(code)

if __name__ == "__main__":
    # The Bluevine Secret provided
    secret_key = "xspkxzppvm6qumx5hry46tz3"
    print(f"VERIFICATION_CODE: {get_totp_token(secret_key)}")
