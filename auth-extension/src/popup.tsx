import React, { useEffect, useState, useRef } from "react";
import '@picocss/pico';
import './styles/poup.css';



function useNativeWebcam(width = 320, height = 240) {
  const streamRef = useRef<MediaStream | null>(null);
  const [ready, setReady] = useState(false);


  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width, height } });
        streamRef.current = stream;
        setReady(true);
      } catch (err) {
        console.error("No se pudo acceder a la cámara:", err);
      }
    }

    startCamera();

    return () => {
      // Detener la cámara al desmontar
      streamRef.current?.getTracks().forEach(track => track.stop());
    };
  }, [width, height]);

  const takePhoto = (): string | null => {
    if (!streamRef.current) return null;

    const video = document.createElement("video");
    video.srcObject = streamRef.current;
    video.play();

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext("2d");

    // Esperamos a que el video tenga datos
    return new Promise<string | null>((resolve) => {
      video.addEventListener("loadeddata", () => {
        ctx?.drawImage(video, 0, 0, width, height);
        resolve(canvas.toDataURL("image/jpeg"));
        video.pause();
      });
    }) as unknown as string; // Forzamos el tipo por simplicidad
  };

  return { takePhoto, ready };
}

async function getToken() {
  try {
    const res = await fetch("http://localhost:5001/auth/token", {
      credentials: "include"
    });
    const data = await res.json();
    return data.token;
  } catch (err) {
    console.error("No se pudo obtener el token", err);
    return null;
  }
}

export default function Popup() {
  const [token, setToken] = useState<string | null>(null);
  const { takePhoto, ready } = useNativeWebcam(320, 240);

async function habilitarBotonSubmit() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab.id) return;

  await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const btn = document.querySelector('button[type="submit"]') as HTMLButtonElement | null;
      if (btn) {
        btn.disabled = false;
        btn.textContent = "Iniciar sesión";
      }
    }
  });
}

  useEffect(() => {
    getToken().then(t => setToken(t));
  }, []);

  const handleVerify = async () => {
    if (!token || !ready) return;

    const photo = await takePhoto();
    if (!photo) return;

    try {
      const res = await fetch("http://127.0.0.1:8000/auth/verify-bio/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ image: photo })
      });

      if (res.ok){
        habilitarBotonSubmit();
      }
      else{
        alert("No autorizado")
      };
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="container">
      {token ? (
        <article>
          <header><b>!!!Estas listo!!!</b></header>
          Ahora abre el sitio que te quieres logear y dale click al botón de validar!!!
          <footer>
            <button onClick={handleVerify} disabled={!ready}>Verificar</button>
          </footer>
        </article>
      ) : (
        <article>
          <header><b>Importante!!!</b></header>
          Debes logearte primero en nuestro sitio!!!
        </article>
      )}
    </main>
  );
}
