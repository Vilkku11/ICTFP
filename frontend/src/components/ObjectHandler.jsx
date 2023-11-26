import "./ObjectHandler.css";
const ObjectHandler = (obj) => {
  let content = "";
  console.log(obj);

  const roundToDecimal = (number, decimals) => {
    return Number(number.toFixed(decimals));
  };

  // Determine object type
  if ("flight" in obj.obj) {
    console.log("why not running");
    content = (
      <div className="list-container">
        <ul className="list-items">
          <li>
            <strong>ID:</strong>
          </li>
          <li>
            <strong>Latitude:</strong>
          </li>
          <li>
            <strong>Longitude:</strong>
          </li>
          <li>
            <strong>Altitude:</strong>
          </li>
        </ul>
        <ul className="list-items">
          <li>{obj.obj.id}</li>
          <li>{roundToDecimal(obj.obj.coordinates[0], 5)}</li>
          <li>{roundToDecimal(obj.obj.coordinates[1], 5)}</li>
          <li>{obj.obj.altitude}</li>
        </ul>
      </div>
    );
  } else {
    console.log("maybe virtualpoint?");
  }
  return content;
};

export default ObjectHandler;
