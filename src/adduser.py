from nicegui import ui
from navbars import adminnavbar
from dbmanager import registeruser
@ui.page("/add_user", title="Crear Cuentas")
async def add_user():
    adminnavbar()
    def handleregister(account_type:int, account_name:str, account_password:str):
        if not username.validate() or not password.validate() or not passwordcheck.validate():
            ui.notify("Verifica que todos los datos introducidos sean correctos", color="red")
            return
        data = registeruser(account_name, account_password, account_type)
        ui.notify(data["status"], color=data["color"])

    with ui.row().style("width:100%; margin-top: 5%;  text-align: center; display: flex; justify-content: center;"):
        with ui.card().style(" width:50%;"):
            ui.label("Crear cuenta nueva.").style("width:100%; font-size: 150%")
            username = ui.input("Usuario:", validation={'El usuario es muy corto': lambda value: len(value) >= 4}).style("width:100%")
            password = ui.input("Contraseña:", password=True, validation={'Contraseña muy corta': lambda value: len(value) >= 8 }).style("width:100%")
            passwordcheck = ui.input("Repetir Contraseña:", validation={'Las contraseñas no coinciden': lambda value: password.value == value }, password=True).style("width:100%")
            ui.button("Crear cuenta normal", on_click=lambda: handleregister(2, username.value, password.value)).style("width:100%")
            ui.button("Crear cuenta administrativa", on_click=lambda: handleregister(1, username.value, password.value)).style("width:100%")