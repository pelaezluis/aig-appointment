import pandas as pd
import streamlit as st
import os
from time import sleep

os.system("cls")

from utils.request import create_schedule, get_schedule, update_schedule


def home():
    # Obtener datos
    response = get_schedule()
    # print(response, 'en home')
    day_list = response["meta"]["day"]
    schedule = pd.DataFrame(response["data"])
    schedule["day_name"] = schedule["day"].apply(lambda x: day_list[x])
    schedule["disabled"] = schedule["disabled"].apply(lambda x: not x)
    dates = schedule.groupby("day")
    schedule.columns = ["id", "Numero Día", "Hora", "Estado", "Día"]
    hours = ["09:00:00", "09:30:00", "10:00:00", "10:30:00"]

    # Crear horarios
    create_schedule_view(hours)
    st.container(height=100, border=False)
    with st.container(border=True):
        st.header("Desactivar horarios de citas", divider=True)   
        # Crear filas y columnas
        row1 = st.columns(2)
        row2 = st.columns(2)
        row3 = st.columns(2)
        groups = list(dates.groups.keys())
        c = 0
        keys = []

        # Mostrar tablas por día
        
        for col in row1 + row2 + row3:
            if c >= len(groups):
                break

            day_from_group = groups[c]
            key = f"data_{day_from_group}"
            keys.append(key)

            container = col.container()
            container.title(day_list[day_from_group])

            # Obtener solo las filas del día específico
            group_data = dates.get_group(day_from_group).reset_index(drop=True)

            # Editor de datos
            df = container.data_editor(
                group_data[["id", "Día", "Hora", "Estado"]], hide_index=True, key=key
            )

            to_delete = df[df["Estado"] == False]
            if len(to_delete["id"].tolist()) == 0:
                pass
            else:
                id = to_delete["id"].tolist()[0]
                update_schedule(id=id)
                st.rerun()
            c += 1
        


def create_schedule_view(hours: list):
    with st.container(border=True):
        st.header("Activar horarios de citas", divider=True)
        day_option = st.selectbox(
            label="Escoge el día de la semana",
            label_visibility="hidden",
            options=("Lunes", "Martes", "Miercoles", "Jueves", "Viernes"),
        )
        hour_options = st.multiselect(
            label="Selecciona un horario",
            placeholder="Selecciona los horarios",
            label_visibility="hidden",
            options=hours,
        )

        if st.button("Activar horarios"):
            create_schedule(day_option, hour_options)
            sleep(2)
            st.rerun()




