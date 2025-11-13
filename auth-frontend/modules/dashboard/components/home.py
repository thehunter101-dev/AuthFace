from fasthtml.common import *

homeComponent,rt = fast_app()

@rt("/")
def get():
    body = Main(
        H1("Bienvenido al panel de control!!!", cls="body_text"),
        P("Selecciona una opcion del panel lateral, recuerda despues de 5 min la sesion pide verificacion!!!", cls="body_text"),
        id="body_contenido",
        cls="container contenido"
    )
    return body

def homeReturn():
    return get()