from fasthtml.common import *

cuentaComponent, rt = fast_app()


@rt("/delete")
def getDelete():
    modal = Dialog(
        Article(
            Header(
                P(
                    "Atencion, esta apunto de borrar su cuenta!!!",
                    style="font-weight:bold;",
                )
            ),
            P(
                "Esta seguro de seguir con esta opcion, al eliminar su cuenta perdera los siguientes datos."
            ),
            Ul(
                Li("Acceso al sitio."),
                Li("Los datos biometricos se borraran de la base de datos"),
                Li("Los sitios agregados seran eliminados."),
            ),
            P("Desea continuar"),
            Footer(
                Button(
                    "Si estoy seguro",
                    style="background-color:red;border:0;",
                    id="buttonDelete",
                ),
                Button("Cancelar", cls="secondary", id="buttonCancel"),
            ),
        ),
        open=True,
        id="model_insert"
    )
    return modal


@rt("/")
def get(req):
    username = req.cookies.get("username")
    email = req.cookies.get("user_email")
    body = Main(
        Div(
            H3("Informacion del Usuario"),
            Hr(),
            Div(
                Div(Img(src="public/user.png"), cls="content_avatar_img"),
                Div(
                    H4(
                        "Nombre de Usuario: ",
                        Span(
                            f"{username}",
                            style="font-weight:normal; margin:0; color:inherit;",
                            id="username",
                        ),
                        cls="body_text",
                    ),
                    H4(
                        "Correo Electronico: ",
                        Span(
                            f"{email}",
                            style="font-weight:normal; margin:0; color:inherit;",
                            id="useremail",
                        ),
                        cls="body_text",
                    ),
                    Button(
                        "Eliminar cuenta",
                        style="background-color:red;border:0;",
                        hx_get="/dashboard/cuenta/delete",
                        hx_target="#model_insert",
                        hx_swap="outerHTML",
                        id="button_delete"
                    ),
                ),
                cls="user_content_info",
            ),
            H3("Extras", style="margin-top:1em;"),
            Hr(),
            Div(
                #Div(Button("Iniciar con dato biometrico"), cls="button_content"),
                Div(
                    Div(H5("Copia de seguridad", cls="body_text"), cls="backup_head"),
                    Div(Button("Local",id="buttonLocal"), Button("Nube",id="buttonCloud"), cls="backup_buttons"),
                    Div(id="drive_status"),
                    cls="backup_content",
                ),
                cls="extra_content",
            ),
            Div(id="model_insert"),
            cls="container",
        ),
        Script(src="/scripts/home.js"),
        cls="contenido",
        id="body_contenido",
    )
    return body
