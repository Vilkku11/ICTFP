import { useEffect, useState } from "react";

function Socket(props) {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    let newSocket = "";

    newSocket = new WebSocket("ws://localhost:8765");

    newSocket.onopen = () => {
      console.log("Websocket OPEN");
      props.setWebSocket(true);
    };

    newSocket.onmessage = (event) => {
      const parsedMsg = JSON.parse(event.data);

      // Check message type.
      props.setPlanes(...[parsedMsg.planes]);

      if (parsedMsg.adsb) {
        props.setReceiver(parsedMsg.adsb.connection);
      }

      if (parsedMsg.virtual_points) {
        props.setVirtualPoints(...[parsedMsg.virtual_points]);
      }
    };

    newSocket.onerror = (error) => {
      console.log("error:");
      console.log(error);
    };

    newSocket.onclose = (event) => {
      console.log("Websocket closed");
      console.log(event);
      props.setWebSocket(false);
      props.setReceiver(false);
    };

    setSocket(newSocket);

    return () => {
      console.log("component unmounted, closing WebSocket");

      if (newSocket) {
        newSocket.close();
      }
    };
  }, []);

  return null;
}

export default Socket;
