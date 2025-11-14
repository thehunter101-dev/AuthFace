export {}

import type { PlasmoCSConfig } from "plasmo"

export const config: PlasmoCSConfig = {
  matches: ["https://aprender.altissia.org/*"],
  world: "MAIN"
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.evaluate(
    '//*[@id="theme-provider"]/div/main/div/form/button',
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue as HTMLButtonElement | null

  if (button) {
    button.disabled = true
    button.textContent = "Necesitas dato biométrico"
  }

  // Avisar al bridge
  window.postMessage({
    source: "altissia-page",
    type: "ready"
  })
})
