import pandas as pd
import streamlit as st
import os
from time import sleep

os.system("cls")

from utils.request import create_schedule, get_schedule, update_schedule, delete_schedules_bulk


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
    st.container(height=50, border=False)
    
    # Sección de resumen de horarios habilitados por día
    show_schedule_summary(dates, day_list)
    st.container(height=50, border=False)
    
    with st.container(border=True):
        st.header("Desactivar horarios de citas", divider=True)
        
        # Selector de día para eliminación en grupo
        day_options = {day_list[key]: key for key in dates.groups.keys()}
        selected_day_name = st.selectbox(
            label="Selecciona el día para ver y eliminar horarios",
            options=list(day_options.keys()),
            key="day_selector_delete"
        )
        
        if selected_day_name:
            selected_day_key = day_options[selected_day_name]
            group_data = dates.get_group(selected_day_key).reset_index(drop=True)
            
            st.subheader(f"Horarios de {selected_day_name}")
            
            # Verificar si hay que seleccionar todos
            select_all_key = f"select_all_{selected_day_key}"
            should_select_all = st.session_state.get(select_all_key, False)
            
            # Agregar columna de selección para eliminar
            group_data["Seleccionar"] = should_select_all
            
            # Editor de datos con columna de selección
            edited_df = st.data_editor(
                group_data[["id", "Día", "Hora", "Seleccionar"]],
                hide_index=True,
                key=f"delete_editor_{selected_day_key}",
                column_config={
                    "id": st.column_config.NumberColumn("ID", disabled=True),
                    "Día": st.column_config.TextColumn("Día", disabled=True),
                    "Hora": st.column_config.TextColumn("Hora", disabled=True),
                    "Seleccionar": st.column_config.CheckboxColumn("Eliminar", default=False)
                },
                disabled=["id", "Día", "Hora"]
            )
            
            # Obtener IDs seleccionados para eliminar
            selected_to_delete = edited_df[edited_df["Seleccionar"] == True]
            ids_to_delete = selected_to_delete["id"].tolist()
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                # Botón para seleccionar todos
                if st.button("📋 Seleccionar todos", key="select_all"):
                    st.session_state[select_all_key] = True
                    st.rerun()
            
            with col2:
                # Botón para eliminar seleccionados
                if len(ids_to_delete) > 0:
                    if st.button(f"🗑️ Eliminar ({len(ids_to_delete)})", type="primary", key="delete_selected"):
                        result = delete_schedules_bulk(ids_to_delete)
                        st.toast(f"Se eliminaron {result['deleted']} de {result['total']} horarios", icon="✅")
                        # Limpiar selección después de eliminar
                        if select_all_key in st.session_state:
                            del st.session_state[select_all_key]
                        sleep(1)
                        st.rerun()
                else:
                    st.button("🗑️ Eliminar (0)", disabled=True, key="delete_disabled")
            
            with col3:
                if len(ids_to_delete) > 0:
                    st.info(f"📌 {len(ids_to_delete)} horario(s) seleccionado(s) para eliminar")
        


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


def show_schedule_summary(dates, day_list):
    """Muestra un resumen de los horarios habilitados por día en formato tabla"""
    with st.container(border=True):
        st.header("📅 Horarios habilitados por día", divider=True)
        
        # Ordenar días
        day_order = {"Lunes": 0, "Martes": 1, "Miercoles": 2, "Jueves": 3, "Viernes": 4}
        groups = sorted(dates.groups.keys(), key=lambda x: day_order.get(day_list[x], 99))
        
        if len(groups) > 0:
            # Obtener todas las horas únicas y ordenarlas
            all_hours = set()
            day_hours = {}
            
            for day_key in groups:
                day_name = day_list[day_key]
                group_data = dates.get_group(day_key)
                hours_list = [h[:5] if len(h) > 5 else h for h in group_data["Hora"].tolist()]
                day_hours[day_name] = set(hours_list)
                all_hours.update(hours_list)
            
            all_hours = sorted(list(all_hours))
            
            # Crear DataFrame para la tabla
            table_data = []
            for hour in all_hours:
                row = {"Hora": hour}
                for day_key in groups:
                    day_name = day_list[day_key]
                    row[day_name] = "✅" if hour in day_hours[day_name] else "—"
                table_data.append(row)
            
            summary_df = pd.DataFrame(table_data)
            
            # Mostrar resumen con métricas
            cols = st.columns(len(groups))
            for idx, day_key in enumerate(groups):
                day_name = day_list[day_key]
                count = len(day_hours[day_name])
                with cols[idx]:
                    st.metric(label=day_name, value=f"{count} horarios")
            
            st.divider()
            
            # Mostrar tabla estilizada
            st.dataframe(
                summary_df,
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Hora": st.column_config.TextColumn("🕐 Hora", width="small"),
                    **{day_list[dk]: st.column_config.TextColumn(day_list[dk], width="small") for dk in groups}
                }
            )
        else:
            st.info("No hay horarios habilitados actualmente.")




