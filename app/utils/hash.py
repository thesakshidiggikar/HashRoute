import string

# Standard Base62 alphabet
ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode_base62(num: int) -> str:
    """Encodes an integer into a Base62 string."""
    if num == 0:
        return ALPHABET[0]
    
    arr = []
    base = len(ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(ALPHABET[rem])
    
    arr.reverse()
    return "".join(arr)

def decode_base62(string: str) -> int:
    """Decodes a Base62 string into an integer."""
    base = len(ALPHABET)
    num = 0
    for char in string:
        num = num * base + ALPHABET.index(char)
    return num

import hashlib

def generate_short_code(url: str, salt: str = "") -> str:
    """
    Generates a unique short code based on URL hash.
    Using MD5 for speed and consistent length, then taking a slice.
    """
    hash_object = hashlib.md5((url + salt).encode())
    # Convert hex digest to integer, then encode to Base62
    hash_int = int(hash_object.hexdigest(), 16)
    # Return first 7 characters of Base62 representation for a good balance of uniqueness/length
    return encode_base62(hash_int)[:7]
