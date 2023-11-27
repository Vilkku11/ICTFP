import { useEffect, useState } from "react";

function Socket(props) {
  const [socket, setSocket] = useState(null);
  const [url, setUrl] = useState("");

  const fetchWebSocketIp = async () => {
    const response = await fetch("http://localhost:5000/getip");
    const data = await response.json();
    console.log(data);
    const url = "ws://" + data.ip + ":8765";
    console.log(url);
    setUrl(url);
  };

  useEffect(() => {
    if (!url) {
      fetchWebSocketIp();
    }
  }, [url]);

  useEffect(() => {
    let newSocket = "";
    if (url) {
      newSocket = new WebSocket("ws://localhost:8765");

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

      /* setTimeout(() => {
      newSocket = new WebSocket("ws://192.168.1.145:8765");
    }, 5000);*/
    }
    return () => {
      console.log("component unmounted, closing WebSocket");

      if (newSocket) {
        newSocket.close();
      }
    };
  }, [url]);

  return null;
}

export default Socket;
