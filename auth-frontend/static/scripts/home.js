// ---------------------- ELIMINAR CUENTA ----------------------
document.body.addEventListener("htmx:afterOnLoad", (e) => {
    if (e.target.id === "button_delete") {
        const buttonDelete = document.getElementById("buttonDelete");
        const buttonCancel = document.getElementById("buttonCancel");

        if (buttonCancel) {
            buttonCancel.addEventListener("click", () => {
                const model = document.getElementById("model_insert");
                if (model) 
                    model.remove();
                

                const newModel = document.createElement("div");
                newModel.id = "model_insert";
                document.body.appendChild(newModel);
            });
        }

        if (buttonDelete) {
            buttonDelete.addEventListener("click", () => {
                fetch(`${
                    Cookies.get('backendURI')
                }/auth/users/${
                    Cookies.get("user_id")
                }/`, {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + Cookies.get("access_token")
                    }
                }).then(response => {
                    if (response.ok) {
                        window.location.href = "/login";
                        notyf.success("Cuenta eliminada");
                    } else {
                        notyf.error("Se generó un error al eliminar la cuenta");
                    }
                });
            });
        }
    }

    // ---------------------- BOTÓN NUBE / DRIVE ----------------------
    const button_local = document.getElementById("buttonLocal")
    const button_send = document.getElementById("buttonCloud");
    if (button_send) {
        button_send.addEventListener("click", uploadJson);
    }
    button_local.addEventListener("click", async () => {
        try { 
            const response = await fetch(`${
                Cookies.get('backendURI')
            }/auth/biometria/`, {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + Cookies.get("access_token"),
                    "Content-Type": "application/json"
                }
            });

            if (! response.ok) {
                notyf.error("Error obteniendo la copia de seguridad");
                return;
            }

            const data = await response.json();

            const blob = new Blob([JSON.stringify(data, null, 2)], {type: "application/json"});

            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "backup_biometria.json"; 
            document.body.appendChild(a);
            a.click();

            
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            notyf.success("Copia de seguridad descargada correctamente");

        } catch (err) {
            console.error(err);
            notyf.error("Error descargando la copia de seguridad");
        }
    });
});

// ---------------------- FUNCIONES GOOGLE DRIVE ----------------------
async function ensureToken() {
    if (!window.accessToken) {
        await new Promise((resolve) => {
            tokenClient.callback = (resp) => {
                if (resp.error) {
                    notyf.error("Error al obtener token de Google");
                    console.error(resp.error);
                    return;
                }
                window.accessToken = resp.access_token;
                resolve();
            };
            tokenClient.requestAccessToken({prompt: 'consent'});
        });
    }
    return window.accessToken;
}

async function uploadJson() {
    const token = await ensureToken();
    if (! token) 
        return;
    

    try {
        const backupResponse = await fetch(`${
            Cookies.get('backendURI')
        }/auth/biometria/`, {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + Cookies.get("access_token"),
                "Content-Type": "application/json"
            }
        });

        if (! backupResponse.ok) {
            notyf.error("Error obteniendo los embeddings desde el servidor");
            return;
        }

        const backupData = await backupResponse.json();

        const metadata = {
            name: "backup_biometria.json",
            mimeType: "application/json"
        };

        const fileContent = JSON.stringify(backupData);
        const blob = new Blob([fileContent], {type: "application/json"});

        const form = new FormData();
        form.append("metadata", new Blob([JSON.stringify(metadata)], {type: "application/json"}));
        form.append("file", blob);

        // 3️⃣ Subir a Google Drive
        const driveResponse = await fetch("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id", {
            method: "POST",
            headers: new Headers(
                {
                    Authorization: "Bearer " + token
                }
            ),
            body: form
        });

        const result = await driveResponse.json();

        if (result.id) {
            notyf.success("Copia de seguridad subida a Drive correctamente");
        } else {
            notyf.error("No se pudo subir la copia a Drive");
            console.error(result);
        }

    } catch (err) {
        console.error(err);
        notyf.error("Error subiendo la copia a Google Drive");
    }

}
