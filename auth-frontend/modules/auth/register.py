from fasthtml.common import *
from layouts import Layout
import httpx

registerModule,rt = fast_app()

@rt("/",name="getRegister")
def get():
    body = Main(
            Div(
                Div(H1("Crear Cuenta"), cls="card_title"),
                Div(
                    Form(
                        Label("Correo Electronico"),
                        Input(name='email'),
                        Label("Usuario"),
                        Input(name='username'),
                        Label("Password"),
                        Input(type="password",name="password"),
                        Label("Verific Password"),
                        Input(type="password",name='verific_password'),
                        Button("Register", type="submit"),
                        id="form_register"
                    ),
                    cls="card_body",
                ),
                cls="card",
                style="",
            ),
            cls="container-fluid",
        )

    return Layout("Crear",['/styles/login.css'],[''],body).render()

@rt("/",name="postRegister")
async def post(req):
    data = await req.form()
    email = data["email"]
    username = data["username"]
    password = data["password"]
    verific_password = data["verific_password"]
    jsonData = {"username":username,"email":email,"password":password}
    if (password != verific_password):
        return JSONResponse({"error":"Error de validacion","detail":{"password_verify":"Las contrasenias no coiciden."}},status_code=400)
    async with httpx.AsyncClient() as client:
        res = await client.post('http://localhost:8000/auth/users/',json=jsonData)
        if res.status_code == 400:
            json_data = res.json()
            print(json_data)
            if "username" in json_data:
                return JSONResponse({"error":'Error de registro!!!','detail':{'userNameExist':json_data['username'][0]}},status_code=400)
            else:
                return JSONResponse({"error":'Error de registro!!!','detail':{'Unkown':'error desconocidom, comuniquese con el admin'}},status_code=400)
        return JSONResponse({"succes":"El usuario se registro correctamente"}) 

