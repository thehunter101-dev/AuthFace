const notyf = new Notyf();
document.addEventListener("DOMContentLoaded", () => {
    const form_register = document.getElementById("form_register");
    const username_input = document.getElementById("input_username");
    const password_input = document.getElementById("password");
    const vPassword_input = document.getElementById("vPassword");
    form_register.addEventListener('submit', async (event) => {
        event.preventDefault();

        const form_data = new FormData(form_register);
        const data = Object.fromEntries(form_data.entries());
        try {
            const res = await fetch('/register', {
                method: 'POST',
                body: form_data
            });
            const json = await res.json()
            console.log(json)
            if (res.ok) {
                notyf.success(json.succes || "Usuario registrado como ya sabes")
                const form_data = new FormData()
                form_data.append("username",username_input.value)
                form_data.append("password",password_input.value)
                fetch("/login",{
                    method:"POST",
                    body:form_data
                }).then(response=>{
                    if (response.ok ){
                        notyf.success("Iniciando session")
                        window.location.href = "/dashboard/"
                    }else{
                        notyf.error("Hubo un problema en el inicio!!!")
                    }
                })
            } else {
                if (json.detail && json.detail.password_verify) {
                    notyf.error(json.detail.password_verify)
                } else if (json.detail && json.detail.userNameExist){
                    notyf.error(json.detail.userNameExist)
                    username_input.setAttribute("aria-invalid","true")
                }else{
                    notyf.error(json.error || "Error desconocido")
                }
            }
        } catch (error) {
            console.error(error)
        }
    })

    username_input.addEventListener('input',()=>{
        if (username_input.getAttribute("aria-invalid") == "true"){
            username_input.removeAttribute("aria-invalid")
        }
    })

    vPassword_input.addEventListener("input",()=>{
        if(password_input.value === vPassword_input.value){
            password_input.setAttribute("aria-invalid","false")
            vPassword_input.setAttribute("aria-invalid","false")
        }else{
            password_input.removeAttribute("aria-invalid")
            vPassword_input.setAttribute("aria-invalid","true")
        }
    })
})
