from nicegui import ui, app
import navbars
from fastapi import File, UploadFile
from misc import RecognizeFromImg
import threading

@ui.page("/recon", title="Reconocimiento Facial")
def recognition():
    role = app.storage.user.get('role')
    if role == 1:
        navbars.adminnavbar()
    else:
        navbars.usernavbar()
    ui.html('''<canvas id="canvas" style="display:none;"></canvas>''')
    ui.add_css('''nosense {width:100%;}
               video {
                display: block;
                margin: 0 auto;
                }''')
    ui.run_javascript("""
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                setInterval(capturarYEnviar, 1000 / 15); // Captura 15 FPS
            })
            .catch(error => {
                console.error("Error al acceder a la webcam:", error);
            });
        
        function capturarYEnviar() {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

            canvas.toBlob(blob => {
                const formData = new FormData();
                formData.append("file", blob, "frame.jpg");

                fetch("/recon_sendimg", {
                    method: "POST",
                    body: formData
                }).catch(err => console.error("Error enviando frame:", err));
            }, "image/jpeg");
        }""")
    with ui.card().style("width:100%;"):
        with ui.row().style("text-align:center; justify-content: center; align-items: center; width:100%"):
            ui.label("Reconocimiento Facial.").style("font-size:30px;")
            ui.label("Se estan enviando datos!").style("font-size:30px; color:green;")
        ui.html('<video id="video" autoplay></video>', tag="nosense")


@app.post("/recon_sendimg")
async def recognizefromweb(file: UploadFile = File(...)):
    file = await file.read()
    if file:
        hilo = threading.Thread(target=RecognizeFromImg, args=(file,))
        hilo.start()
        return {"created":"Recognition Task Created"}
    else:
        return {"error":"No file provided"}