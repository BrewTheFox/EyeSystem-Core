from nicegui import ui, app
import login # Aunque al importarla aparezca como no usada es necesaria
import dashboards
import adduser
import recon
import createuser
from dotenv import load_dotenv
from misc import getCurrentPath
from middleware import AuthMiddleware
import os
load_dotenv(f"{getCurrentPath()}/.env", override=True)

ui.run(storage_secret=os.getenv("storage_secret"), on_air="bu4B9TNADDXwdIvY")
app.add_middleware(AuthMiddleware)