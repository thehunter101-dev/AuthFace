// content-script.ts
export {}

import type {PlasmoCSConfig}
from "plasmo"

// Configuración: inyectar en todas las páginas
export const config: PlasmoCSConfig = {
    matches: ["http://localhost:5001/*"],
    all_frames: true,
    world: "MAIN" // para poder acceder al window principal
}

