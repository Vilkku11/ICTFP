import "./Status.css";
const Status = (props) => {
  return (
    <div className="status-text">
      <p>Websocket {props.webSocket ? "CONNECTED" : "DISCONNECTED"}</p>
    </div>
  );
};

export default Status;
