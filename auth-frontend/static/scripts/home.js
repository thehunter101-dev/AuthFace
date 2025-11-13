document.body.addEventListener("htmx:afterOnLoad", (e) => {
    if (e.target.id === "button_delete") {
        const buttonDelete = document.getElementById("buttonDelete");
        const buttonCancel = document.getElementById("buttonCancel");

        buttonCancel.addEventListener("click", () => {
            const model = document.getElementById("model_insert");
            model.remove();
            const newModel = document.createElement("div")
            newModel.id = "model_insert"
            document.body.appendChild(newModel)
        });

        buttonDelete.addEventListener("click", () => {
            fetch(`${Cookies.get('backendURI')}/auth/users/${Cookies.get("user_id")}/`, {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + Cookies.get("access_token")
                }
            }).then(response =>{
                if (response.ok){
                    window.location.href="/login"
                    notya.succes("Cuenta eliminada")
                }else{
                    notyf.error("Se genero un error al eliminar la cuenta")
                }
            })
        });
    }
});


function apagarCamara() { // Detener todos los tracks de video
    const stream = Webcam.stream;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    // Opcional: limpiar el contenedor
    Webcam.reset();
}
