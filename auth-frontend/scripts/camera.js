rostros = []
const snapB = document.getElementById("snapB")
let snapeable = false

Webcam.attach('#camara');
function take_snapshot() {
    Webcam.snap(function (data_uri) {
        rostros.push(data_uri)
    });
}

function send_snapshots() {
    if (rostros.length >= 4) {
        fetch("http://localhost:8000/auth/img/post", {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: JSON.stringify(
                {rostros: rostros}
            )
        }).then(res => res.json()).then(data => console.log(data)).catch(err => console.error(err))

    } else {
        alert("Agrege mas de 3 rsotros!!!")
    }
}

Promise.all([faceapi.nets.tinyFaceDetector.loadFromUri('/static/models')]).then(startDetection);


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
            if (faceWidth > 100 && faceWidth < 300){
                color = "lime";
                if(!snapeable){
                    snapB.disabled = false
                    snapeable = true
                }
            }

            if(snapeable && color == "red"){
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
