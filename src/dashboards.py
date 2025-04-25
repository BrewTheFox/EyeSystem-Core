from nicegui import ui, app
import numpy as np
from random import randint
from dbmanager import getuserquantity, getassistancequantity, changepassword, getjornadas, getasistenciajornada, getcursos, getasistenciacurso
from pyecharts.charts import Pie, Bar
import navbars

@ui.page("/dashboard", title="Dashboard")
async def dashboard():
    if app.storage.user["role"] == 1:
        navbars.adminnavbar()
    else:
        navbars.usernavbar()
    with ui.card().style("width:100%"):
        with ui.row().style("justify-content: space-between; width: 100%"):
            ui.label(f"Estudiantes: {getuserquantity()}").style("font-size:200%")
            ui.label(f"Registros de hoy: {getassistancequantity()}").style("font-size:200%;")

    with ui.row().style("display: flex; align-items: center; justify-content: center; width:100%"):
        xaxisCursos = []
        yaxisCursos = []
        for curso in getcursos():
            xaxisCursos.append(curso[0])
            yaxisCursos.append(getasistenciacurso(curso[0]))

        ui.echart.from_pyecharts(Bar().add_xaxis(xaxisCursos).add_yaxis("Asistencias", [1])).style("width:40%; height:400%")
        asistanceDataStudyTime = []
        for jornada in getjornadas():
            asistanceDataStudyTime.append([jornada[0], getasistenciajornada(jornada)])
        ui.echart.from_pyecharts(Pie().add("", asistanceDataStudyTime)).style("width:50%")
    ui.label("Eye System Version Core por @BrewTheFox").style("color:grey; position:absolute; top:95%")


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
