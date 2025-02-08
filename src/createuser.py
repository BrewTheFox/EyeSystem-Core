from nicegui import ui, app
from fastapi import File, UploadFile, responses, Form
from misc import FaceCropper
from navbars import adminnavbar
from typing import Annotated


@ui.page("/user_training", title="Entrenamiento y recoleccion de datos")
async def training_page():
    def startSampling(code:str):
        ui.notify("Toma de fotos comenzada. Porfavor activar camara en caso de ser solicitado", color="green")
        ui.run_javascript(f'iniciarCaptura("{code}")')

    adminnavbar()
    with ui.row().style("width:100%; margin-top: 5%;  text-align: center; display: flex; justify-content: center;"):
        with ui.card().style("width:50%;"):
            ui.label("Tomar datos").style("width:100%; font-size: 150%")
            code = ui.input("Codigo del estudiante").style("width:100%")
            ui.input("Apellidos del estudiante").style("width:100%")
            ui.input("Nombres del estudiante").style("width:100%")
            ui.input("Grupo del estudiante").style("width:100%")
            ui.select(["Seleccionar Jornada","Mañana", "Tarde"], label="Jornada", value="Seleccionar Jornada").style("width:100%")
            ui.button("Guardar Datos").style("width:100%")
            ui.button("Iniciar Captura", on_click=lambda:startSampling(code.value)).style("width:100%")
            ui.html('<h6 id="cantidad">Se han recolectado 0 imagenes de las 200 necesarias</h6>').style("font-size:120%; color:red")
            ui.add_body_html("""<script>async function iniciarCaptura(codigo) {
            try {
            const textocantidad = document.getElementById("cantidad")
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            const track = stream.getVideoTracks()[0];
            const settings = track.getSettings();

            const canvas = new OffscreenCanvas(settings.width, settings.height);
            const ctx = canvas.getContext("2d");

            const video = document.createElement("video");
            video.srcObject = stream;
            video.play();

            async function capturarYEnviar() {
                if (video.readyState === video.HAVE_ENOUGH_DATA) {
                    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                    const blob = await canvas.convertToBlob({ type: "image/jpeg" });
                    const formData = new FormData();
                    formData.append("file", blob, "frame.jpg");
                    formData.append("code", codigo);

                    fetch("/training_sendimg", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                           textocantidad.innerText = "Se han recolectado " + data.imagenes_obtenidas.toString() + " imagenes de las 200 necesarias"
                           if (data.imagenes_obtenidas >= 200) {
                                textocantidad.innerText = "Se han recolectado las 200 imagenes satisfactoriamente"
                                textocantidad.style.color = "green"
                                console.log("Se han alcanzado 200 imágenes, deteniendo la captura.");
                                track.stop()
                                video.srcObject = null;
                                return;
                            }
                    })
                    .catch(err => console.error("Error enviando frame o procesando respuesta:", err));
                }

                setTimeout(capturarYEnviar, 100); // Captura a 10 FPS
            }

            capturarYEnviar();
        } catch (error) {
            console.error("Error al acceder a la webcam:", error);
        }
    }</script>""")


@app.post("/training_sendimg")
async def idk(code:Annotated[str, Form()], file: UploadFile = File(...)):
    return responses.JSONResponse(await FaceCropper(await file.read(), code))