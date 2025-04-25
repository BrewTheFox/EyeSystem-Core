from nicegui import ui, app
import dbmanager
from asyncio import sleep as async_wait

@ui.page(path="/login", title="Eye System Core")
async def login():
    async def managelogin(username:str, password:str):
        data = dbmanager.checklogin(username, password)
        ui.notify(data["status"], color=data["color"])
        if data["type"] == "success":
            app.storage.user.update({"username":username, "role": data["role"], "authenticated":True})
            await async_wait(2)
            ui.navigate.to("/")
    ui.add_css(""".gradient{font-size:120%;
                color: #D98880; 
                background-image: linear-gradient(45deg, #D98880 45%, #C74375 96%, #912D5E 86%, #5A1846 68%); 
                background-clip: text; 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                }
            }""")
    with ui.row().style("width:100%; text-align: center; display: flex; justify-content: center;"):
        ui.html('<h1>Eye System <span class="gradient">Core<span><h1>').style("margin-top: 5%; font-size:200%;")
    with ui.row().style("display: flex; justify-content: center; text-align: center; width: 100%;"):
        with ui.card().style("width: 25%; text-align: center; margin-top: 5%;"):
            ui.label("Inicio de sesion.").style("width:100%; font-size: 150%")
            username = ui.input("Usuario:").style("width:100%")
            password = ui.input("Contraseña:", password=True).style("width:100%")
            ui.button("Iniciar Sesion", on_click=lambda:managelogin(username.value, password.value)).style("width:100%")
    ui.label("Eye System Version Core por @BrewTheFox").style("color:grey; position:absolute; top:95%")