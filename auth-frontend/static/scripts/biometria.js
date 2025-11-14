let button_add = document.createElement("button")
let button_content = document.getElementById("buttonContent")
let biometriaExist
let biometriaId

fetch(`${Cookies.get('backendURI')}/auth/verify-bio/`, {
    method: "GET",
    headers: {
        "Authorization": "Bearer " + Cookies.get("access_token")
    }
}).then(res => res.json()).then(data => {
    biometriaExist = data["add"]
    if (biometriaExist){
        button_add.textContent = "Actualizar dato biometrico"
        biometriaId = data["bioId"]
    }else{
        button_add.textContent = "Agregar dato biometrico"
    }
    button_content.appendChild(button_add)    
})

button_add.addEventListener("click",()=>{
    send_snapshots(biometriaExist,biometriaId,button_add)
})
