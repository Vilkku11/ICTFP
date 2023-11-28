import "./ObjectHandler.css";

import { roundToDecimal, calculateHeading } from "../utils/dataFormat";

const ObjectHandler = ({ obj, type }) => {
  let content = "";
  console.log(obj);
  console.log(type);

  // Determine object type
  if (type == "plane") {
    content = (
      <div className="list-container">
        <ul className="list-items">
          <li>
            <strong>ID:</strong>
          </li>
          <li>
            <strong>Flight:</strong>
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
          <li>
            <strong>V/S:</strong>
          </li>
          <li>
            <strong>Heading:</strong>
          </li>
        </ul>
        <ul className="list-items">
          <li>{obj.id}</li>
          <li>{obj.flight}</li>
          <li>{roundToDecimal(obj.coordinates[0], 3)}</li>
          <li>{roundToDecimal(obj.coordinates[1], 3)}</li>
          <li>{obj.altitude}</li>
          <li>{obj.velocity[2]}</li>
          <li>{calculateHeading(obj.velocity)}</li>
        </ul>
      </div>
    );
  } else if (type == "virtualPoint") {
    console.log("virtualpoint");
    content = (
      <div className="list-container">
        <ul className="list-items-virtualpoint">
          <li>
            <strong>ID:</strong>
          </li>
          <li>
            <strong>Lat:</strong>
          </li>
          <li>
            <strong>Lon:</strong>
          </li>
        </ul>
        <ul className="list-items">
          <li>{obj.id}</li>
          <li>{obj.position[0]}</li>
          <li>{obj.position[1]}</li>
        </ul>
      </div>
    );
  }

  return content;
};

export default ObjectHandler;
