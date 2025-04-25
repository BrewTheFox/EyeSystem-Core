from nicegui import ui, app

def logout():
    app.storage.user.clear()
    ui.navigate.to("/login")

def adminnavbar():
    ui.add_css(""".gradient{font-size:120%;
                color: #D98880; 
                background-image: linear-gradient(45deg, #D98880 45%, #C74375 96%, #912D5E 86%, #5A1846 68%); 
                background-clip: text; 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                }
    }""")
    with ui.card().style("width:100%; position: sticky; top: 0; overflow: hidden; z-index: 1000;"):
        with ui.row():
            ui.html('<a href="/admin_dashboard">Eye System</a>').style("font-size:150%;")
            ui.html('<a href="/admin_dashboard">Core</a>').style("font-size:150%;").classes("gradient")
            ui.button("Reconocimiento", on_click=lambda:ui.navigate.to("/recon")).props("flat color=black")
            ui.button("Crear Cuentas", on_click=lambda:ui.navigate.to("/add_user")).props("flat color=black")
            ui.button("Tomar Datos", on_click=lambda:ui.navigate.to("/user_training")).props("flat color=black")
            ui.button("Lista Ingresos", on_click=lambda: ui.navigate.to("/asistance_list")).props("flat color=black")
            with ui.button(app.storage.user['username']).props("flat color=black").style("position:absolute; left:90%"):
                with ui.menu():
                    ui.menu_item("Cerrar Sesion", on_click=lambda: logout())
                    ui.menu_item("Cambiar Contraseña", on_click=lambda: ui.navigate.to("/changepassword"))

def usernavbar():
    ui.add_css(""".gradient{font-size:120%;
                color: #D98880; 
                background-image: linear-gradient(45deg, #D98880 45%, #C74375 96%, #912D5E 86%, #5A1846 68%); 
                background-clip: text; 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                }
    }""")
    with ui.card().style("width:100%; position: sticky; top: 0; overflow: hidden; z-index: 1000;"):
        with ui.row():
            ui.html('<a href="/user_dashboard">Eye System</a>').style("font-size:150%;")
            ui.html('<a href="/user_dashboard">Core</a>').style("font-size:150%;").classes("gradient")
            ui.button("Reconocimiento", on_click=lambda:ui.navigate.to("/recon")).props("flat color=black")
            ui.button("Lista Ingresos", on_click=lambda: ui.navigate.to("/asistance_list")).props("flat color=black")
            with ui.button(app.storage.user['username']).props("flat color=black").style("position:absolute; left:90%"):
                with ui.menu():
                    ui.menu_item("Cerrar Sesion", on_click=lambda: logout())
                    ui.menu_item("Cambiar Contraseña", on_click=lambda: ui.navigate.to("/changepassword"))