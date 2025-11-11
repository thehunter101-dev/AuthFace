from fasthtml.common import *
from layouts import Dashboard
from .components import home, biometria
from beforeware import auth_before

beforeware = Beforeware(auth_before)

routes = (
    Mount('/home',home.homeComponent,name="home"),
    Mount('/biometria',biometria.biometriaComponent,name="biometria")
)

dashboardModule, rt = fast_app(routes=routes,before=beforeware)
@rt("/")
def get():
    body= Main(
        H1("Bienvenido al panel de control!!!", cls="body_text"),
        P("Selecciona una opcion del panel lateral, recuerda despues de 5 min la sesion pide verificacion!!!", cls="body_text"),
        id="body_contenido",
        cls="container contenido"
    )
    dashboard = Dashboard("Home",['/styles/dashboard/home.css'],[''],body).render()
    return dashboard