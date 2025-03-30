def xor(data, key):
    # Make sure the key is a single character (e.g., a letter or number)
    key = ord(key)  # Convert the key to its ASCII value (int)
    
    # XOR each character with the key and return the result
    result = ''.join(chr(ord(char) ^ key) for char in data)
    
    return result
