import streamlit as st
from database import Database

import login as login
import halaman_utama as halaman_utama


def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'full_name' not in st.session_state:
        st.session_state.full_name = None


def main():
    st.set_page_config(
        page_title="CamoCrypt",
        page_icon="🔐",
        layout="centered"
    )

    init_session_state()

    db = Database()

    if not st.session_state.logged_in:
        login.show_login()
        login.show_footer()
    else:
        halaman_utama.main()


if __name__ == "__main__":
    main()
