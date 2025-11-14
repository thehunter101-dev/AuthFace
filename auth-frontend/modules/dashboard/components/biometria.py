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
            cls = "content-camara",
        ),
        Div(
            Button("Tomar Captura", onclick="take_snapshot()",style="",disabled=True,id="snapB"),
            style="display:flex;gap:1em;",
            id="buttonContent"
        ),
        Script(src="/scripts/biometria.js"),
        cls="contenido",
        id="body_contenido",
        style="display:flex;flex-direction:column;justify-content:center;align-items:center;gap:2em;"
        )
    return body