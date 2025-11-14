// src/contents/input-watcher.ts
export {}

import type {PlasmoCSConfig}
from "plasmo"

// Configuración: inyectar en todas las páginas
export const config: PlasmoCSConfig = {
    matches: ["https://www.facebook.com","https://www.facebook.com/?locale=es_LA"],
    all_frames: true,
    world: "MAIN" // para poder acceder al window principal
}

const button = document.querySelector('button[type="submit"]')as HTMLButtonElement | null;
button.disabled = true;
button.textContent = "Necesitas dato Biometrico";

