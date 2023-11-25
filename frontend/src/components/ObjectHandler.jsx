const ObjectHandler = (obj) => {
  let content = "";
  console.log(obj);

  // Determine object type
  if ("flight" in obj.obj) {
    console.log("why not running");
    content = (
      <div>
        <ul>
          <li>id: {obj.obj.id}</li>
          <li>lon: {obj.obj.coordinates[0]}</li>
          <li>lat: {obj.obj.coordinates[1]}</li>
          <li>altitude: {obj.obj.altitude}</li>
        </ul>
      </div>
    );
  } else {
    console.log("maybe virtualpoint?");
  }
  return content;
};

export default ObjectHandler;
