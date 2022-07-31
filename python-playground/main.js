function initDv(websocket) {
  websocket.addEventListener("open", () => {
    let event = { type: "client" };
    websocket.send(JSON.stringify(event));
  });
}

function receiveMessage(websocket) {
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    console.log(event);
    switch (event.type) {
      case "init":
        let token = event.key;
        const request = new Request('http://localhost:5000' + '?token=' + token);
        fetch(request)
          .then((response) => {
            console.log(response);
            if (response.status === 200) {
              const para = document.createElement("p");
              const node = document.createTextNode("开始......");
              para.appendChild(node);
              const element = document.getElementById("message");
              element.appendChild(para);
            } else {
              throw new Error('Something went wrong on API server!');
            }
          })
        break;
      case "progress":
        const para = document.createElement("p");
        const node = document.createTextNode(event.message);
        para.appendChild(node);
        const element = document.getElementById("message");
        element.appendChild(para);
        break;
      default:
        throw new Error(`Unsupported event type: ${event.type}.`);
    }
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const websocket = new WebSocket("ws://localhost:8001/");
  initDv(websocket);
  receiveMessage(websocket);
});