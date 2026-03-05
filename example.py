### METODO 1 -> Library
import pyotp # Intalar no terminal

#1.  Gerando uma chave secreta

secret = pyotp.random_base32()
print(f"Secret: {secret}")

totp = pyotp.TOTP(secret)

# Gerando o codigo
current_code = totp.now()
print("Current OTP Code", current_code)

# Verificação
print(totp.verify(current_code))

shared_secret = "Executar o codigo todo antes, e pegar o OTP no terminal"

### metodo 2 -> Pure python
import time
import hashlib
import struct
import base64
import hmac

def get_totp_token(secret):
    missing_padding = len(secret) % 8
    if missing_padding:
    secret += "=" * (8 - missing_padding)

    key = base64.b32decode(secret, casefold=True)
    print("key", key)

    interval_no = int(time.time()//3-)
    counter = struct.pack(">Q", interval_no)
    print("Counter: {counter}")


    # HMACH Hash
    hmac_hash = hmac.new(key, counter, hashlib.sha1).digest()
    print(f"Hmac: {hmac_hash}")

    # Truncation
    offset = hmac_hash[-1] & 0x0F
    truncate_hasg = hmac_hash[offset:offset + 4]
    print(f"Truncation: {truncate_hasg}")

    #Convert to Integer
    token_int = struct.unpack(">I", truncate_hasg[0] & 0x7FFFFFFF)

    #Take the last 6 digit
    token = token_int % 1000000
    return str(token).zfill(6) # PODEMOS ALTERAR MAIS MAIS OU MENOS DIGITOS DEPOIS



