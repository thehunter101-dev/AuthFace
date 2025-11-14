const notyf = new Notyf();
const SCOPES = 'https://www.googleapis.com/auth/drive.file';
const CLIENT_ID = '891723098233-8bk902nrm8luut4ur55p78ffc8ots5no.apps.googleusercontent.com';


let snapB
let snapeable
let access_token
let rostros = []

document.addEventListener("DOMContentLoaded", () => {
    const H2Name = document.getElementById("h2username")
    fetch("http://localhost:8000/auth/user/info", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + Cookies.get("access_token")
        }
    }).then(response => response.json()).then(data => {
        Cookies.set("username", data.username)
        Cookies.set("user_email", data.email)
        Cookies.set("user_id", data.id)
    })
    H2Name.textContent = Cookies.get("username")
    Promise.all([faceapi.nets.tinyFaceDetector.loadFromUri('/models')]);
    let detectionInterval = null;
    async function startDetection() {
        const video = document.querySelector('#camara video');
        const canvas = document.getElementById('overlay');
        const displaySize = {
            width: 320,
            height: 240
        };
        faceapi.matchDimensions(canvas, displaySize);

        const ctx = canvas.getContext('2d');

        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions());
            const resized = faceapi.resizeResults(detections, displaySize);
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (resized.length > 0) {
                const box = resized[0].box;
                const faceWidth = box.width;

                // Cambia color según distancia
                let color = "red";
                if (faceWidth > 100 && faceWidth < 300) {
                    color = "lime";
                    if (! snapeable) {
                        snapB.disabled = false
                        snapeable = true
                    }
                }

                if (snapeable && color == "red") {
                    snapB.disabled = true
                    snapeable = false
                }
                ctx.strokeStyle = color;
                ctx.lineWidth = 3;
                ctx.strokeRect(box.x, box.y, box.width, box.height);

                // Mostrar valor de distancia aproximada
                ctx.fillStyle = color;

            }
        }, 200);
    }

    function stopDetection() {
        if (detectionInterval) {
            clearInterval(detectionInterval);
            detectionInterval = null;
        }
    }
    document.body.addEventListener("htmx:afterOnLoad", (e) => {
        if (e.target.id != "LiBiometria") {
            rostros = []
            Webcam.reset();
            stopDetection()
        } else {
            snapB = document.getElementById("snapB")
            snapeable = false
            access_token = Cookies.get("access_token")

            Webcam.attach('#camara');
            startDetection()

        }
    })


  
})

function take_snapshot() {
    Webcam.snap(function (data_uri) {
        rostros.push(data_uri)
    });
}


function send_snapshots(biometriaExist,biometriaId,button_add) {
    if (rostros.length >= 4) {
        if (! biometriaExist) {
            fetch("http://localhost:8000/auth/img/post", {
                method: "POST",
                headers: {
                    'Authorization': 'Bearer ' + access_token,
                    "Content-type": "application/json"
                },
                body: JSON.stringify(
                    {rostros: rostros}
                )
            }).then(res => res.json()).then(data => {
                rostros = []
                button_add.textContent = "Actualizar dato biometrico"
                notyf.success("Dato biometrico agregado!!!")

            }).catch(err => notyf.error("Hubo problemas en el servidor!!!"))

        } else {
            fetch(`http://localhost:8000/auth/biometria/${biometriaId}/`, {
                method: "PATCH",
                headers: {
                    'Authorization': 'Bearer ' + access_token,
                    "Content-type": "application/json"
                },
                body: JSON.stringify(
                    {rostros: rostros}
                )
            }).then(res => res.json()).then(data => {
                rostros = []
                notyf.success("Dato biometrico actualizado!!!")

            }).catch(err => notyf.error("Hubo problemas en el servidor!!!"))
        }
    } else {
        notyf.error("Agrege mas de 3 rostros!!!")
    }
}

function gapiLoaded() {
    gapi.load('client', initializeGapiClient);
  }

  async function initializeGapiClient() {
    await gapi.client.init({
      discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"],
    });
    window.gapiInited = true;
    maybeEnableButtons();
  }

  function gisLoaded() {
    window.tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: CLIENT_ID,
      scope: "https://www.googleapis.com/auth/drive.file",
      callback: () => {},
    });
    window.gisInited = true;
    maybeEnableButtons();
  }

  function maybeEnableButtons() {
    if (window.gapiInited && window.gisInited) {
      document.getElementById("authorize_button").style.visibility = "visible";
    }
  }
