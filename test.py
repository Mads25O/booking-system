# from Crypto.Util.Padding import pad, unpad
# from Crypto.Cipher import AES
# from Crypto.Random import get_random_bytes

# data = b'Unaligned'   # 9 bytes
# key = b'\xb1\x84\xa6\xe8\x93Jk\xdb\xb5|\xf3{\xa4\x98\x07G#w!\x82\xe8\xb3c\x11$\xeb\x10\x15\xaa?W('
# iv = b'\xc1\xd6\n\xd3v\xdae$\xb2\xbd\x17\x8e\xe1\xc4\x1e\xd9'
# print(f'Key: {key}')
# print(f'IV: {iv}')

# # cipher1 = AES.new(key, AES.MODE_CBC, iv)
# # ct = cipher1.encrypt(pad(data, 16))
# # print(ct)

# encrypted = b'\x8e.\xc2\x83tV\xa3H\x00#\xdd84\xdden\xbd\xc8\xa3\xb6\xbf3\x92\xf0H\x1e\xc2t\x17\xd7\t\x9b'

# cipher2 = AES.new(key, AES.MODE_CBC, iv)
# pt = unpad(cipher2.decrypt(encrypted), 16)
# print(pt)

# assert(data == pt)

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

# Din krypterede tekst
encrypted = b'\x8e.\xc2\x83tV\xa3H\x00#\xdd84\xdden\xbd\xc8\xa3\xb6\xbf3\x92\xf0H\x1e\xc2t\x17\xd7\t\x9b'

key = b'\xb1\x84\xa6\xe8\x93Jk\xdb\xb5|\xf3{\xa4\x98\x07G#w!\x82\xe8\xb3c\x11$\xeb\x10\x15\xaa?W('
iv = b'\xc1\xd6\n\xd3v\xdae$\xb2\xbd\x17\x8e\xe1\xc4\x1e\xd9'

# Dekryptering
cipher = AES.new(key, AES.MODE_CBC, iv)

# Først dekrypterer vi, og derefter fjerner vi padding (mellemrum) manuelt
decrypted = cipher.decrypt(encrypted)

# Fjern padding (mellemrum)
decrypted_str = decrypted.decode('utf-8').rstrip(' ')

print(f'Decrypted: {decrypted_str}')