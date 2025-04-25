from nicegui import ui, app
import numpy as np
from random import randint
from dbmanager import getuserquantity, getassistancequantity, changepassword
import navbars

@ui.page("/admin_dashboard", title="Dashboard")
async def admin_dashboard():
    navbars.adminnavbar()
    with ui.card().style("width:100%"):
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.label(f"Estudiantes: {getuserquantity()}").style("font-size:200%")
            ui.label(f"Registros de hoy: {getassistancequantity()}").style("font-size:200%;")

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

@ui.page("/user_dashboard", title="Dashboard")
async def user_dashboard():
    navbars.usernavbar()
    with ui.card().style("width:100%"):
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.label(f"Estudiantes: {getuserquantity()}").style("font-size:200%")
            ui.label(f"Registros de hoy: {getassistancequantity()}").style("font-size:200%;")

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

@ui.page("/changepassword", title="Cambiar Contraseña")
async def changeform():
    def handlepasswordchange(actual:str, nueva:str, usuario:str):
        if len(nueva) < 8:
            ui.notification('La contraseña tiene menos de 8 caracteres', color="red")
            return
        if nueva == actual:
            ui.notification('Ambas contraseñas son iguales', color="red")
            return
        datos = changepassword(username=usuario, new=nueva, current=actual)
        ui.notification(datos["status"], color=datos["color"])
        
    if app.storage.user["role"] == 1:
        navbars.adminnavbar()
    else:
        navbars.usernavbar()
    with ui.row().style("width:100%; text-align: center; display: flex; justify-content: center;"):
        with ui.card():
            ui.label("Cambiar contraseña.").style("font-size:25px")
            actual = ui.input("Contraseña Actual:", password=True).style("width:100%")
            nueva = ui.input("Contraseña Nueva:", password=True).style("width:100%")
            ui.button("Cambiar", on_click=lambda: handlepasswordchange(actual.value, nueva.value, app.storage.user["username"])).style("width:100%")
