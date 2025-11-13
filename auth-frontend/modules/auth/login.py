from fasthtml.common import *
from layouts import Layout
import httpx

loginModule, rt = fast_app()


@rt("/", name="getLogin")
def get():
    body = Div(
        Card(
            Div(H1("Login"), cls="card_title"),
            Div(
                Form(
                    Label(
                        "Usuario",
                        Input(name="username", required="true", id="input_username"),
                    ),
                    Label(
                        "Password",
                        Input(
                            name="password",
                            type="password",
                            required="true",
                            id="input_password",
                        ),
                    ),
                    Button("Iniciar sesion", type="submit"),
                    method="post",
                    action=uri("/login"),
                    id="form_login",
                ),
                Div(A("Registrate", href="/register/"), cls="card_link"),
                cls="card_body",
            ),
            cls="card",
        ),
        cls="container-fluid",
    )

    return Layout("Login", ["/styles/login.css"], ["/scripts/login.js"], body).render()


@rt("/", name="postLogin")
async def post(req):
    data = await req.form()
    username = data["username"]
    password = data["password"]

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "http://127.0.0.1:8000/auth/token/",
            json={"username": username, "password": password},
        )
        if res.status_code == 200:
            tokens = res.json()
            response = RedirectResponse("/dashboard", status_code=303)
            response.set_cookie("access_token", tokens["access"])
            return response
        return JSONResponse({"error": "Usuario no registrado"}, status_code=401)
