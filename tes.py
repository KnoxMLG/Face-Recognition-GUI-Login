import win32crypt

# Define the encrypted data and entropy
encrypted_data = b'...encrypted data...'

# Decrypt the data
decrypted_data = win32crypt.CryptProtectData(encrypted_data, None, None, None, None, 0)

realdec = (win32crypt.CryptUnprotectData(decrypted_data, None)[1]).decode("utf-8")

print(realdec)
