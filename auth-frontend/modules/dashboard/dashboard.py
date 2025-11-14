from fasthtml.common import *
from layouts import Dashboard
from .components import cuenta, biometria,home
from beforeware import auth_before
import os
beforeware = Beforeware(auth_before)

routes = (
    Mount('/home',home.homeComponent,name="home"),
    Mount('/cuenta',cuenta.cuentaComponent,name="cuenta"),
    Mount('/biometria',biometria.biometriaComponent,name="biometria")
)

dashboardModule, rt = fast_app(routes=routes,before=beforeware)
@rt("/")
def get():
    body= home.homeReturn()
    dashboard = Dashboard("Home",['/styles/dashboard/home.css'],['/scripts/dashboard.js'],body).render()
    return dashboard