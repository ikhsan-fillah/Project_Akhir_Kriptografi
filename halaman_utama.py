import streamlit as st
from database import Database
from crypto_text import SuperEncryption
from crypto_image import ImageSteganography
from crypto_file import TripleDESFileEncryption
import tempfile
import os


def show_sidebar():
    with st.sidebar:
        st.title("🔐 Menu Utama")
        
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                <p style='margin:0; font-size: 0.9rem;'>👤 <strong>{st.session_state.full_name}</strong></p>
                <p style='margin:0; font-size: 0.8rem; opacity: 0.9;'>@{st.session_state.username}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        
        menu = st.radio(
            "Pilih Fitur:",
            [
                "🏠 Dashboard",
                "💬 Enkripsi Text",
                "🖼️ Steganografi Gambar",
                "📁 Enkripsi File",
                "📊 Riwayat"
            ],
            key="main_menu"
        )
        
        st.markdown("---")
        
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_id = None
            st.session_state.full_name = None
            st.rerun()
        
        st.markdown("---")
        st.caption("© 2025 CamoCrypt")
    
    return menu


def show_dashboard():
    st.title("🏠 Dashboard")
    st.markdown("### Selamat Datang di CamoCrypt!")
    st.markdown("---")
    
    db = Database()
    stats = db.get_user_statistics(st.session_state.user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 Enkripsi Text", stats['text_encryptions'])
    with col2:
        st.metric("🖼️ Steganografi", stats['steganography'])
    with col3:
        st.metric("📁 Enkripsi File", stats['file_encryptions'])
    with col4:
        st.metric("📊 Total Aktivitas", stats['total'])
    
    st.markdown("---")
    
    st.markdown("### 🔒 Fitur Keamanan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            #### 1. 💬 Super Enkripsi Text
            **Algoritma:** Caesar Cipher + AES-192 CBC
            - Double layer encryption
            - Caesar Cipher (klasik)
            - AES-192 CBC (modern)
            - Passphrase-protected
            - IV embedded dalam ciphertext
            
            #### 2. 🖼️ Steganografi Gambar
            **Metode:** LSB (Least Significant Bit)
            - Sembunyikan pesan dalam gambar
            - Tidak terlihat secara visual
            - Support PNG, JPG, BMP
            - Kapasitas tergantung ukuran gambar
        """)
    
    with col2:
        st.markdown("""
            #### 3. 📁 Enkripsi File 3DES
            **Algoritma:** 3DES-192
            - Triple Data Encryption Standard
            - 192-bit key, 64-bit block
            - Password-based encryption
            - Support semua jenis file
            
            #### 4. 🔐 Autentikasi Aman
            **Hash:** SHA-256 dengan Salt
            - Password hashing dengan salt
            - Salt unik per user
            - One-way function
            - Collision resistant
            - Database SQLite
        """)


def show_text_encryption():
    st.title("💬 Super Enkripsi Text")
    st.markdown("**Algoritma:** Caesar Cipher + AES-192 CBC")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔒 Enkripsi", "🔓 Dekripsi"])
    
    
    with tab1:
        st.subheader("Enkripsi Pesan")
        
        plaintext = st.text_area(
            "Pesan yang akan dienkripsi:",
            height=150,
            placeholder="Ketik atau paste pesan di sini..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            shift = st.slider("Caesar Cipher Shift:", 1, 25, 5)
        with col2:
            password = st.text_input("Passphrase AES:", type="password", placeholder="Passphrase untuk enkripsi")
        
        if st.button("🔒 Enkripsi", type="primary", use_container_width=True):
            if plaintext and password:
                try:
                    crypto = SuperEncryption(shift=shift)
                    result = crypto.encrypt(plaintext, password)
                    
                    st.success("✅ Enkripsi berhasil!")
                    
                    st.text_area("Ciphertext:", value=result['ciphertext'], height=100)

                    db = Database()
                    db.save_text_encryption(
                        st.session_state.user_id,
                        plaintext,
                        result['ciphertext'],
                        result['algorithm'],
                        result['iv'],
                        result['shift']
                    )
                    txt_content = (
                        f"Shift: {shift}\n"
                        f"Password: {password}\n"
                        f"Ciphertext: {result['ciphertext']}\n"
                    )

                    st.download_button(
                        label="💾 Download Key (.txt)",
                        data=txt_content,
                        file_name="encryption_key.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            else:
                st.warning("⚠️ Mohon isi pesan dan passphrase!")
    
    
    with tab2:
        st.subheader("Dekripsi Pesan")
        
        ciphertext = st.text_area(
            "Ciphertext:",
            height=100,
            placeholder="Paste ciphertext di sini..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            shift_dec = st.slider("Caesar Cipher Shift:", 1, 25, 5, key="shift_dec")
        with col2:
            password_dec = st.text_input("Passphrase AES:", type="password", placeholder="Passphrase untuk dekripsi", key="pass_dec")
        
        if st.button("🔓 Dekripsi", type="primary", use_container_width=True):
            if ciphertext and password_dec:
                try:
                    crypto = SuperEncryption(shift=shift_dec)
                    plaintext = crypto.decrypt(ciphertext, password_dec)
                    
                    st.success("✅ Dekripsi berhasil!")
                    st.text_area("Pesan Asli:", value=plaintext, height=150)

                    from datetime import datetime
                    decryption_time = datetime.utcnow().isoformat() + "Z"
                    txt_content = (
                        f"Plaintext: {plaintext}\n"
                        f"Ciphertext: {ciphertext}\n"
                        f"Shift: {shift_dec}\n"
                        f"Passphrase: {password_dec}\n"
                        f"DecryptionTime(UTC): {decryption_time}\n"
                    )

                    st.download_button(
                        label="💾 Download Hasil Dekripsi (.txt)",
                        data=txt_content,
                        file_name="decryption_result.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Dekripsi gagal! Pastikan ciphertext, passphrase, dan shift benar.")
                    st.error(f"Error: {str(e)}")
            else:
                st.warning("⚠️ Mohon isi semua field!")


def show_steganography():
    st.title("🖼️ Steganografi Gambar")
    st.markdown("**Metode:** LSB (Least Significant Bit) Embedding")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["📥 Sembunyikan Pesan", "📤 Ekstrak Pesan"])
    
    
    with tab1:
        st.subheader("Sembunyikan Pesan dalam Gambar")
        
        uploaded_image = st.file_uploader(
            "Upload gambar cover:",
            type=['png', 'jpg', 'jpeg', 'bmp'],
            key="cover_image"
        )
        
        if uploaded_image:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(uploaded_image, caption="Gambar Cover", use_container_width=True)
                
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                    tmp.write(uploaded_image.getvalue())
                    tmp_path = tmp.name
                
                stego = ImageSteganography()
                max_chars, width, height, total_pixels = stego.calculate_capacity(tmp_path)
                
                st.info(f"""
                    📊 **Informasi Gambar:**
                    - Ukuran: {width} x {height} px
                    - Total pixels: {total_pixels:,}
                    - Kapasitas pesan: ~{max_chars:,} karakter
                """)
            
            with col2:
                message = st.text_area(
                    "Pesan rahasia:",
                    height=200,
                    placeholder="Ketik pesan yang akan disembunyikan...",
                    max_chars=max_chars if max_chars > 0 else None
                )
                
                if message:
                    st.caption(f"Panjang pesan: {len(message)} / {max_chars} karakter")
                
                if st.button("🔒 Sembunyikan Pesan", type="primary", use_container_width=True):
                    if message:
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as output_tmp:
                                output_path = output_tmp.name
                            
                            success, msg = stego.embed_message(tmp_path, message, output_path)
                            
                            if success:
                                st.success(f"✅ {msg}")

                                st.image(output_path, caption="Stego Image (Gambar dengan Pesan Tersembunyi)", 
                                        use_container_width=True)
                                db = Database()
                                db.save_steganography(
                                    st.session_state.user_id,
                                    uploaded_image.name,
                                    "stego_image.png",
                                    message
                                )

                                with open(output_path, 'rb') as f:
                                    st.download_button(
                                        label="💾 Download Stego Image",
                                        data=f.read(),
                                        file_name="stego_image.png",
                                        mime="image/png",
                                        use_container_width=True
                                    )
                            else:
                                st.error(f"❌ {msg}")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    else:
                        st.warning("⚠️ Masukkan pesan terlebih dahulu!")

    with tab2:
        st.subheader("Ekstrak Pesan dari Stego Image")
        
        uploaded_stego = st.file_uploader(
            "Upload stego image:",
            type=['png'],
            key="stego_image"
        )
        
        if uploaded_stego:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(uploaded_stego, caption="Stego Image", use_container_width=True)
            
            with col2:
                if st.button("🔓 Ekstrak Pesan", type="primary", use_container_width=True):
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                            tmp.write(uploaded_stego.getvalue())
                            tmp_path = tmp.name
                        
                        stego = ImageSteganography()
                        success, message = stego.extract_message(tmp_path)
                        
                        if success:
                            st.success("✅ Pesan berhasil diekstrak!")
                            st.text_area("Pesan Tersembunyi:", value=message, height=200)
                            
                            st.download_button(
                                label="💾 Download Pesan (TXT)",
                                data=message,
                                file_name="extracted_message.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        else:
                            st.error(f"❌ {message}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")


def show_file_encryption():
    st.title("📁 Enkripsi File dengan 3DES")
    st.markdown("**Algoritma:** 3DES-192 (Triple Data Encryption Standard)")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔒 Enkripsi", "🔓 Dekripsi"])
    
    
    with tab1:
        st.subheader("Enkripsi File")
        
        uploaded_file = st.file_uploader("Upload file yang akan dienkripsi:", type=None, key="file_enc")
        
        if uploaded_file:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info(f"""
                    📄 **Informasi File:**
                    - Nama: {uploaded_file.name}
                    - Ukuran: {len(uploaded_file.getvalue()) / 1024:.2f} KB
                    - Tipe: {uploaded_file.type or 'Unknown'}
                """)
            
            with col2:
                password_enc = st.text_input(
                    "Password:",
                    type="password",
                    placeholder="Masukkan password",
                    key="pass_enc"
                )
                
                if st.button("🔒 Enkripsi File", type="primary", use_container_width=True):
                    if password_enc:
                        try:
                            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                                tmp.write(uploaded_file.getvalue())
                                tmp_path = tmp.name
                            
                            des3 = TripleDESFileEncryption()
                            success, msg, output_path = des3.encrypt_file(
                                tmp_path,
                                password_enc
                            )
                            
                            if success and output_path:
                                st.success(f"✅ {msg}")
                                with open(output_path, 'rb') as f:
                                    encrypted_data = f.read()

                                db = Database()
                                db.save_file_encryption(
                                    st.session_state.user_id,
                                    uploaded_file.name,
                                    uploaded_file.name + ".encrypted",
                                    "3DES-192",
                                    len(encrypted_data)
                                )
                                
                                st.download_button(
                                    label="💾 Download File Terenkripsi",
                                    data=encrypted_data,
                                    file_name=f"{uploaded_file.name}.encrypted",
                                    mime="application/json",
                                    use_container_width=True
                                )
                                
                                st.warning("⚠️ **PENTING:** Simpan password dengan aman untuk dekripsi!")
                            else:
                                st.error(f"❌ {msg}")
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
                    else:
                        st.warning("⚠️ Masukkan password terlebih dahulu!")
    
    
    with tab2:
        st.subheader("Dekripsi File")
        
        uploaded_encrypted = st.file_uploader(
            "Upload file terenkripsi (.encrypted):",
            type=['encrypted'],
            key="file_dec"
        )
        
        if uploaded_encrypted:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.info(f"""
                    📄 **Informasi File:**
                    - Nama: {uploaded_encrypted.name}
                    - Ukuran: {len(uploaded_encrypted.getvalue()) / 1024:.2f} KB
                """)
            
            with col2:
                password_dec = st.text_input(
                    "Password:",
                    type="password",
                    placeholder="Masukkan password",
                    key="pass_dec"
                )
                
                if st.button("🔓 Dekripsi File", type="primary", use_container_width=True):
                    if password_dec:
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.encrypted', mode='w') as tmp:
                                tmp.write(uploaded_encrypted.getvalue().decode('utf-8'))
                                tmp_path = tmp.name
                            
                            des3 = TripleDESFileEncryption()
                            success, msg, output_path = des3.decrypt_file(
                                tmp_path,
                                password_dec
                            )
                            
                            if success:
                                st.success(f"✅ {msg}")
                                with open(output_path, 'rb') as f:
                                    decrypted_data = f.read()
                                original_name = uploaded_encrypted.name
                                if original_name.endswith('.encrypted'):
                                    original_name = original_name[:-10]
                                st.download_button(
                                    label="💾 Download File Terdekripsi",
                                    data=decrypted_data,
                                    file_name=original_name,
                                    mime="application/octet-stream",
                                    use_container_width=True
                                )
                            else:
                                st.error(f"❌ {msg}")
                        
                        except Exception as e:
                            st.error(f"❌ Dekripsi gagal! Pastikan file dan password benar.")
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Masukkan password terlebih dahulu!")



def show_history():
    st.title("📊 Riwayat Aktivitas")
    st.markdown("---")
    
    db = Database()

    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Enkripsi Text",
        "🖼️ Steganografi",
        "📁 Enkripsi File",
        "📈 Statistik"
    ])
    
    with tab1:
        st.subheader("Riwayat Enkripsi Text")
        history = db.get_text_encryption_history(st.session_state.user_id)
        
        if history:
            for idx, item in enumerate(history):
                with st.expander(f"📝 {item['created_at']} - {item['algorithm']}"):
                    st.text_area("Plaintext:", value=item['plaintext'], height=80, disabled=True, key=f"text_plain_{idx}")
                    st.text_area("Ciphertext:", value=item['ciphertext'], height=80, disabled=True, key=f"text_cipher_{idx}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"🔄 Shift: {item['shift']}")
                    with col2:
                        st.info(f"🔑 IV: {item['iv'][:20]}...")
        else:
            st.info("Belum ada riwayat enkripsi text.")
    
    with tab2:
        st.subheader("Riwayat Steganografi")
        history = db.get_steganography_history(st.session_state.user_id)
        
        if history:
            for idx, item in enumerate(history):
                with st.expander(f"🖼️ {item['created_at']} - {item['stego_image']}"):
                    st.write(f"**Original Image:** {item['original_image']}")
                    st.write(f"**Stego Image:** {item['stego_image']}")
                    st.text_area("Message:", value=item['message'], height=80, disabled=True, key=f"stego_msg_{idx}")
        else:
            st.info("Belum ada riwayat steganografi.")
    
    with tab3:
        st.subheader("Riwayat Enkripsi File")
        history = db.get_file_encryption_history(st.session_state.user_id)
        
        if history:
            for idx, item in enumerate(history):
                with st.expander(f"📁 {item['created_at']} - {item['original_filename']}"):
                    st.write(f"**File Asli:** {item['original_filename']}")
                    st.write(f"**File Enkripsi:** {item['encrypted_filename']}")
                    st.write(f"**Algoritma:** {item['algorithm']}")
                    try:
                        file_size = float(item['file_size']) if item['file_size'] else 0
                        st.write(f"**Ukuran:** {file_size / 1024:.2f} KB")
                    except (ValueError, TypeError):
                        st.write(f"**Ukuran:** N/A")
        else:
            st.info("Belum ada riwayat enkripsi file.")
    
    with tab4:
        st.subheader("Statistik Pengguna")
        stats = db.get_user_statistics(st.session_state.user_id)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💬 Enkripsi Text", stats['text_encryptions'])
            st.metric("🖼️ Steganografi", stats['steganography'])
        
        with col2:
            st.metric("📁 Enkripsi File", stats['file_encryptions'])
            st.metric("📊 Total Aktivitas", stats['total'])


def main():
    if not st.session_state.get('logged_in', False):
        st.warning("⚠️ Anda belum login!")
        st.stop()

    menu = show_sidebar()

    if menu == "🏠 Dashboard":
        show_dashboard()
    elif menu == "💬 Enkripsi Text":
        show_text_encryption()
    elif menu == "🖼️ Steganografi Gambar":
        show_steganography()
    elif menu == "📁 Enkripsi File":
        show_file_encryption()
    elif menu == "📊 Riwayat":
        show_history()


if __name__ == "__main__":
    pass
