const notyf = new Notyf();

document.addEventListener("DOMContentLoaded", () => {
    const form_login = document.getElementById("form_login")
    form_login.addEventListener("submit", (e) => {
        e.preventDefault();
        const form_data = new FormData(form_login)
        fetch("/login", {
            method: "POST",
            body: form_data
        }).then(response => {
            if (response.ok) {
                notyf.success("Inicio de session correcta")
                window.location.href = "/dashboard/"
            } else if (response.status == 401) {
                notyf.error("El usuario no existe")
            } else {
                notyf.error("Error desconocido, comunicarse con el administrador")
            }
        })
    })
})
