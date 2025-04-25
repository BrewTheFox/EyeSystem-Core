from nicegui import ui, app
import navbars
import datetime
from dbmanager import getcursos, getasistance, getjornadas

@ui.page("/asistance_list")
async def AsistanceList():
    if app.storage.user["role"] == 1:
        navbars.adminnavbar()
    else:
        navbars.usernavbar()
    cursos = {}
    jornadas = {}
    for curso in getcursos():
        cursos[curso[0]] = curso
    for jornada in getjornadas():
        jornadas[jornada[0]] = jornada
    with ui.dialog() as dialog:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        date = ui.date(value=date)
    with ui.row().style("width:100%; text-align: center; display: flex; justify-content: center;"):
        with ui.card().style("width:80%"):
            ui.label("Lista de asistencia").style("font-size:25px")
            with ui.row().style("width:100%; text-align: center; display: flex; justify-content: center;"):
                grade = ui.select(options=cursos, value=list(cursos.keys())[0])
                studytime = ui.select(options=jornadas, value=list(jornadas.keys())[0])
            ui.button("Seleccionar Fecha", on_click=lambda:dialog.open()).style("width:100%")
            ui.button("Buscar", on_click=lambda: updatetable(getasistance(grade.value, studytime.value, date.value))).style("width:100%")
            columns = [{'name':"Nombre", "label":"Nombre", "field":"Nombre"}, {'name':"Hora", "label":"Hora", "field":"Hora"}]
            rows = []
            table = ui.table(columns=columns, rows=rows).style("width:100%")
        @ui.refreshable
        def updatetable(information:tuple):
            rows = []
            for person in information:
                rows.append({"Nombre":f"{person[0]} {person[1]}", "Hora":person[2]})
            table.rows = rows
