import streamlit as st
from database import Database


def show_login():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1>🔐 CamoCrypt</h1>
            <p style='color: #666; font-size: 1.1rem;'>Secure Message & File Encryption</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input(
                "Username",
                placeholder="Masukkan username",
                key="login_username"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Masukkan password",
                key="login_password"
            )
            
            submit = st.form_submit_button("🔓 Login", use_container_width=True, type="primary")
            
            if submit:
                if username and password:
                    db = Database()
                    success, user_data = db.verify_user(username, password)
                    
                    if success and user_data:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_id = user_data['user_id']
                        st.session_state.full_name = user_data['full_name']
                        
                        st.success(f"✅ Selamat datang, {user_data['full_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah!")
                else:
                    st.warning("⚠️ Mohon isi semua field!")
    
    with tab2:
        st.subheader("Register")
        
        with st.form("register_form", clear_on_submit=True):
            reg_fullname = st.text_input(
                "Nama Lengkap",
                placeholder="Masukkan nama lengkap",
                key="reg_fullname"
            )
            
            reg_username = st.text_input(
                "Username",
                placeholder="Pilih username",
                key="reg_username"
            )
            
            reg_password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimal 6 karakter",
                key="reg_password"
            )
            
            reg_confirm = st.text_input(
                "Konfirmasi Password",
                type="password",
                placeholder="Ulangi password",
                key="reg_confirm"
            )
            
            register = st.form_submit_button("✨ Buat Akun", use_container_width=True, type="primary")
            
            if register:
                if reg_fullname and reg_username and reg_password and reg_confirm:
                    if len(reg_password) < 6:
                        st.error("❌ Password minimal 6 karakter!")
                    elif reg_password != reg_confirm:
                        st.error("❌ Password tidak cocok!")
                    else:
                        db = Database()
                        success, message = db.register_user(reg_username, reg_password, reg_fullname)
                        
                        if success:
                            st.success("✅ " + message)
                        else:
                            st.error("❌ " + message)
                else:
                    st.warning("⚠️ Mohon isi semua field!")


def show_footer():
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p><strong>CamoCrypt</strong> - Secure Encryption System</p>
            <p style='font-size: 0.9rem;'>© 2025 All Rights Reserved</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # demo/testing removed for production
    pass
