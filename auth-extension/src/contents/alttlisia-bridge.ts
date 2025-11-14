export {}

window.addEventListener("message", (ev) => {
  if (ev.data?.source !== "altissia-page") return

  chrome.runtime.sendMessage({
    type: "ws-send",
    data: ev.data
  })
})

chrome.runtime.onMessage.addListener((msg) => {
  window.postMessage({
    source: "altissia-extension",
    ...msg
  })
})
