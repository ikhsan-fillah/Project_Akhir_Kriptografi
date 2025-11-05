import sqlite3
import hashlib
import base64
from datetime import datetime
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class Database:
    def __init__(self, db_name="cryptography.db"):
        self.db_name = db_name
        self._encryption_key = self._prepare_encryption_key(
            os.environ.get("DB_ENCRYPTION_KEY", "CamoCrypt217219!@SecretKey")
        )
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def _prepare_encryption_key(self, secret: str) -> bytes:
        #Siapkan kunci AES-256 (32-byte) dari secret string.
        return hashlib.sha256(secret.encode("utf-8")).digest()

    def _encrypt_value(self, value):
        if value is None:
            return None

        data = str(value).encode("utf-8")
        iv = os.urandom(16)
        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return base64.b64encode(iv + ciphertext).decode("utf-8")

    def _decrypt_value(self, encrypted_value):
        if encrypted_value is None:
            return None

        try:
            raw = base64.b64decode(encrypted_value)
            iv = raw[:16]
            ciphertext = raw[16:]
            cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
            return plaintext.decode("utf-8")
        except Exception:
            return encrypted_value
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS text_encryption (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plaintext TEXT,
                ciphertext TEXT,
                algorithm TEXT,
                iv TEXT,
                shift INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS steganography (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                original_image TEXT,
                stego_image TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_encryption (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                original_filename TEXT,
                encrypted_filename TEXT,
                algorithm TEXT,
                file_size INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        conn.close()

        self.create_default_user()
    
    def create_default_user(self):
        try:
            self.register_user("admin", "admin123", "Administrator")
        except:
            pass
    
    def generate_salt(self, length=16):
        #Generate random salt untuk password hashing
        import base64
        from Crypto.Random import get_random_bytes
        return base64.b64encode(get_random_bytes(length)).decode("utf-8")
    
    def hash_password(self, password, salt):
        #Hash password menggunakan SHA-256 dengan salt
        combined = salt.encode("utf-8") + password.encode("utf-8")
        return hashlib.sha256(combined).hexdigest()
    
    def register_user(self, username, password, full_name):
        #Registrasi user baru dengan salt
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Generate salt dan hash password
            salt = self.generate_salt()
            password_hash = self.hash_password(password, salt)
            
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, salt, full_name))
            conn.commit()
            return True, "Registrasi berhasil!"
        except sqlite3.IntegrityError:
            return False, "Username sudah terdaftar!"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            conn.close()
    
    def verify_user(self, username, password):
        #Verifikasi username dan password dengan salt
        conn = self.get_connection()
        cursor = conn.cursor()
        
        #Ambil salt dan hash dari database
        cursor.execute('''
            SELECT id, full_name, salt, password_hash FROM users 
            WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False, None
        
        user_id, full_name, salt, stored_hash = result
        
        #Hash password input dengan salt yang sama
        input_hash = self.hash_password(password, salt)
        
        #Bandingkan hash
        if input_hash == stored_hash:
            return True, {"user_id": user_id, "full_name": full_name}
        
        return False, None
    
    def get_user_info(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, full_name, created_at, salt
            FROM users WHERE username = ?
        ''', (username,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "user_id": result[0],
                "username": result[1],
                "full_name": result[2],
                "created_at": result[3],
                "salt": result[4]
            }
        return None
    
    def save_text_encryption(self, user_id, plaintext, ciphertext, algorithm, iv, shift):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO text_encryption 
                (user_id, plaintext, ciphertext, algorithm, iv, shift)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                self._encrypt_value(plaintext),
                self._encrypt_value(ciphertext),
                algorithm,
                iv,
                self._encrypt_value(shift)
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving text encryption: {e}")
            return False
        finally:
            conn.close()
    
    def get_text_encryption_history(self, user_id, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, plaintext, ciphertext, algorithm, iv, shift, created_at
            FROM text_encryption
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            plaintext = self._decrypt_value(row[1])
            ciphertext = self._decrypt_value(row[2])
            shift_raw = self._decrypt_value(row[5])
            try:
                shift_value = int(shift_raw) if shift_raw is not None else None
            except (TypeError, ValueError):
                shift_value = shift_raw
            history.append({
                "id": row[0],
                "plaintext": plaintext[:50] + "..." if plaintext and len(plaintext) > 50 else plaintext,
                "ciphertext": ciphertext[:50] + "..." if ciphertext and len(ciphertext) > 50 else ciphertext,
                "algorithm": row[3],
                "iv": row[4],
                "shift": shift_value,
                "created_at": row[6]
            })
        
        return history
    
    def save_steganography(self, user_id, original_image, stego_image, message):
        """Simpan riwayat steganografi"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO steganography 
                (user_id, original_image, stego_image, message)
                VALUES (?, ?, ?, ?)
            ''', (
                user_id,
                self._encrypt_value(original_image),
                self._encrypt_value(stego_image),
                self._encrypt_value(message)
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving steganography: {e}")
            return False
        finally:
            conn.close()
    
    def get_steganography_history(self, user_id, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, original_image, stego_image, message, created_at
            FROM steganography
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            original_image = self._decrypt_value(row[1])
            stego_image = self._decrypt_value(row[2])
            message = self._decrypt_value(row[3])
            history.append({
                "id": row[0],
                "original_image": original_image,
                "stego_image": stego_image,
                "message": message[:30] + "..." if message and len(message) > 30 else message,
                "created_at": row[4]
            })
        
        return history
    
    def save_file_encryption(self, user_id, original_filename, encrypted_filename, algorithm, file_size):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO file_encryption 
                (user_id, original_filename, encrypted_filename, algorithm, file_size)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                self._encrypt_value(original_filename),
                self._encrypt_value(encrypted_filename),
                algorithm,
                self._encrypt_value(file_size)
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error saving file encryption: {e}")
            return False
        finally:
            conn.close()
    
    def get_file_encryption_history(self, user_id, limit=10):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, original_filename, encrypted_filename, algorithm, file_size, created_at
            FROM file_encryption
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for row in results:
            original_filename = self._decrypt_value(row[1])
            encrypted_filename = self._decrypt_value(row[2])
            file_size_raw = self._decrypt_value(row[4])
            try:
                file_size_value = float(file_size_raw) if file_size_raw is not None else None
            except (TypeError, ValueError):
                file_size_value = file_size_raw
            history.append({
                "id": row[0],
                "original_filename": original_filename,
                "encrypted_filename": encrypted_filename,
                "algorithm": row[3],
                "file_size": file_size_value,
                "created_at": row[5]
            })
        
        return history
    
    def get_user_statistics(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM text_encryption WHERE user_id = ?', (user_id,))
        text_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM steganography WHERE user_id = ?', (user_id,))
        stego_count = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM file_encryption WHERE user_id = ?', (user_id,))
        file_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "text_encryptions": text_count,
            "steganography": stego_count,
            "file_encryptions": file_count,
            "total": text_count + stego_count + file_count
        }

if __name__ == "__main__":
    pass
