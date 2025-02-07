from nicegui import ui, app
import login # Aunque al importarla aparezca como no usada es necesaria
from dotenv import load_dotenv
from middleware import AuthMiddleware
import os
load_dotenv("../.env")

ui.run(storage_secret=os.getenv("storage_secret"))
app.add_middleware(AuthMiddleware)