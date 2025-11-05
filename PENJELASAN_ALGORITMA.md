# 📚 Penjelasan Algoritma Kriptografi - CamoCrypt

**Dokumentasi Lengkap untuk Presentasi dan Pemahaman Teknis**

---

## 📑 Daftar Isi

1. [Super Enkripsi Text (Caesar + AES-192)](#1-super-enkripsi-text-caesar--aes-192)
2. [Enkripsi File dengan 3DES-192](#2-enkripsi-file-dengan-3des-192)
3. [Steganografi Gambar (LSB)](#3-steganografi-gambar-lsb)
4. [Enkripsi Database dengan AES-256](#4-enkripsi-database-dengan-aes-256)
5. [Autentikasi User (SHA-256 + Salt)](#5-autentikasi-user-sha-256--salt)

---

## 1. Super Enkripsi Text (Caesar + AES-192)

### 🎯 Konsep Dasar

Super enkripsi adalah **kombinasi dua algoritma kriptografi** yang berbeda untuk meningkatkan keamanan:

- **Caesar Cipher** (klasik) → Enkripsi layer pertama
- **AES-192 CBC** (modern) → Enkripsi layer kedua

### 🔄 Alur Enkripsi

```
Plaintext → [Caesar Cipher] → Caesar Result → [AES-192 CBC] → Ciphertext (Base64)
```

### 📝 Penjelasan Langkah Demi Langkah

#### **TAHAP ENKRIPSI:**

**Step 1: Caesar Cipher**

```python
def encrypt(plaintext, shift):
    for char in plaintext:
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
```

- **Input:** Text asli + shift value (1-25)
- **Proses:** Geser setiap huruf sebanyak `shift` posisi dalam alfabet
- **Contoh:**
  - Input: "HELLO" dengan shift 3
  - H → K, E → H, L → O, L → O, O → R
  - Output: "KHOOR"
- **Karakteristik:**
  - Non-huruf tidak berubah (spasi, angka, simbol)
  - Case-sensitive (huruf besar tetap besar)

**Step 2: AES-192 Encryption**

```python
def aes192_enkripsi(teks: str, password: str):
    # 1. Generate kunci dari password (langsung tanpa SHA-256)
    kunci = buat_kunci_aes(password)  # 24 bytes (192-bit)

    # 2. Generate IV random
    iv = get_random_bytes(16)

    # 3. Buat cipher AES CBC
    cipher = AES.new(kunci, AES.MODE_CBC, iv)

    # 4. Padding data ke kelipatan 16 bytes
    data_padded = tambah_padding(teks.encode("utf-8"))

    # 5. Enkripsi
    ciphertext = cipher.encrypt(data_padded)

    # 6. Gabung IV + ciphertext
    return iv + ciphertext
```

**Komponen AES-192:**

- **Kunci:** 192-bit (24 bytes) langsung dari password (pad/truncate)
- **Mode:** CBC (Cipher Block Chaining)
- **Block Size:** 128-bit (16 bytes)
- **IV:** 16 bytes random, berbeda setiap enkripsi
- **Padding:** PKCS7 (tambahkan bytes sampai kelipatan 16)

**Step 3: Encode Base64**

```python
ciphertext_b64 = base64.b64encode(iv + ciphertext).decode("utf-8")
```

- Mengubah binary data ke ASCII string
- Memudahkan penyimpanan dan transfer

#### **TAHAP DEKRIPSI:**

```
Ciphertext (Base64) → [Decode Base64] → IV + Ciphertext → [AES-192 Decrypt]
→ Caesar Result → [Caesar Decrypt] → Plaintext
```

**Step 1: Decode Base64**

```python
iv_ct = base64.b64decode(ciphertext)
```

**Step 2: Pisahkan IV dan Ciphertext**

```python
iv = iv_ct[:16]      # 16 bytes pertama
ct = iv_ct[16:]      # Sisanya
```

**Step 3: Dekripsi AES**

```python
cipher = AES.new(kunci, AES.MODE_CBC, iv)
caesar_result = hapus_padding(cipher.decrypt(ct))
```

**Step 4: Dekripsi Caesar**

```python
plaintext = CaesarCipher.decrypt(caesar_result, shift)
```

### 🔐 Keamanan

**Kelebihan:**

- **Double layer protection:** Bahkan jika Caesar di-break, masih ada AES
- **Key diversification:** Caesar shift + AES password
- **Modern security:** AES-192 sangat kuat (2^192 kombinasi)
- **Random IV:** Setiap enkripsi menghasilkan ciphertext berbeda
- **Simple key derivation:** Langsung dari passphrase tanpa hash overhead

**Potensi Kelemahan:**

- Caesar shift harus disimpan/diingat
- Jika shift diketahui, tinggal break AES saja

### 💡 Pertanyaan Interview yang Mungkin:

**Q: Kenapa pakai Caesar kalau sudah ada AES?**
A: Super enkripsi mendemonstrasikan konsep **defense in depth** - multiple layer security. Caesar sebagai pre-processing juga mengobfuscate pola plaintext sebelum AES.

**Q: Kenapa IV disimpan bersama ciphertext?**
A: IV bukan rahasia, hanya perlu unik. Tujuan IV adalah memastikan plaintext yang sama menghasilkan ciphertext berbeda. Keamanan tetap bergantung pada key.

**Q: Apa itu CBC mode?**
A: Cipher Block Chaining - setiap block di-XOR dengan ciphertext block sebelumnya. Block pertama di-XOR dengan IV. Ini mencegah pattern recognition attack.

---

## 2. Enkripsi File dengan 3DES-192

### 🎯 Konsep Dasar

**3DES (Triple Data Encryption Standard)** adalah evolusi dari DES yang menerapkan DES **tiga kali** dengan tiga kunci berbeda.

### 🔧 Spesifikasi Teknis

- **Algoritma:** 3DES (Triple DES)
- **Key Size:** 192-bit (3 × 64-bit keys)
- **Block Size:** 64-bit (8 bytes)
- **Mode:** CBC (Cipher Block Chaining)
- **Key Derivation:** PBKDF2 (Password-Based Key Derivation Function 2)

### 🔄 Alur Enkripsi File

```
Original File → [Read Binary] → File Data → [PBKDF2] → 192-bit Key
                                              ↓
                                         [3DES CBC]
                                              ↓
                        Ciphertext → [JSON Wrapper] → .encrypted file
```

### 📝 Penjelasan Langkah Demi Langkah

#### **TAHAP ENKRIPSI:**

**Step 1: Baca File**

```python
with open(input_path, 'rb') as f:
    file_data = f.read()
```

- Baca file dalam mode binary
- Semua jenis file didukung (txt, pdf, jpg, dll)

**Step 2: Key Derivation dengan PBKDF2**

```python
salt = get_random_bytes(16)
key = PBKDF2(password, salt, dkLen=24, count=100000)
```

**Penjelasan PBKDF2:**

- **Input:** Password + Salt
- **Output:** 192-bit (24 bytes) key untuk 3DES
- **Iterations:** 100,000 kali (mencegah brute force)
- **Salt:** 16 bytes random (mencegah rainbow table attack)

**Mengapa PBKDF2?**

- Password user biasanya lemah (< 20 karakter)
- PBKDF2 memperkuat password dengan iterasi berulang
- Membuat brute force attack sangat lambat

**Step 3: Generate IV dan Buat Cipher**

```python
iv = get_random_bytes(8)  # 8 bytes untuk DES block size
cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
```

**Step 4: Padding Data**

```python
padded_data = pad(file_data, 8)  # Padding ke kelipatan 8 bytes
```

- 3DES block size = 8 bytes
- Padding PKCS7: tambahkan N bytes dengan nilai N

**Step 5: Enkripsi**

```python
ciphertext = cipher.encrypt(padded_data)
```

**Step 6: Simpan ke JSON**

```python
encrypted_data = {
    'algorithm': '3DES-192',
    'salt': base64.b64encode(salt).decode('utf-8'),
    'iv': base64.b64encode(iv).decode('utf-8'),
    'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
    'original_filename': filename
}

with open(output_path, 'w') as f:
    json.dump(encrypted_data, f)
```

**Mengapa JSON?**

- Menyimpan metadata (salt, iv, filename)
- Format terstruktur, mudah di-parse
- Human-readable (untuk debugging)

#### **TAHAP DEKRIPSI:**

**Step 1: Load Encrypted File**

```python
with open(input_path, 'r') as f:
    encrypted_data = json.load(f)
```

**Step 2: Extract Components**

```python
salt = base64.b64decode(encrypted_data['salt'])
iv = base64.b64decode(encrypted_data['iv'])
ciphertext = base64.b64decode(encrypted_data['ciphertext'])
```

**Step 3: Regenerate Key**

```python
key = PBKDF2(password, salt, dkLen=24, count=100000)
```

- **Penting:** Gunakan salt yang sama!
- Password + salt sama = key yang sama

**Step 4: Dekripsi**

```python
cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
padded_data = cipher.decrypt(ciphertext)
file_data = unpad(padded_data, 8)
```

**Step 5: Simpan File**

```python
with open(output_path, 'wb') as f:
    f.write(file_data)
```

### 🔐 Keamanan

**Kekuatan:**

- **192-bit key:** 2^192 kombinasi (sangat kuat)
- **Triple encryption:** DES diterapkan 3 kali
- **PBKDF2:** Mencegah brute force password
- **Random salt:** Setiap file berbeda, tidak bisa pre-compute

**Struktur 3DES:**

```
Plaintext → [Encrypt K1] → [Decrypt K2] → [Encrypt K3] → Ciphertext
```

**Known Issues:**

- Block size 64-bit dianggap kecil (rentan birthday attack untuk data besar)
- Lebih lambat dari AES
- Legacy algorithm, AES lebih direkomendasikan untuk aplikasi baru

### 💡 Pertanyaan Interview:

**Q: Mengapa 3DES dan bukan DES biasa?**
A: DES 56-bit key sudah tidak aman (bisa di-crack < 24 jam). 3DES meningkatkan key menjadi 192-bit dengan menerapkan DES tiga kali.

**Q: Kenapa pakai PBKDF2 dengan 100,000 iterasi?**
A: PBKDF2 memperlambat brute force. Dengan 100k iterasi, attacker harus menjalankan PBKDF2 100k kali untuk setiap password attempt.

**Q: Apa bedanya salt dan IV?**
A:

- **Salt:** Digunakan dalam key derivation (PBKDF2), mencegah rainbow table
- **IV:** Digunakan dalam enkripsi CBC, mencegah pattern recognition

**Q: Kenapa salt dan IV disimpan plain text?**
A: Salt dan IV bukan rahasia. Keamanan hanya bergantung pada password/key. Menyimpan salt/IV memungkinkan dekripsi tanpa menambah kompleksitas.

---

## 3. Steganografi Gambar (LSB)

### 🎯 Konsep Dasar

**Steganografi** adalah seni menyembunyikan informasi dalam media lain, sehingga **tidak terlihat** ada pesan rahasia. Berbeda dengan kriptografi yang mengacak pesan, steganografi **menyembunyikan** keberadaan pesan itu sendiri.

### 🖼️ Metode: LSB (Least Significant Bit)

**Prinsip LSB:**

- Pixel gambar RGB memiliki 3 channel: Red, Green, Blue
- Setiap channel 8-bit (0-255)
- Bit terakhir (LSB) diubah untuk menyimpan data
- Perubahan 1 bit di LSB hampir tidak terlihat mata

**Contoh:**

```
Pixel asli:     R=11010110, G=10101100, B=11001101
                  ↑ MSB               ↑ LSB

Ubah LSB:       R=11010111, G=10101100, B=11001100
                       ↑                      ↑
Perubahan nilai: 214→215      204→204      205→204
Visual impact:   Tidak terlihat oleh mata manusia
```

### 🔄 Alur Steganografi

#### **EMBEDDING (Sembunyikan Pesan):**

```
Cover Image → [Load RGB] → Pixel Array → [Flatten] → 1D Array
                                                         ↓
Message Text → [Text to Binary] → Binary String → [Replace LSB]
                                                         ↓
                                            Modified Array → [Reshape]
                                                         ↓
                                                   Stego Image
```

### 📝 Penjelasan Langkah Demi Langkah

#### **TAHAP EMBEDDING:**

**Step 1: Load dan Convert Image**

```python
img = Image.open(image_path)
if img.mode != 'RGB':
    img = img.convert('RGB')
img_array = np.array(img)
```

- Convert ke RGB (3 channel)
- NumPy array untuk manipulasi cepat

**Step 2: Convert Text ke Binary**

```python
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)
```

**Contoh:**

```
Text: "Hi"
H = 72  → 01001000
i = 105 → 01101001
Binary: "0100100001101001"
```

**Step 3: Tambah Delimiter**

```python
full_message = message + "$$$END$$$"
binary_message = text_to_binary(full_message)
```

- Delimiter menandai akhir pesan
- Penting untuk ekstraksi nanti

**Step 4: Flatten Image Array**

```python
flat_img = img_array.flatten()
```

- Convert 3D array (height, width, 3) ke 1D
- Memudahkan iterasi

**Step 5: Replace LSB**

```python
for i, bit in enumerate(binary_message):
    flat_img[i] = (flat_img[i] & 0xFE) | int(bit)
```

**Penjelasan bit manipulation:**

```python
original_byte = 11010110  (214)
& 0xFE        = 11111110
              = 11010110  (set LSB = 0)

| new_bit (1) = 11010111  (215)
```

- `& 0xFE`: Clear LSB (set jadi 0)
- `| int(bit)`: Set LSB sesuai bit pesan

**Step 6: Reshape dan Save**

```python
stego_array = flat_img.reshape(img_array.shape)
stego_img = Image.fromarray(stego_array.astype('uint8'), mode='RGB')
stego_img.save(output_path, 'PNG')
```

- **Penting:** Simpan sebagai PNG (lossless)
- JPG akan merusak LSB karena kompresi lossy

#### **TAHAP EXTRACTION:**

**Step 1: Load Stego Image**

```python
img = Image.open(stego_image_path)
img_array = np.array(img)
flat_img = img_array.flatten()
```

**Step 2: Extract LSB**

```python
binary_message = ''
for pixel_value in flat_img:
    binary_message += str(pixel_value & 1)
```

- `& 1`: Extract bit terakhir

**Step 3: Convert Binary ke Text**

```python
def binary_to_text(binary):
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text += chr(int(byte, 2))
    return text
```

**Step 4: Cari Delimiter**

```python
full_text = binary_to_text(binary_message)
if "$$$END$$$" in full_text:
    message = full_text.split("$$$END$$$")[0]
```

### 📊 Kapasitas

**Formula:**

```
Kapasitas (karakter) = (Width × Height × 3) ÷ 8 - len(delimiter)
```

**Contoh:**

- Image: 1000×1000 px
- Total pixels: 1,000,000 × 3 (RGB) = 3,000,000 bits
- Kapasitas: 3,000,000 ÷ 8 = 375,000 karakter (~375 KB)

### 🔐 Keamanan

**Kelebihan:**

- **Tidak terlihat:** Perubahan 1 bit di LSB hampir tidak terdeteksi
- **Kapasitas besar:** Tergantung ukuran gambar
- **Tidak ada encryption overhead:** File size hampir sama

**Kelemahan:**

- **Tidak encrypted:** Jika ketahuan ada pesan, langsung bisa dibaca
- **Format sensitif:** Harus PNG, tidak boleh JPG
- **Steganalysis:** Algoritma khusus bisa deteksi LSB steganography

**Cara Meningkatkan Keamanan:**

1. Enkripsi pesan dulu sebelum embed (AES + Steganography)
2. Gunakan random LSB selection (tidak berurutan)
3. Gunakan password-based LSB placement

### 💡 Pertanyaan Interview:

**Q: Kenapa tidak terlihat secara visual?**
A: Mata manusia tidak sensitif terhadap perubahan 1 bit di nilai pixel. Perubahan 254→255 atau 100→101 tidak terlihat.

**Q: Kenapa harus PNG, tidak bisa JPG?**
A: JPG menggunakan kompresi lossy yang memodifikasi nilai pixel, sehingga LSB akan rusak/berubah.

**Q: Bagaimana jika gambar di-compress/resize?**
A: Pesan akan rusak. Steganografi LSB hanya tahan terhadap penyimpanan lossless.

**Q: Apakah lebih aman dari kriptografi?**
A: Bukan lebih aman, tapi berbeda tujuan:

- Kriptografi: Sembunyikan **isi** pesan
- Steganografi: Sembunyikan **keberadaan** pesan

**Q: Apa itu steganalysis?**
A: Teknik untuk mendeteksi ada/tidaknya steganografi. Metode: histogram analysis, chi-square test, dll.

---

## 4. Enkripsi Database dengan AES-256

### 🎯 Konsep Dasar

**Database encryption at rest** - mengenkripsi data sensitif sebelum disimpan ke database, sehingga jika database dicuri/di-leak, data tidak bisa dibaca tanpa encryption key.

### 🔧 Spesifikasi Teknis

- **Algoritma:** AES-256 CBC
- **Key Size:** 256-bit (32 bytes)
- **Mode:** CBC (Cipher Block Chaining)
- **Key Derivation:** SHA-256 dari secret key
- **Scope:** Kolom sensitif (plaintext, ciphertext, message, filename, shift, file_size)

### 🏗️ Arsitektur

```
Application Layer (Python)
         ↓
    [Encrypt]
         ↓
Database Layer (SQLite)
 ┌─────────────────────┐
 │ Encrypted Columns:  │
 │ - plaintext         │  ← AES-256 encrypted
 │ - ciphertext        │  ← AES-256 encrypted
 │ - message           │  ← AES-256 encrypted
 │ - filename          │  ← AES-256 encrypted
 └─────────────────────┘
```

### 🔄 Alur Enkripsi/Dekripsi

#### **WRITE (Enkripsi):**

```
Data → [_encrypt_value] → IV + Ciphertext → [Base64] → Database
```

#### **READ (Dekripsi):**

```
Database → [Base64 Decode] → IV + Ciphertext → [_decrypt_value] → Data
```

### 📝 Penjelasan Implementasi

#### **Key Management:**

**Step 1: Generate Master Key**

```python
def _prepare_encryption_key(self, secret: str) -> bytes:
    return hashlib.sha256(secret.encode("utf-8")).digest()
```

- SHA-256 menghasilkan 256-bit key
- Secret dari environment variable atau hardcoded default
- **Best practice:** Gunakan environment variable, jangan hardcode

**Master Key Source:**

```python
os.environ.get("DB_ENCRYPTION_KEY", "CAMOCRYPT_DB_DEFAULT_KEY")
```

#### **Enkripsi Value:**

```python
def _encrypt_value(self, value):
    if value is None:
        return None

    # 1. Convert ke bytes
    data = str(value).encode("utf-8")

    # 2. Generate random IV
    iv = os.urandom(16)

    # 3. Create AES cipher
    cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv)

    # 4. Padding dan enkripsi
    ciphertext = cipher.encrypt(pad(data, AES.block_size))

    # 5. Gabung IV + ciphertext
    combined = iv + ciphertext

    # 6. Encode Base64 untuk storage
    return base64.b64encode(combined).decode("utf-8")
```

**Flow Detail:**

1. **Input:** "Hello World"
2. **Bytes:** b'Hello World'
3. **Padding:** b'Hello World\x05\x05\x05\x05\x05' (16 bytes)
4. **IV:** Random 16 bytes (contoh: b'\x1a\x2b\x3c...')
5. **Encrypt:** Ciphertext 16 bytes
6. **Combine:** IV + Ciphertext (32 bytes)
7. **Base64:** "GisuPIQ7DxY..." (44 characters)
8. **Store:** Simpan ke database

#### **Dekripsi Value:**

```python
def _decrypt_value(self, encrypted_value):
    if encrypted_value is None:
        return None

    try:
        # 1. Decode Base64
        raw = base64.b64decode(encrypted_value)

        # 2. Split IV dan ciphertext
        iv = raw[:16]
        ciphertext = raw[16:]

        # 3. Create cipher dengan IV yang sama
        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv)

        # 4. Dekripsi dan unpad
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # 5. Convert ke string
        return plaintext.decode("utf-8")

    except Exception:
        # Backward compatibility: data lama belum encrypted
        return encrypted_value
```

**Error Handling:**

- Try-except untuk backward compatibility
- Jika dekripsi gagal, asumsikan data lama (plain text)
- Memungkinkan migrasi gradual

#### **Transparent Encryption:**

**Save Data:**

```python
def save_text_encryption(self, user_id, plaintext, ciphertext, ...):
    cursor.execute('''
        INSERT INTO text_encryption (user_id, plaintext, ciphertext, ...)
        VALUES (?, ?, ?, ...)
    ''', (
        user_id,
        self._encrypt_value(plaintext),      # ← Auto encrypt
        self._encrypt_value(ciphertext),     # ← Auto encrypt
        ...
    ))
```

**Read Data:**

```python
def get_text_encryption_history(self, user_id):
    cursor.execute('SELECT plaintext, ciphertext FROM ...')
    results = cursor.fetchall()

    history = []
    for row in results:
        history.append({
            'plaintext': self._decrypt_value(row[0]),    # ← Auto decrypt
            'ciphertext': self._decrypt_value(row[1]),   # ← Auto decrypt
        })
```

### 🔐 Keamanan

**Threat Model:**

1. **Database File Stolen:**

   - ✅ Data encrypted
   - ✅ Attacker tidak punya encryption key
   - ✅ Data tidak bisa dibaca

2. **SQL Injection:**

   - ✅ Data encrypted, tidak berguna untuk attacker
   - ⚠️ Masih bisa delete/modify encrypted data

3. **Application Compromised:**

   - ❌ Key ada di application, data bisa didecrypt
   - **Mitigation:** Separate key management service

4. **Insider Threat (DB Admin):**
   - ✅ DB admin tidak bisa baca data
   - ✅ Butuh application access untuk decrypt

**Best Practices:**

1. **Key Rotation:**

   ```python
   # Ideal: Rotate key setiap 90 hari
   # Re-encrypt semua data dengan key baru
   ```

2. **Environment Variable:**

   ```bash
   export DB_ENCRYPTION_KEY="your-256-bit-secret-key"
   ```

3. **Key Storage:**

   - ❌ Jangan hardcode di code
   - ✅ Environment variable
   - ✅ AWS KMS / Azure Key Vault (production)

4. **Audit Logging:**
   - Log setiap read/write encrypted data
   - Monitor suspicious access patterns

### 💡 Pertanyaan Interview:

**Q: Mengapa tidak encrypt seluruh database?**
A:

- Performance: Enkripsi/dekripsi setiap query lambat
- Functionality: Tidak bisa search/index encrypted data
- **Selective encryption:** Hanya kolom sensitif

**Q: Bagaimana dengan performance?**
A:

- Overhead ~20-30% untuk encrypt/decrypt
- Trade-off: Security vs Performance
- **Optimization:** Cache decrypted data di memory (dengan risk)

**Q: Apa bedanya dengan database-level encryption (SQLCipher)?**
A:

- **SQLCipher:** Encrypt entire database file
- **Application-level:** Encrypt specific columns
- **Hybrid:** Gunakan keduanya untuk defense in depth

**Q: Bagaimana jika lupa encryption key?**
A: **Data hilang selamanya**. Tidak ada recovery. Backup key sangat penting.

**Q: Kenapa pakai CBC bukan GCM?**
A:

- CBC: Enkripsi saja
- GCM: Enkripsi + authentication
- **Ideal:** GCM lebih baik (prevent tampering)

---

## 5. Autentikasi User (SHA-256 + Salt)

### 🎯 Konsep Dasar

**Password hashing** adalah proses satu arah untuk menyimpan password secara aman. Sistem tidak menyimpan password asli, hanya hash-nya.

### 🔐 Komponen

#### **1. Hash Function (SHA-256)**

```python
def hash_password(password, salt):
    combined = salt.encode("utf-8") + password.encode("utf-8")
    return hashlib.sha256(combined).hexdigest()
```

**Karakteristik SHA-256:**

- **One-way:** Tidak bisa reverse (hash → password)
- **Deterministic:** Input sama → hash sama
- **Avalanche effect:** Input beda 1 bit → hash beda 50%
- **Fixed size:** Output selalu 256-bit (64 hex characters)

**Contoh:**

```
Password: "hello123"
SHA-256:  "8b428614f68eafebac4fa68e74f5c8b3f7c32e91ac8c8c5f41f62f4e8e8e8e8e"

Password: "hello124" (beda 1 karakter)
SHA-256:  "9c539715g79fbfgcbd5gb69f85g6d9c4g8d43f02bd9d9d6g52g73g5f9f9f9f9f"
         ↑ Completely different!
```

#### **2. Salt**

```python
def generate_salt(length=16):
    return base64.b64encode(get_random_bytes(length)).decode("utf-8")
```

**Mengapa Salt?**

**Tanpa Salt (VULNERABLE):**

```
User 1: password123 → SHA-256 → ef92b778...
User 2: password123 → SHA-256 → ef92b778...  ← Hash sama!
```

- **Rainbow table attack:** Pre-computed hash untuk password umum
- Semua user dengan password sama = hash sama

**Dengan Salt (SECURE):**

```
User 1: salt_abc + password123 → SHA-256 → 8f7a9c...
User 2: salt_xyz + password123 → SHA-256 → 2d4e1b...  ← Hash beda!
```

- Salt unique per user
- Rainbow table tidak berguna
- Attacker harus brute force tiap user

### 🔄 Alur Autentikasi

#### **REGISTRASI:**

```
User Input: username, password
                ↓
         [Generate Salt]
                ↓
      Salt: "aBc123XyZ..."
                ↓
    [Hash: SHA-256(salt + password)]
                ↓
      Hash: "8f7a9c..."
                ↓
   [Store: username, hash, salt]
                ↓
         Database
```

**Code:**

```python
def register_user(self, username, password, full_name):
    # 1. Generate random salt
    salt = self.generate_salt()

    # 2. Hash password dengan salt
    password_hash = self.hash_password(password, salt)

    # 3. Simpan ke database
    cursor.execute('''
        INSERT INTO users (username, password_hash, salt, full_name)
        VALUES (?, ?, ?, ?)
    ''', (username, password_hash, salt, full_name))
```

#### **LOGIN:**

```
User Input: username, password
                ↓
    [Query DB: get salt, hash]
                ↓
      Salt from DB: "aBc123XyZ..."
      Hash from DB: "8f7a9c..."
                ↓
    [Hash: SHA-256(salt + password)]
                ↓
      Computed Hash: "8f7a9c..."
                ↓
    [Compare: computed == stored]
                ↓
         Login Success!
```

**Code:**

```python
def verify_user(self, username, password):
    # 1. Query salt dan hash dari database
    cursor.execute('''
        SELECT id, full_name, salt, password_hash FROM users
        WHERE username = ?
    ''', (username,))

    result = cursor.fetchone()
    if not result:
        return False, None

    user_id, full_name, salt, stored_hash = result

    # 2. Hash password input dengan salt dari DB
    input_hash = self.hash_password(password, salt)

    # 3. Compare hash
    if input_hash == stored_hash:
        return True, {"user_id": user_id, "full_name": full_name}

    return False, None
```

### 🔐 Keamanan

**Attack Vectors dan Mitigasi:**

1. **Rainbow Table Attack**

   - **Threat:** Pre-computed hash untuk password umum
   - **Mitigation:** ✅ Salt mencegah ini

2. **Brute Force Attack**

   - **Threat:** Try semua kombinasi password
   - **Current:** SHA-256 sangat cepat (~1M hash/detik)
   - **Mitigation:** ⚠️ Gunakan slow hash (bcrypt, Argon2)

3. **Dictionary Attack**

   - **Threat:** Try password umum (password123, admin, qwerty)
   - **Mitigation:**
     - ✅ Password policy (min 6 characters)
     - ⚠️ Better: min 12 characters, complexity requirements

4. **Credential Stuffing**
   - **Threat:** Gunakan leaked credentials dari breach lain
   - **Mitigation:**
     - ✅ Unique hash per user (salt)
     - ⚠️ Add: rate limiting, CAPTCHA

### 🚀 Improvements

**Current Implementation:**

```python
password_hash = hashlib.sha256(salt + password).hexdigest()
```

**Better (Production):**

```python
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,      # Iterations
    memory_cost=65536, # 64 MB
    parallelism=4     # Threads
)

# Register
password_hash = ph.hash(password)  # Salt automatic

# Login
try:
    ph.verify(password_hash, password)
    # Valid!
except:
    # Invalid
```

**Mengapa Argon2 lebih baik?**

- **Memory-hard:** Butuh banyak RAM, mencegah GPU/ASIC attack
- **Time-cost:** Configurable iterations
- **Winner of Password Hashing Competition 2015**

### 💡 Pertanyaan Interview:

**Q: Mengapa tidak encrypt password?**
A:

- Encrypt: Two-way (bisa decrypt)
- Hash: One-way (tidak bisa reverse)
- **Sistem tidak perlu tahu password asli**, cukup verify hash

**Q: Apakah admin bisa lihat password user?**
A: **Tidak**. Admin hanya lihat hash. Bahkan admin tidak bisa recover password. Hanya bisa reset.

**Q: Bagaimana forgot password?**
A:

1. Kirim reset link (dengan token)
2. User buat password baru
3. Hash password baru, simpan

- **Tidak ada "kirim password lama"** karena tidak tersimpan

**Q: Apa bedanya salt dan pepper?**
A:

- **Salt:** Random, unique per user, disimpan di database
- **Pepper:** Secret, sama untuk semua user, disimpan di application config
- **Best:** Gunakan keduanya: `hash(pepper + salt + password)`

**Q: Kenapa salt disimpan plain text di database?**
A: Salt bukan rahasia. Tujuan salt: mencegah rainbow table dan identical hash untuk password sama. Keamanan tetap bergantung pada password.

---

## 🎓 Tips Presentasi

### Struktur Presentasi yang Baik:

1. **Opening (2 menit)**

   - Perkenalan aplikasi CamoCrypt
   - Overview fitur: Text, File, Steganography, Database

2. **Super Enkripsi (5 menit)**

   - Jelaskan Caesar → AES flow
   - Demo enkripsi "Hello World"
   - Tunjukkan ciphertext berbeda dengan input sama

3. **File Encryption (4 menit)**

   - Jelaskan 3DES dan PBKDF2
   - Tunjukkan JSON structure hasil enkripsi
   - Demo enkripsi file .txt

4. **Steganografi (5 menit)**

   - Jelaskan LSB dengan diagram
   - Tunjukkan pixel sebelum/sesudah (nilai hampir sama)
   - Demo embed dan extract

5. **Database Security (3 menit)**

   - Tunjukkan database dengan data encrypted
   - Jelaskan transparent encryption
   - Tunjukkan query result (data decrypted)

6. **Q&A (5 menit)**
   - Siap jawab pertanyaan teknis di atas

### Key Points yang Harus Ditekankan:

✅ **Defense in Depth:** Multiple layer security
✅ **Modern Standards:** AES, 3DES, SHA-256
✅ **Best Practices:** Salt, IV, PBKDF2
✅ **Transparent Security:** User tidak perlu tahu detail teknis

### Jika Ditanya Hal Sulit:

- **Jangan panik:** "Pertanyaan bagus, saya jelaskan..."
- **Gunakan analogi:** "Seperti mengunci brankas di dalam brankas"
- **Rujuk dokumentasi:** "Sesuai NIST standard..."
- **Acknowledge limitation:** "Memang ada kelemahan X, mitigasinya Y"

---

## 📚 Referensi

- [NIST AES Standard](https://csrc.nist.gov/publications/detail/fips/197/final)
- [3DES (FIPS 46-3)](https://csrc.nist.gov/publications/detail/fips/46/3/archive/1999-10-25)
- [PBKDF2 RFC 2898](https://tools.ietf.org/html/rfc2898)
- [LSB Steganography Research](https://ieeexplore.ieee.org)

---

**Good luck untuk presentasi! 🚀**

Kalau ada yang belum jelas atau mau drill down lebih dalam di topik tertentu, tanya aja!
