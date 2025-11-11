# Codigo inicial para fastHtml
from fasthtml.common import *
from modules.auth import login, register
from modules.dashboard.dashboard import dashboardModule
from beforeware import auth_before
import httpx

beforeware = Beforeware(
    auth_before,
    skip=[
        "/login",
        #"/dashboard/biometria",
        #"/dashboard/home",
        "/auth/login",
        "/register",
        r"/public/.*",
        r"/models/.*",   # rutas públicas
        #"/", 
        r"/static/.*",
        r".*\.css",
        r".*\.js"
    ]
)

routes=(
    Mount("/login",login.loginModule, name="login"),
    Mount("/register",register.registerModule,name="register"),
    Mount("/dashboard",dashboardModule,name="dashboard")
)

app, rt = fast_app(hdrs=picocondlink, before=beforeware,live=True,routes=routes,static_path="static")
app.static_route_exts(prefix="/public",static_path='public')


@rt("/auth/token")
def get(req):
    token = req.cookies.get("access_token")
    return {"token":token}




serve()