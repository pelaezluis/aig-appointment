import httpx
import streamlit as st

URL_BASE = "https://apiaig4u.portalaig.com/api/v1"

def get_schedule():
    TOKEN: str = st.session_state["access_token"]
    url = f"{URL_BASE}/medical_appointment_scheduler/scheduler_appointment"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Error en la petición: {e.response.status_code}")
        return {}


def create_schedule(day: str, hours: list):
    TOKEN: str = st.session_state["access_token"]
    url = f"{URL_BASE}/medical_appointment_scheduler/scheduler_create"
    headers = {"Authorization": f"Bearer {TOKEN}"}

    try:
        for hour in hours:
            data = {"day": day, "hour": hour}
            response = httpx.post(url, headers=headers, json=data)
            response.raise_for_status()
            st.toast(f"{day} - {hour} activado exitosamente", icon="✅")
            st.success(f"{day} - {hour} activado exitosamente", icon="✅")
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Error en la petición: {e.response.status_code}")
        return {}


def update_schedule(id: int):
    TOKEN: str = st.session_state["access_token"]
    url = f"{URL_BASE}/medical_appointment_scheduler/scheduler_update/{id}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = httpx.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Error en la petición: {e.response.status_code}")
        return {}


def delete_schedules_bulk(ids: list):
    """Elimina múltiples horarios en grupo"""
    TOKEN: str = st.session_state["access_token"]
    headers = {"Authorization": f"Bearer {TOKEN}"}
    deleted_count = 0
    
    for id in ids:
        url = f"{URL_BASE}/medical_appointment_scheduler/scheduler_update/{id}"
        try:
            response = httpx.delete(url, headers=headers)
            response.raise_for_status()
            deleted_count += 1
        except httpx.HTTPStatusError as e:
            print(f"Error eliminando id {id}: {e.response.status_code}")
    
    return {"deleted": deleted_count, "total": len(ids)}