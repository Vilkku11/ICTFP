import { useEffect, useState } from "react";

function Socket(props) {
  const [socket, setSocket] = useState(null);

  //const URL = "ws://0.0.0.0:8765"; new WebSocket("ws://0.0.0.0:8765")

  useEffect(() => {
    let newSocket = new WebSocket("ws://127.0.1.1:8765");

    newSocket.onopen = () => {
      console.log("Websocket OPEN");
      props.setWebSocket(true);
    };
    // adsb message
    // {"adsb": {"connection": true, "last_msg_ts": "2023-11-24 13:29:33.362208"}}
    newSocket.onmessage = (event) => {
      console.log("websocket message:");
      const parsedMsg = JSON.parse(event.data);
      console.log(event.data);
      console.log(parsedMsg);
      console.log(parsedMsg.planes);
      // Check message type.
      props.setPlanes(...[parsedMsg.planes]);
      props.setVirtualPoints(...[parsedMsg.virtual_points]);
      
      
    };

    newSocket.onerror = (error) => {
      console.log("error:");
      console.log(error);
    };

    newSocket.onclose = (event) => {
      console.log("Websocket closed");
      console.log(event);
      props.setWebSocket(false);
    };

    setSocket(newSocket);

    setTimeout(() => {
      newSocket = new WebSocket("ws://127.0.1.1:8765");
    }, 5000);

    return () => {
      console.log("component unmounted, closing WebSocket");
      newSocket.close();
    };
  }, []);

  return null;
}

export default Socket;
