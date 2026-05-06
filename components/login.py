import streamlit as st

from utils.login import check_login


def login_view():
    # st.header("Iniciar sesión", divider=True)
    with st.form(key="login_form"):
        user = st.text_input(
            label="user", label_visibility="hidden", placeholder="Usuario"
        )
        password = st.text_input(
            label="password",
            label_visibility="hidden",
            type="password",
            placeholder="Contraseña",
        )
        if st.form_submit_button("Iniciar sesión", icon=":material/login:"):
            check_login(user, password)
