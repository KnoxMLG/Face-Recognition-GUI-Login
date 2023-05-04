import win32crypt

# Define the encrypted data and entropy
encrypted_data = b'...encrypted data...'
encrypted_data2 = b'...encrypted data...'
# Decrypt the data
decrypted_data = win32crypt.CryptProtectData(encrypted_data, None, None, None, None, 0)
decrypted_data2 = win32crypt.CryptProtectData(encrypted_data2, None, None, None, None, 0)

if (decrypted_data2==decrypted_data2):
    print(True)
