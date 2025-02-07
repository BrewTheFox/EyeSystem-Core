from nicegui import ui

@ui.page(path="/login", title="Eye System Core")
async def login():
    ui.add_css(""".animated{font-size:120%;
                color: #D98880; 
                background-image: linear-gradient(45deg, #D98880 45%, #C74375 96%, #912D5E 86%, #5A1846 68%); 
                background-clip: text; 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                }
            }""")
    with ui.row().style("width:100%; text-align: center; display: flex; justify-content: center;"):
        ui.html('<h1>Eye System <span class="animated">Core<span><h1>').style("margin-top: 5%; font-size:200%;")
    with ui.row().style("display: flex; justify-content: center; text-align: center; width: 100%;"):
        with ui.card().style("width: 25%; text-align: center; margin-top: 5%;"):
            ui.label("Inicio de sesion.").style("width:100%; font-size: 150%")
            ui.input("Usuario:").style("width:100%")
            ui.input("Contraseña:").style("width:100%")
            ui.button("Iniciar Sesion").style("width:100%")
    ui.label("Eye System Version Core por @BrewTheFox").style("color:grey; position:absolute; top:95%")