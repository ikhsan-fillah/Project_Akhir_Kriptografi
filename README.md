# 🔐 CamoCrypt - Sistem Keamanan Data Berbasis Python

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

CamoCrypt adalah aplikasi kriptografi komprehensif yang mengimplementasikan berbagai algoritma enkripsi modern dan klasik untuk keamanan data. Dibuat sebagai tugas akhir mata kuliah Kriptografi.

## 📋 Daftar Isi

- [Fitur](#-fitur-utama)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Algoritma](#-algoritma-yang-digunakan)
- [Struktur Proyek](#-struktur-proyek)
- [Screenshot](#-screenshot)
- [Kontributor](#-kontributor)

## ✨ Fitur Utama

### 1. 🔑 Autentikasi Aman (SHA-256 + Salt)

- Login dan registrasi user
- Password hashing menggunakan SHA-256 dengan salt unik per user
- Database SQLite dengan enkripsi AES-256 untuk data sensitif
- Session management yang aman

### 2. 💬 Super Enkripsi Text (Caesar + AES-192)

- **Double Layer Encryption:**
  - Layer 1: Caesar Cipher (Algoritma Klasik, shift 1-25)
  - Layer 2: AES-192 CBC (Algoritma Modern)
- Custom shift untuk Caesar Cipher (1-25)
- Password-protected (langsung dari passphrase)
- Random IV untuk setiap enkripsi
- IV embedded dalam ciphertext (Base64)
- Defense in depth security

### 3. 🖼️ Steganografi Gambar (LSB)

- **Metode:** LSB (Least Significant Bit) Embedding
- Sembunyikan pesan dalam gambar RGB
- Support PNG, JPG, JPEG, BMP (PNG recommended)
- Ekstraksi pesan dari stego image
- Tidak terlihat secara visual (perubahan 1 bit per pixel)
- Kapasitas otomatis dihitung berdasarkan ukuran gambar
- Delimiter `$$$END$$$` untuk marking akhir pesan

### 4. 📁 Enkripsi File (3DES-192)

- **3DES (Triple Data Encryption Standard)** dengan 192-bit key
- **PBKDF2** untuk key derivation (100,000 iterasi)
- Support semua jenis file (txt, pdf, jpg, dll)
- Password-based encryption
- Metadata disimpan dalam JSON format
- Random salt dan IV untuk setiap file

### 5. 🔐 Database Encryption (AES-256)

- **Application-level encryption** untuk kolom sensitif
- AES-256 CBC mode
- Transparent encryption/decryption
- Custom encryption key: `CamoCrypt217219!@SecretKey`
- Kolom yang dienkripsi: plaintext, ciphertext, message, filename, shift, file_size

### 6. 📊 Riwayat & Statistik

- Tracking semua aktivitas enkripsi
- Statistik per user (text, steganografi, file)
- History enkripsi text dengan algoritma dan shift
- History steganografi dengan pesan
- History enkripsi file dengan ukuran dan algoritma

## 🚀 Instalasi

### Prasyarat

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download repository**

```bash
cd "KULIAH/Semester 5/Kriptografi/project akhir"
```

2. **Buat virtual environment (opsional, tapi disarankan)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Jalankan aplikasi**

```bash
streamlit run app.py
```

5. **Buka browser**

```
http://localhost:8501
```

## 📖 Cara Penggunaan

### Login / Register

1. Buka aplikasi di browser
2. **Login** dengan user default:
   - Username: `admin`
   - Password: `admin123`
3. Atau **Register** untuk membuat akun baru

### Enkripsi Text (Super Enkripsi)

**Enkripsi:**

1. Pilih menu "💬 Enkripsi Text"
2. Tab "🔒 Enkripsi":
   - Masukkan pesan yang ingin dienkripsi
   - Atur Caesar Shift (1-25, default: 5)
   - Masukkan passphrase AES
   - Klik "🔒 Enkripsi"
   - Ciphertext (Base64 dengan IV embedded) akan ditampilkan

**Dekripsi:**

1. Tab "🔓 Dekripsi":
   - Paste ciphertext (Base64)
   - Masukkan shift yang sama (1-25)
   - Masukkan passphrase yang sama
   - Klik "🔓 Dekripsi"
   - Pesan asli akan ditampilkan

### Steganografi Gambar

**Sembunyikan Pesan:**

1. Pilih menu "🖼️ Steganografi Gambar"
2. Tab "📥 Sembunyikan Pesan":
   - Upload gambar cover (PNG disarankan untuk hasil terbaik)
   - Lihat kapasitas gambar (karakter maksimal)
   - Ketik pesan rahasia
   - Klik "🔒 Sembunyikan Pesan"
   - Download stego image (PNG format)

**Ekstrak Pesan:**

1. Tab "📤 Ekstrak Pesan":
   - Upload stego image (harus PNG)
   - Klik "🔓 Ekstrak Pesan"
   - Pesan tersembunyi akan ditampilkan
   - Download pesan hasil ekstraksi (.txt)

### Enkripsi File (3DES)

**Enkripsi:**

1. Pilih menu "📁 Enkripsi File"
2. Tab "� Enkripsi":
   - Upload file yang akan dienkripsi (semua jenis file)
   - Masukkan password untuk enkripsi
   - Klik "🔒 Enkripsi File"
   - Download file terenkripsi (.encrypted dalam format JSON)
   - **PENTING:** Simpan password dengan aman!

**Dekripsi:**

1. Tab "🔓 Dekripsi":
   - Upload file .encrypted
   - Masukkan password yang sama saat enkripsi
   - Klik "🔓 Dekripsi File"
   - Download file asli yang terdekripsi

## 🔒 Algoritma yang Digunakan

### 1. SHA-256 + Salt (Password Hashing)

- **Fungsi:** Password hashing untuk autentikasi
- **Output:** 256-bit hash (64 hex characters)
- **Properties:** One-way, collision-resistant
- **Salt:** 16 bytes random, unique per user
- **Mencegah:** Rainbow table attack, identical password hash

### 2. Caesar Cipher (Classical Cryptography)

- **Jenis:** Substitution cipher
- **Key space:** 25 (shift 1-25)
- **Contoh:** HELLO → KHOOR (shift 3)
- **Karakteristik:** Case-sensitive, non-huruf tidak berubah
- **Fungsi:** Pre-processing layer dalam super enkripsi

### 3. AES-192 CBC (Advanced Encryption Standard)

- **Jenis:** Symmetric block cipher
- **Mode:** CBC (Cipher Block Chaining)
- **Key size:** 192 bit (24 bytes) langsung dari passphrase
- **Block size:** 128 bit (16 bytes)
- **Padding:** PKCS7
- **IV:** 16 bytes random, embedded dalam ciphertext
- **Fungsi:** Layer kedua dalam super enkripsi text

### 4. 3DES-192 (Triple Data Encryption Standard)

- **Jenis:** Symmetric block cipher
- **Key size:** 192 bit (24 bytes)
- **Block size:** 64 bit (8 bytes)
- **Mode:** CBC
- **Key Derivation:** PBKDF2 (100,000 iterasi)
- **Struktur:** Encrypt → Decrypt → Encrypt (EDE)
- **Fungsi:** Enkripsi file

### 5. LSB Steganography (Least Significant Bit)

- **Metode:** Least Significant Bit embedding
- **Carrier:** Image RGB pixels
- **Capacity:** ~1 byte per 8 pixels
- **Formula:** `(Width × Height × 3) ÷ 8` karakter
- **Delimiter:** `$$$END$$$` untuk marking akhir pesan
- **Format:** PNG (lossless, JPG tidak disarankan)

### 6. AES-256 CBC (Database Encryption)

- **Jenis:** Symmetric block cipher
- **Mode:** CBC (Cipher Block Chaining)
- **Key size:** 256 bit (32 bytes) dari SHA-256
- **Block size:** 128 bit (16 bytes)
- **Master Key:** `CamoCrypt217219!@SecretKey`
- **Fungsi:** Enkripsi kolom sensitif di database
- **Scope:** Plaintext, ciphertext, message, filename, shift, file_size

### 7. PBKDF2 (Key Derivation Function)

- **Fungsi:** Strengthen password untuk key generation
- **Iterations:** 100,000 kali
- **Output:** 192-bit key untuk 3DES
- **Salt:** 16 bytes random
- **Mencegah:** Brute force attack pada password

## 📁 Struktur Proyek

```
project akhir/
│
├── app.py                     # Main entry point (Streamlit routing)
├── database.py                # Database handler (SQLite + AES-256 encryption)
├── login.py                   # Halaman login & register (tabs)
├── halaman_utama.py           # Dashboard & semua fitur utama
├── register.py                # (Not used - legacy file)
│
├── crypto_text.py             # Super enkripsi (Caesar + AES-128)
├── crypto_image.py            # Steganografi LSB
├── crypto_file.py             # Enkripsi file 3DES-192
│
├── requirements.txt           # Python dependencies
├── README.md                  # Dokumentasi (file ini)
├── PENJELASAN_ALGORITMA.md    # Penjelasan detail algoritma
├── QUICKSTART.md              # Quick start guide
├── USAGE_GUIDE.md             # Panduan penggunaan lengkap
├── .gitignore                 # Git ignore rules
│
└── cryptography.db            # Database SQLite (auto-generated)
```

## 🛠️ Teknologi & Library

### Backend

- **Python 3.13+**
- **PyCryptodome** - Implementasi AES, 3DES, SHA-256, PBKDF2
- **Pillow (PIL)** - Image processing untuk steganografi
- **NumPy** - Array operations untuk LSB manipulation
- **SQLite** - Database management dengan AES-256 encryption

### Frontend

- **Streamlit 1.29** - Web UI framework
- **Custom CSS** - Styling untuk button dan layout (biru theme)

## 📊 Database Schema

### Table: `users`

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,        -- SHA-256 hash
    salt TEXT NOT NULL,                 -- Random salt per user
    full_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Table: `text_encryption`

```sql
CREATE TABLE text_encryption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plaintext TEXT,                     -- AES-256 encrypted
    ciphertext TEXT,                    -- AES-256 encrypted
    algorithm TEXT,                     -- 'Caesar Cipher + AES-192 CBC'
    iv TEXT,                            -- Empty (embedded in ciphertext)
    shift INTEGER,                      -- AES-256 encrypted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Table: `steganography`

```sql
CREATE TABLE steganography (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    original_image TEXT,                -- AES-256 encrypted
    stego_image TEXT,                   -- AES-256 encrypted
    message TEXT,                       -- AES-256 encrypted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### Table: `file_encryption`

```sql
CREATE TABLE file_encryption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    original_filename TEXT,             -- AES-256 encrypted
    encrypted_filename TEXT,            -- AES-256 encrypted
    algorithm TEXT,                     -- '3DES-192'
    file_size INTEGER,                  -- AES-256 encrypted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## ⚠️ Catatan Penting

### Keamanan

- ✅ Simpan password dengan aman (tidak bisa dipulihkan jika lupa)
- ✅ Backup file penting sebelum enkripsi
- ✅ Untuk steganografi, gunakan PNG (lossless compression)
- ✅ JPG tidak disarankan untuk steganografi (lossy compression merusak LSB)
- ✅ Caesar Cipher shift harus diingat untuk dekripsi
- ✅ Password 3DES file encryption harus disimpan dengan aman
- ✅ Database encryption key: `CamoCrypt217219!@SecretKey`

### Limitasi

- **Caesar Cipher:** Rentan terhadap frequency analysis (untuk pembelajaran)
- **Steganografi:**
  - JPG compression dapat merusak data tersembunyi
  - Resize/crop gambar akan merusak pesan
  - Hanya PNG yang aman
- **3DES:**
  - Legacy algorithm (AES lebih modern)
  - Block size 64-bit dianggap kecil
  - Lebih lambat dari AES
- **File Encryption:** Password hilang = data tidak bisa didekripsi

## 📚 Referensi

1. **Buku:**

   - William Stallings - "Cryptography and Network Security"
   - Bruce Schneier - "Applied Cryptography"
   - Alfred J. Menezes - "Handbook of Applied Cryptography"

2. **Standar:**

   - NIST FIPS 197 (AES)
   - NIST FIPS 180-4 (SHA-256)
   - NIST FIPS 46-3 (3DES)
   - RFC 2898 (PBKDF2)

3. **Dokumentasi:**

   - [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/)
   - [Streamlit Documentation](https://docs.streamlit.io/)
   - [NumPy Documentation](https://numpy.org/doc/)

4. **Papers:**
   - LSB Steganography Research Papers (IEEE Xplore)
   - Password Hashing Competition (Argon2 winner)

## 🎓 Informasi Akademik

**Mata Kuliah:** Kriptografi  
**Semester:** 5  
**Tahun Akademik:** 2024/2025  
**Institusi:** [Nama Universitas]

## 👥 Kontributor

**Nama Mahasiswa:**

- **[Nama Lengkap]**
  - NIM: [NIM]
  - GitHub: [ikhsan-fillah](https://github.com/ikhsan-fillah)
  - Email: [email]

## 🔗 Links

- 📖 [Penjelasan Algoritma Detail](PENJELASAN_ALGORITMA.md)
- 🚀 [Quick Start Guide](QUICKSTART.md)
- 📘 [Usage Guide](USAGE_GUIDE.md)
- 🐙 [GitHub Repository](https://github.com/ikhsan-fillah/Project_Akhir_Kriptografi)

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik dan pembelajaran.

## 🤝 Kontribusi

Jika menemukan bug atau ingin menambahkan fitur:

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## 📧 Kontak

Untuk pertanyaan atau feedback:

- GitHub: [@ikhsan-fillah](https://github.com/ikhsan-fillah)
- Repository: [Project_Akhir_Kriptografi](https://github.com/ikhsan-fillah/Project_Akhir_Kriptografi)

---

**© 2025 - CamoCrypt**  
_Dibuat dengan ❤️ untuk pendidikan keamanan informasi_

🔐 Caesar + AES-192 | 🖼️ LSB Steganografi | 📁 3DES-192 | 🔒 AES-256 DB | 🔑 SHA-256 + Salt
