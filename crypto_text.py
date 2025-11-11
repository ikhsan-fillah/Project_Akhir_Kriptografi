from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

class CaesarCipher:
    @staticmethod
    def encrypt(plaintext, shift):
        result = ""
        for char in plaintext:
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                result += char
        return result
    
    @staticmethod
    def decrypt(ciphertext, shift):
        result = ""
        for char in ciphertext:
            if char.isupper():
                result += chr((ord(char) - shift - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) - shift - 97) % 26 + 97)
            else:
                result += char
        return result


def buat_kunci_aes(bahan_kunci: str) -> bytes:
    #Buat kunci AES 192-bit dari passphrase (menggunakan SHA-256 lalu ambil 24 byte)
    h = hashlib.sha256(bahan_kunci.encode("utf-8")).digest()
    return h[:24]  # 192-bit


def tambah_padding(data: bytes, ukuran_blok=16) -> bytes:
    #Tambahkan padding PKCS7
    pad = ukuran_blok - (len(data) % ukuran_blok)
    return data + bytes([pad]) * pad


def hapus_padding(data: bytes) -> bytes:
    #Hapus padding PKCS7
    pad = data[-1]
    return data[:-pad]


def aes192_enkripsi(teks: str, bahan_kunci: str) -> bytes:
    #Enkripsi teks dengan AES-192 CBC mode
    kunci = buat_kunci_aes(bahan_kunci)
    iv = get_random_bytes(16)
    cipher = AES.new(kunci, AES.MODE_CBC, iv)
    data = tambah_padding(teks.encode("utf-8"))
    ct = cipher.encrypt(data)
    return iv + ct


def aes192_dekripsi(iv_ct: bytes, bahan_kunci: str) -> str:
    #Dekripsi ciphertext AES-192 CBC
    kunci = buat_kunci_aes(bahan_kunci)

    iv = iv_ct[:16]
    ct = iv_ct[16:]

    cipher = AES.new(kunci, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ct)
    pt = hapus_padding(pt)

    return pt.decode("utf-8")


class SuperEncryption:
    def __init__(self, shift=3):
        self.shift = shift
    
    def encrypt(self, plaintext, password):
        # Step 1: Caesar Cipher (Klasik)
        caesar_result = CaesarCipher.encrypt(plaintext, self.shift)
        
        # Step 2: AES-192 CBC (Modern)
        iv_ct = aes192_enkripsi(caesar_result, password)
        
        # Step 3: Encode ke Base64 untuk output
        ciphertext_b64 = base64.b64encode(iv_ct).decode("utf-8")
        
        return {
            'ciphertext': ciphertext_b64,
            'iv': base64.b64encode(iv_ct[:16]).decode('utf-8'),
            'shift': self.shift,
            'algorithm': 'Caesar Cipher + AES-192 CBC'
        }
    
    def decrypt(self, ciphertext, password):
        # Step 1: Decode Base64
        iv_ct = base64.b64decode(ciphertext)
        
        # Step 2: Dekripsi AES-192
        caesar_result = aes192_dekripsi(iv_ct, password)
        
        # Step 3: Dekripsi Caesar Cipher
        plaintext = CaesarCipher.decrypt(caesar_result, self.shift)
        return plaintext

class AESEncryption:    
    @staticmethod
    def prepare_key(password):
        """Konversi password ke 192-bit key menggunakan SHA-256"""
        return buat_kunci_aes(password)
    
    @staticmethod
    def encrypt(plaintext, password):
        iv_ct = aes192_enkripsi(plaintext, password)

        # Split IV and ciphertext
        iv = iv_ct[:16]
        ct = iv_ct[16:]

        return (
            base64.b64encode(ct).decode('utf-8'),
            base64.b64encode(iv).decode('utf-8')
        )
    
    @staticmethod
    def decrypt(ciphertext_base64, password, iv_base64):
        ct = base64.b64decode(ciphertext_base64)
        iv = base64.b64decode(iv_base64)

        # Combine IV + ciphertext
        iv_ct = iv + ct

        return aes192_dekripsi(iv_ct, password)


