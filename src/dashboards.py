from nicegui import ui, app
import numpy as np
from random import randint
import navbars
@ui.page("/admin_dashboard", title="Dashboard")
async def admin_dashboard():
    navbars.adminnavbar()
    with ui.card().style("width:100%"):
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.label(f"Estudiantes: {randint(1,100)}").style("font-size:200%")
            ui.label(f"Registros de hoy: {randint(1,100)}").style("font-size:200%;")

    with ui.row().style("display: flex; align-items: center; justify-content: center; width:100%"):
        with ui.matplotlib(figsize=(7, 4)).figure as fig:
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            ax = fig.gca()
            ax.plot(x, y, '-')

        with ui.matplotlib(figsize=(7, 4)).figure as fig:
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            ax = fig.gca()
            ax.plot(x, y, '-')

    with ui.row().style("display: flex; align-items: center; justify-content: center; width:100%"):
        with ui.matplotlib(figsize=(7, 4)).figure as fig:
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            ax = fig.gca()
            ax.plot(x, y, '-')

@ui.page("/user_dashboard")
async def user_dashboard():
    navbars.usernavbar()
    with ui.card().style("width:100%"):
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.label(f"Estudiantes: {randint(1,100)}").style("font-size:200%")
            ui.label(f"Registros de hoy: {randint(1,100)}").style("font-size:200%;")

    with ui.row().style("display: flex; align-items: center; justify-content: center; width:100%"):
        with ui.matplotlib(figsize=(7, 4)).figure as fig:
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            ax = fig.gca()
            ax.plot(x, y, '-')

        with ui.matplotlib(figsize=(7, 4)).figure as fig:
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            ax = fig.gca()
            ax.plot(x, y, '-')

    with ui.row().style("display: flex; align-items: center; justify-content: center; width:100%"):
        with ui.matplotlib(figsize=(7, 4)).figure as fig:
            x = np.linspace(0.0, 5.0)
            y = np.cos(2 * np.pi * x) * np.exp(-x)
            ax = fig.gca()
            ax.plot(x, y, '-')

