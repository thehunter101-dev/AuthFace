from fasthtml.common import *
biometriaComponent, rt = fast_app()

@rt("/")
def get():
    body = Div(
        H1("Agrega tu rostro", cls="body_text"),
        Div(
            Div(
                style="width:320px;height:240px;position:absolute; top:0;left:0; z-index:1;",
                id="camara"
            ),
            Canvas(
                id="overlay", 
                style="width:320px;height:240px; position:absolute; top:0;left:0; z-index:2;",
            ),
            style="width:320px; height:240px;position:relative;",
            cls = "content-camara"
        ),
        Div(
            Button("Tomar Captura", onclick="take_snapshot()",style="",disabled=True,id="snapB"),
            Button("Escanear rostro", onclick="send_snapshots()"),
            style="display:flex;gap:1em;"
        ),
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/webcamjs/1.0.26/webcam.min.js"),
        Script(src="https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js"),
        Script(src="/scripts/camera.js?==v2"),
        cls="contenido",
        id="body_contenido",
        style="display:flex;flex-direction:column;justify-content:center;align-items:center;gap:2em;"
        )
    return body