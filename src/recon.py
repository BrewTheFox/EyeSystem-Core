from nicegui import ui, app
import navbars
from fastapi import File, UploadFile
from misc import FaceCropper

@ui.page("/recon", title="Reconocimiento Facial")
def recognition():
    role = app.storage.user.get('role')
    if role == 1:
        navbars.adminnavbar()
    if role == 2:
        navbars.usernavbar()
    ui.label("Implementacion en progreso...")
    ui.html('<video id="video" autoplay></video>')
    ui.html('<canvas id="canvas" style="display:none;"></canvas>')
    ui.run_javascript("""
        const video = document.getElementById('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                video.srcObject = stream;
                setInterval(capturarYEnviar, 1000 / 10); // Captura 10 FPS
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

'''@app.post("/recon_sendimg")
async def idk(file: UploadFile = File(...)):
    await FaceCropper(await file.read())
    return {"message": "Frame recibido", "filename": file.filename}'''