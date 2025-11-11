from fasthtml.common import *
from layouts import Layout
import httpx

loginModule, rt = fast_app()

@rt("/",name="getLogin")
def get():
    body = Div(
            Card(
                Div(H1("Login"), cls="card_title"),
                Div(
                    Form(
                        Label("Usuario",Input(name='username',required="true")),
                        Label("Password",Input(name='password',type="password",required="true")),
                        Button("Iniciar sesion", type="submit"),
                        method="post",
                        action=uri("/login")
                    ),
                    Div(A("Registrate", src="#"), cls="card_link"),
                    cls="card_body",
                ),
                cls="card",
            ),
            cls="container-fluid",
        )

    return Layout("Login",['/styles/login.css'],[''],body).render()


@rt("/",name = "postLogin")
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
            response = RedirectResponse('/dashboard',status_code=303)
            response.set_cookie('access_token',tokens['access'])
            return response
        return Main(H1('No estas cumeado!!!'),NotStr('<div class="tenor-gif-embed" data-postid="18173140706170597575" data-share-method="host" data-aspect-ratio="1" data-width="100%"><a href="https://tenor.com/view/bocchi-the-rock-gif-18173140706170597575">Bocchi The Rock Sticker</a>from <a href="https://tenor.com/search/bocchi+the+rock-stickers">Bocchi The Rock Stickers</a></div> <script type="text/javascript" async src="https://tenor.com/embed.js"></script>'),cls='container',style='width:30em')
