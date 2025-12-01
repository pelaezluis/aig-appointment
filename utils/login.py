import httpx
import streamlit as st

URL_BASE = "https://apiaig4u.portalaig.com/api/v1"


def check_login(username, password):
    """Check if the user and password are correct"""
    try:
        url = f"{URL_BASE}/login/access-token"
        data = {"username": username, "password": password}
        response = httpx.post(url, data=data)
        response.raise_for_status()
        st.session_state["access_token"] = response.json()['access_token']
        st.success("Iniciando sesión", icon=":material/verified_user:")
        st.rerun()
        
    except httpx.HTTPStatusError as e:
        print(f"Error en la petición: {e.response.status_code}")
        st.error("Usuario y/o contraseña incorrectos", icon=":material/gpp_bad:")

