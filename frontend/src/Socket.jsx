import { useEffect, useState } from "react";

const Socket = ({ onReceiveMessage }) => {
  const [socket, setSocket] = useState(null);
  const [message, setMessage] = useState("");

  //const URL = "ws://0.0.0.0:8765";

  const connectWebSocket = () => {
    console.log("Running connectWebSocket");
    console.log("socket:");
    console.log(socket);
    const newSocket = new WebSocket("ws://0.0.0.0:8765");

    newSocket.onopen = () => {
      console.log("Websocket connected and IS OPEN");
    };

    newSocket.onerror = (error) => {
      console.log(error);
    };

    newSocket.onmessage = (event) => {
      // Initial message handle if needed
      const message = event.data;
      onReceiveMessage(message);
    };

    newSocket.onclose = () => {
      console.log("Websocket closed");
    };

    setSocket(newSocket);
  };

  useEffect(() => {
    connectWebSocket();
    console.log("In socket useEffect");
    return () => {
      console.log("Socket now unmounting");
      if (socket) {
        socket.close();
      }
    };
  }, []);

  return null;
};

export default Socket;
