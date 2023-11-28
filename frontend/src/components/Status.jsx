import "./Status.css";
const Status = ({ webSocket, receiver }) => {
  return (
    <div className="status-text">
      <p>Websocket: {webSocket ? "CONNECTED" : "DISCONNECTED"}</p>
      <p>Receiver: {receiver ? "CONNECTED" : "NO CONNECTION"}</p>
    </div>
  );
};

export default Status;
