# Codigo inicial para fastHtml
from logging import disable
from fasthtml.common import *
from layouts import Dashboard, Layout
import httpx

async def auth_before(req,sess):
    token = req.cookies.get("access_token")
    if not token:
        return RedirectResponse('/login',status_code=303)
    
    async with httpx.AsyncClient() as client:
        res = await client.get('http://127.0.0.1:8000/auth/protected/',headers={"Authorization":f"Bearer {token}"})
    if res.status_code != 200:
        return RedirectResponse('/login',status_code=303)

    return


beforeware = Beforeware(
    auth_before,
    skip=[
        "/login",
        "/dashboard/biometria",
        #"/dashboard/home",
        "/auth/login",
        r"/public/.*",
        r"/models/.*",   # rutas públicas
        "/", 
        r"/static/.*",
        r".*\.css",
        r".*\.js"
    ]
)

app, rt = fast_app(hdrs=picocondlink, before=beforeware,live=True)
app.static_route_exts('/public','/public')
app.static_route_exts('/styles','/styles')
app.mount("/static", StaticFiles(directory="static"), name="static")

@rt("/auth/login")
async def post(req):
    data = await req.form()
    username = data['username']
    password = data['password']

    async with httpx.AsyncClient() as client:
        res = await client.post('http://127.0.0.1:8000/auth/token/', json={
            'username':username,
            'password':password
        })
        if res.status_code == 200:
            tokens = res.json()
            response = RedirectResponse('/dashboard')
            response.set_cookie('access_token',tokens['access'])
            return response
        return Main(H1('No estas cumeado!!!'),NotStr('<div class="tenor-gif-embed" data-postid="18173140706170597575" data-share-method="host" data-aspect-ratio="1" data-width="100%"><a href="https://tenor.com/view/bocchi-the-rock-gif-18173140706170597575">Bocchi The Rock Sticker</a>from <a href="https://tenor.com/search/bocchi+the+rock-stickers">Bocchi The Rock Stickers</a></div> <script type="text/javascript" async src="https://tenor.com/embed.js"></script>'),cls='container',style='width:30em')

@rt("/auth/token")
def get(req):
    token = req.cookies.get("access_token")
    return {"token":token}




class Templates:
    def __init__(self, body, title):
        self.body = body
        self.title = title

    def render(self):
        return Html(
            Head(
                Title(self.title),
                Link(
                    rel="stylesheet",
                    href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css",
                ),
                Link(rel="stylesheet", href="/styles/login.css"),
            ),
            Body(self.body),
        )


@rt("/login")
def login():
    body = Div(
        Div(Img(src="/public/logo.png"), cls="navbar"),
        Div(
            Div(cls="card_blur"),
            Card(
                Div(H1("Login"), cls="card_title"),
                Div(
                    Form(method="post",action="/auth/login")(
                        Label("Usuario",Input(name='username',required="true")),
                        Label("Password",Input(name='password',type="password",required="true")),
                        Button("Iniciar sesion", type="submit"),
                    ),
                    Div(A("Registrate", src="#"), cls="card_link"),
                    cls="card_body",
                ),
                cls="card",
                style="",
            ),
            cls="background",
        ),
        style="height:100vh",
    )

    return Templates(body, "Login").render()


@rt("/register")
def register():
    body = Div(
        Div(Img(src="public/logo.png"), cls="navbar"),
        Div(
            Div(cls="card_blur"),
            Div(
                Div(H1("Crear Cuenta"), cls="card_title"),
                Div(
                    Form(
                        Label("Correo Electronico"),
                        Input(),
                        Label("Usuario"),
                        Input(),
                        Label("Password"),
                        Input(type="password"),
                        Label("Verific Password"),
                        Input(type="password"),
                        Button("Register", type="submit"),
                    ),
                    cls="card_body",
                ),
                cls="card",
                style="",
            ),
            cls="background",
        ),
        style="height:100vh",
    )

    return Templates(body, "Crear").render()

@rt("/dashboard")
def dashboard():
    body= Main(
        H1("Bienvenido al panel de control!!!", cls="body_text"),
        P("Selecciona una opcion del panel lateral, recuerda despues de 5 min la sesion pide verificacion!!!", cls="body_text"),
        id="body_contenido",
        cls="container contenido"
    )
    dashboard = Dashboard("Home",['/styles/dashboard/home.css'],body).render()
    return dashboard

@rt("/dashboard/home")
def get():
    body = Main(
        Div(
            H3("Informacion del Usuario"),
            Hr(),
            Div(
                Div(
                    Img(src="/public/avatar.jpg"),
                    cls="content_avatar_img"
                ),
                Div(
                    H4("Nombre de Usuario: ",Span("", style="font-weight:normal; margin:0; color:inherit;",id="username"),cls="body_text"),
                    H4("Correo Electronico: ",Span("", style="font-weight:normal; margin:0; color:inherit;",id="useremail"),cls="body_text")
                ),
                cls="user_content_info"
            ),
            H3("Extras",style="margin-top:1em;"),
            Hr(),
            Div(
                Div(
                    Button("Iniciar con dato biometrico"),
                    cls="button_content"
                ),
                Div(
                    Div(H5("Copia de seguridad", cls="body_text"),cls="backup_head"),
                    Div(
                        Button("Local"),
                        Button("Nube"),
                        cls="backup_buttons"
                    ),
                    cls="backup_content"
                ),
                cls="extra_content"
            ),
            cls="container"
        ),
        Script(src="/scripts/home.js"),
        cls="contenido",id="body_contenido" 
    )
    return body

@rt("/dashboard/biometria")
def get():
    body = Div(
                Script(src="https://cdnjs.cloudflare.com/ajax/libs/webcamjs/1.0.26/webcam.min.js"),
                Script('let rostros = []'),
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
        Script(src="https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js"),
        Script(src="/scripts/camera.js"),
        cls="contenido",
        id="body_contenido",
        style="display:flex;flex-direction:column;justify-content:center;align-items:center;gap:2em;"
        )
    return body

serve()