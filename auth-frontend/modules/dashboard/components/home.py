from fasthtml.common import *

homeComponent, rt = fast_app()
@rt("/")
def get():
    body = Main(
        Div(
            H3("Informacion del Usuario"),
            Hr(),
            Div(
                Div(
                    Img(src="public/avatar.jpg"),
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

