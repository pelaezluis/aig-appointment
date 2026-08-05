# AIG Appointment

Aplicación para la gestión de horarios de citas (activación y desactivación) usando Streamlit.

## Requisitos

- [uv](https://docs.astral.sh/uv/) como gestor de paquetes
- Python 3.13 (definido en `.python-version`)

## Instalación

```bash
uv sync
```

Esto crea el entorno virtual e instala las dependencias declaradas en `pyproject.toml` (definidas en `uv.lock`).

## Ejecución

```bash
uv run streamlit run app.py
```

O con make:

```bash
make run
```

## Estructura

```
app.py                 # Punto de entrada
components/
  home.py              # Vista principal (horarios)
  login.py             # Vista de inicio de sesión
utils/
  login.py             # Llamada a la API para autenticación
  request.py           # Llamadas a la API (crear/obtener/eliminar horarios)
```

## Notas

- La aplicación consume la API en `https://apiaig4u.portalaig.com/api/v1`.
- Los datos de autenticación se solicitan en la vista de login y el token se guarda en la sesión de Streamlit.
