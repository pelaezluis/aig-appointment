import streamlit as st

from components.home import home
from components.login import login_view

def main_view():
    if "access_token" in st.session_state:
        home()
    else:
        st.header("Bloqueo de horarios de citas", divider=True)
        login_view()

main_view()