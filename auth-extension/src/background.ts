let ws: WebSocket | null = null

function conectarWS() {
  ws = new WebSocket("ws://localhost:1815")

  ws.onopen = () => console.log("WS conectado")

  ws.onmessage = (evt) => {
    // Reenviar el mensaje al bridge
    chrome.tabs.query({}, (tabs) => {
      for (const t of tabs) {
        if (t.id) {
          chrome.tabs.sendMessage(t.id, {
            type: "ws-message",
            data: evt.data
          })
        }
      }
    })
  }

  ws.onclose = () => setTimeout(conectarWS, 2000)
}

conectarWS()

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "from-page") {
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(msg.data))
    }
  }
})
