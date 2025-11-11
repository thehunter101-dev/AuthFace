function apagarCamara() {
    // Detener todos los tracks de video
    const stream = Webcam.stream;
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    // Opcional: limpiar el contenedor
    Webcam.reset();
}

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
    let spanname = document.getElementById("username")
    let spanemail = document.getElementById("useremail")
    console.log(data)
    spanname.textContent = data.username
    spanemail.textContent = data.email
})