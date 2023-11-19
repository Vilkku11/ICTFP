import { useState } from "react";
import { IconLayer, TextLayer } from "@deck.gl/layers";
import { MapboxOverlay } from "@deck.gl/mapbox/typed";
import {
  Map,
  ScaleControl,
  FullscreenControl,
  NavigationControl,
  useControl,
  AttributionControl,
} from "react-map-gl/maplibre";

import Socket from "./Socket";
import Status from "./components/Status";
import InfoCard from "./components/InfoCard";

import "maplibre-gl/dist/maplibre-gl.css";

// Rendering all Layers on top of the map
function DeckGLOverlay(props) {
  const overlay = useControl(() => new MapboxOverlay(props));
  overlay.setProps(props);
  return null;
}

function App() {
  const [viewState, setViewState] = useState({
    longitude: 23.7601,
    latitude: 61.498,
    zoom: 11,
    dragRotate: false,
    touchRotate: false,
    keyboard: false,
  });

  const [iconSize, setIconSize] = useState(50);
  const [textSize, setTextSize] = useState(15);

  //Temporary
  const [webSocket, setWebSocket] = useState(false);

  const [testPlanes, setTestPlanes] = useState([
    { name: "test", coordinates: [23.7609, 61.48], angle: 100 },
    { name: "receiver", coordinates: [23.76, 61.46], angle: 10 },
  ]);

  const [waypoints, setWaypoints] = useState([
    { name: "first", coordinates: [23.7609, 61.48] },
  ]);

  const iconLayer = new IconLayer({
    id: "icon-layer",
    data: testPlanes,
    pickable: true,
    onHover: (info, event) => console.log("Hovered:", info.object),
    onClick: (info, event) => console.log("Clicked:", event),
    iconAtlas: "airplane.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => d.coordinates,
    getAngle: (d) => d.angle,
    getSize: (d) => iconSize,
    getColor: (d) => [Math.sqrt(d.exits), 140, 0],
    updateTriggers: {
      getSize: iconSize,
    },
  });

  const textLayer = new TextLayer({
    id: "text-layer",
    data: testPlanes,
    pickable: true,
    background: true,
    getPosition: (d) => [d.coordinates[0], d.coordinates[1] + 0.005],
    getText: (d) => d.name,
    getSize: (d) => textSize,
    updateTriggers: {
      getSize: textSize,
    },
  });

  const handleIconSize = (zoom) => {
    const baseSize = 50;
    const saturationZoom = 9;
    const zoomMultiplier = 0.09;
    const sizeMultiplier = zoom <= saturationZoom ? zoom * zoomMultiplier : 1;
    const iconSize = baseSize * sizeMultiplier;
    setIconSize(iconSize);
  };
  const handleTextSize = (zoom) => {
    const baseSize = 15;
    const saturationZoom = 9;
    const zoomMultiplier = 0.09;
    const sizeMultiplier = zoom <= saturationZoom ? zoom * zoomMultiplier : 1;
    const textSize = baseSize * sizeMultiplier;
    setTextSize(textSize);
  };

  return (
    <>
      <Socket setWebSocket={setWebSocket} />
      <Map
        initialViewState={viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        onZoom={() => {
          handleIconSize(viewState.zoom);
          handleTextSize(viewState.zoom);
        }}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: 0,
          width: "100%",
        }}
        mapStyle="style.json"
      >
        <NavigationControl position="top-right" />
        <FullscreenControl position="top-right" />
        <ScaleControl position="bottom-right" />
        <AttributionControl
          customAttribution="© OpenMapTiles © OpenStreetMap contributors"
          position="bottom-left"
        />
        <DeckGLOverlay
          layers={[iconLayer, textLayer]}
          getTooltip={({ object }) => object && `${object.name}` + `${object}`}
        />
      </Map>
      <Status webSocket={webSocket} />
      <InfoCard />
    </>
  );
}
/*
<
        
*/

export default App;
// http://0.0.0.0:3000/finland/{z}/{x}/{y}

/*const testButton = () => {
    let data = test;
    //data.push({ name: "receiverlol", coordinates: [23.76, 61.5], angle: 20 });
    //data[0].coordinates[0] = data[0].coordinates[0] + 0.01;
    //data[1].angle = data[1].angle + 1;
    if (data.length >= 1) {
      data.pop();
    } else if (data.length == 0) {
      data.push({ name: "receiverlol", coordinates: [23.76, 61.5], angle: 20 });
    }
    console.log(viewState.zoom);

    // shallow check
    setTest(...[data]);
    key = data.length;
    console.log(test);
  };*/
