const notyf = new Notyf();
document.addEventListener("DOMContentLoaded",()=>{
    const H2Name = document.getElementById("h2username")
    fetch("http://localhost:8000/auth/user/info", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + Cookies.get("access_token")
        }
    }).then(response => response.json()).then(data => {
        Cookies.set("username",data.username)
        Cookies.set("user_email",data.email)
        Cookies.set("user_id",data.id)
    })
    H2Name.textContent = Cookies.get("username")
})