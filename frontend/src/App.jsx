import { useState, useEffect } from "react";
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

  // Icon and textbox size
  const [iconSize, setIconSize] = useState(50);
  const [textSize, setTextSize] = useState(15);
  // TextBox offset in pixel coordinates
  const [textOffset, setTextOffset] = useState([0, -30]);

  const [webSocket, setWebSocket] = useState(false);
  // Infocard
  const [isOpen, setIsOpen] = useState(false);

  const [testPlanes, setTestPlanes] = useState([
    { name: "test", coordinates: [23.7609, 61.48], angle: 100 },
    { name: "receiver", coordinates: [23.76, 61.46], angle: 10 },
  ]);

  const [testPoints, setTestPoints] = useState([
    { name: "first", coordinates: [23.7609, 61.48] },
  ]);

  const [planes, setPlanes] = useState([]);
  const [virtualPoints, setVirtualPoints] = useState([]);

  const planeLayer = new IconLayer({
    id: "plane-layer",
    data: testPlanes,
    pickable: true,
    //onHover: (info, event) => console.log("Hovered:", info.object),
    //onClick: (info, event) => console.log("Clicked:", info.object.name),
    onClick: () => setIsOpen(!isOpen),
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

  const planeIdLayer = new TextLayer({
    id: "plane-id-layer",
    data: testPlanes,
    pickable: true,
    background: true,
    getPosition: (d) => [d.coordinates[0], d.coordinates[1]],
    getPixelOffset: textOffset,
    getText: (d) => d.name,
    getSize: (d) => textSize,
    updateTriggers: {
      getSize: textSize,
      getTextOffset: textOffset,
    },
  });

  const virtualPointLayer = new IconLayer({
    id: "virtual-point-layer",
    data: testPoints,
    pickable: true,
    iconAtlas: "airplane.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => d.coordinates,
    getSize: (d) => iconSize,
    getColor: (d) => [Math.sqrt(d.exits), 0, 140],
    updateTriggers: {
      getSize: iconSize,
    },
  });

  // Handles icon, textlayer size on different zoom levels
  const handleIconSize = (zoom) => {
    if (zoom >= 10) {
      setIconSize(50);
      setTextSize(15);
      setTextOffset([0, -30]);
    } else if (zoom >= 9 && zoom < 10) {
      setIconSize(40);
      setTextSize(10);
      setTextOffset([0, -23]);
    } else if (zoom >= 8 && zoom < 9) {
      setIconSize(30);
      setTextSize(8);
      setTextOffset([0, -15]);
    } else if (zoom >= 7 && zoom < 8) {
      setIconSize(20);
      setTextSize(1);
    } else if (zoom < 7) {
      setIconSize(10);
      setTextSize(0);
    }
  };

  return (
    <>
      <Socket
        setWebSocket={setWebSocket}
        setPlanes={setPlanes}
        setVirtualPoints={setVirtualPoints}
      />
      <Map
        initialViewState={viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        onZoom={() => {
          handleIconSize(viewState.zoom);
        }}
        mapStyle="style.json"
        RTLTextPlugin={null}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: 0,
          width: "100%",
        }}
      >
        <NavigationControl position="top-right" />
        <FullscreenControl position="top-right" />
        <ScaleControl position="bottom-right" />
        <AttributionControl
          customAttribution="© OpenMapTiles © OpenStreetMap contributors"
          position="bottom-left"
        />
        <DeckGLOverlay
          layers={[planeLayer, planeIdLayer, virtualPointLayer]}
          //getTooltip={({ object }) => object && `${object.name}` + `${object}`}
        />
      </Map>
      <Status webSocket={webSocket} />
      <InfoCard isOpen={isOpen} setIsOpen={setIsOpen} />
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
