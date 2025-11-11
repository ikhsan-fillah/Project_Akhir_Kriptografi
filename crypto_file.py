from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
import os
import json
import base64
import hashlib


class TripleDESFileEncryption:
    def __init__(self):
        self.algorithm = "3DES-192"
        self.key_size = 24
        self.block_size = 8  
    
    def _derive_key(self, password):
        salt = get_random_bytes(16)
        #menggunakan PBKDF2 untuk derive key 192-bit untuk 3DES
        key = PBKDF2(password, salt, dkLen=24, count=100000)
        return key, salt
    
    def encrypt_file(self, input_path, password, output_path=None):
        try:
            if not os.path.exists(input_path):
                return False, "File tidak ditemukan!", None

            if output_path is None:
                output_path = input_path + ".encrypted"

            with open(input_path, 'rb') as f:
                file_data = f.read()

            key, salt = self._derive_key(password)

            iv = get_random_bytes(self.block_size)
            cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)

            padded_data = pad(file_data, self.block_size)
            ciphertext = cipher.encrypt(padded_data)

            encrypted_data = {
                'algorithm': self.algorithm,
                'salt': base64.b64encode(salt).decode('utf-8'),
                'iv': base64.b64encode(iv).decode('utf-8'),
                'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
                'original_filename': os.path.basename(input_path)
            }

            with open(output_path, 'w') as f:
                json.dump(encrypted_data, f)

            file_size = os.path.getsize(output_path)
            return True, f"Enkripsi berhasil! Ukuran: {self._format_size(file_size)}", output_path

        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def decrypt_file(self, input_path, password, output_path=None):
        try:
            if not os.path.exists(input_path):
                return False, "File tidak ditemukan!", None

            with open(input_path, 'r') as f:
                encrypted_data = json.load(f)

            if output_path is None:
                if 'original_filename' in encrypted_data:
                    output_path = encrypted_data['original_filename']
                else:
                    output_path = input_path.replace('.encrypted', '')

            salt = base64.b64decode(encrypted_data['salt'])
            iv = base64.b64decode(encrypted_data['iv'])
            ciphertext = base64.b64decode(encrypted_data['ciphertext'])

            key = PBKDF2(password, salt, dkLen=24, count=100000)

            cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
            padded_data = cipher.decrypt(ciphertext)

            file_data = unpad(padded_data, self.block_size)

            with open(output_path, 'wb') as f:
                f.write(file_data)

            file_size = os.path.getsize(output_path)
            return True, f"Dekripsi berhasil! Ukuran: {self._format_size(file_size)}", output_path

        except ValueError as e:
            return False, "Dekripsi gagal! Password salah atau file rusak.", None
        except Exception as e:
            return False, f"Error: {str(e)}", None
    
    def _format_size(self, size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

