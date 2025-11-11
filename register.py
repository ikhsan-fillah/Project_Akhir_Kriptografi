import streamlit as st
from database import Database


def show_register():
    st.title("📝 Registrasi Akun Baru")
    st.markdown("---")
    
    with st.form("register_form"):
        full_name = st.text_input(
            "Nama Lengkap",
            placeholder="Masukkan nama lengkap Anda"
        )
        
        username = st.text_input(
            "Username",
            placeholder="Pilih username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimal 6 karakter"
        )
        
        confirm_password = st.text_input(
            "Konfirmasi Password",
            type="password",
            placeholder="Ulangi password"
        )
        
        submit = st.form_submit_button("✨ Daftar", use_container_width=True, type="primary")
        
        if submit:
            if not all([full_name, username, password, confirm_password]):
                st.error("❌ Semua field harus diisi!")
            elif len(password) < 6:
                st.error("❌ Password minimal 6 karakter!")
            elif password != confirm_password:
                st.error("❌ Password dan konfirmasi tidak cocok!")
            else:
                db = Database()
                success, message = db.register_user(username, password, full_name)
                
                if success:
                    st.success("✅ Registrasi berhasil!")
                else:
                    st.error(f"❌ {message}")


if __name__ == "__main__":
    pass
