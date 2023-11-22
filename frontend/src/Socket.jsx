import { useEffect } from "react";

function Socket({ setWebSocket, setPlanes, setVirtualPoints }) {
  //const [socket, setSocket] = useState(null);

  //const URL = "ws://0.0.0.0:8765"; new WebSocket("ws://0.0.0.0:8765")

  useEffect(() => {
    let newSocket = new WebSocket("ws://0.0.0.0:8765");

    newSocket.onopen = () => {
      console.log("Websocket OPEN");
      setWebSocket(true);
    };

    newSocket.onmessage = (event) => {
      console.log("websocket message:");
      console.log(event.data);
      const data = JSON.parse(event.data);
      setPlanes(...[data.planes]);
      setVirtualPoints(...[data.virtualPoints]);
    };

    newSocket.onerror = (error) => {
      console.log("error:");
      console.log(error);
    };

    newSocket.onclose = (event) => {
      console.log("Websocket closed");
      console.log(event);
      setWebSocket(false);
    };

    //setSocket(newSocket);

    setTimeout(() => {
      newSocket = new WebSocket("ws://0.0.0.0:8765");
    }, 5000);

    return () => {
      console.log("component unmounted, closing WebSocket");
      newSocket.close();
    };
  }, []);

  return null;
}

export default Socket;
