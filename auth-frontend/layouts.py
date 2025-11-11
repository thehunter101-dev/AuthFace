from fasthtml.common import *
from dataclasses import dataclass

class Layout:
    def __init__(self,titulo,css,scripts,body):
        self.titulo = titulo
        self.css = css
        self.body=body
        self.scripts=scripts

    def render(self):
        return Html(
            Head(
                Title(self.titulo),
                Link(
                    rel="stylesheet",
                    href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css",
                ),
                Link(
                    rel="stylesheet",
                    href="/styles/index.css"
                ),
                *[(Link(rel="stylesheet",href=content)) for content in self.css],
                *[(Script(src=content)) for content in self.scripts],
            ),
            Body(Div(Img(src="public/logo.png"), cls="navbar"),self.body),
        )


class Dashboard(Layout):
    def render(self):
         return Html(
            Head(
                Title(self.titulo),
                Link(
                    rel="stylesheet",
                    href="https://unpkg.com/@picocss/pico@latest/css/pico.min.css",
                ),
                Link(
                    rel="stylesheet",
                    href="/styles/index.css"
                ),
                Link(
                    rel="stylesheet",
                    href="/styles/dashboard.css"
                ),
                *[(Link(rel="stylesheet",href=content)) for content in self.css],
                htmxsrc,
                Script(src="https://cdnjs.cloudflare.com/ajax/libs/webcamjs/1.0.26/webcam.min.js"),
                Script(src='https://cdn.jsdelivr.net/npm/js-cookie@3.0.5/dist/js.cookie.min.js'),
                Script('let rostros = []')
            ),
            Body(
                Div(
                    Div(
                        Section(
                            Div(Img(src="public/avatar.jpg", cls="img_avatar"),cls='avatar_img'),
                            Div(
                                H2("",id="h2username"),
                                P(""),
                                cls="avatar_name"
                            ),
                            Script(
                                '''
                                function getCookie(name) {
                                    const value = `; ${document.cookie}`;
                                    const parts = value.split(`; ${name}=`);
                                    if (parts.length === 2) return parts.pop().split(';').shift();
                                }


                                fetch("http://localhost:8000/auth/user/info",{
                                    method:"GET",
                                    headers:{
                                        "Authorization": "Bearer " + getCookie("access_token")
                                    }
                                }).then(response => response.json())
                                .then(data => {
                                    let h2name = document.getElementById("h2username")
                                    h2name.textContent = data.username
                                })
                                '''
                            ),
                            cls='avatar_user'
                        ),
                        Section(
                            Ul(
                                Li(A(Div(H4("Inicio"),cls="item_select")),hx_get="/dashboard/home",hx_target="#body_contenido",hx_swap="outerHTML"),
                                Li(A(Div(H4("Biometria"),cls="item_select")),hx_get="/dashboard/biometria",hx_target="#body_contenido",hx_swap="outerHTML"),
                                Li(A(Div(H4("Sitios"),cls="item_select"))),
                                Li(A(Div(H4("Cuenta"),cls="item_select"))),
                            ),cls="menu"
                        ),
                        cls="left_bar"
                    ),
                    Div(
                        Div(Img(src="public/logo.png"), cls="navbar"),
                        Div(self.body),
                        cls="contenedor"
                    ),
                    cls="main"
                ),
            )
        )