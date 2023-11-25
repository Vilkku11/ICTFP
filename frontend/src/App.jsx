import React, { useState } from "react";
import { IconLayer, TextLayer } from "@deck.gl/layers";
import { MapboxOverlay } from "@deck.gl/mapbox/typed";
import {
  Map,
  ScaleControl,
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
  const [planeInfo, setPlaneInfo] = useState({});
  const testData = {
    planes: [
      {
        id: "461E1C",
        flight: "FIN4MW__",
        velocity: [423, 1.8956222586147526, 640, "GS"],
        coordinates: [67.61805725097656, 31.711287064985793],
        altitude: 36775,
      },
      {
        id: "4601FD",
        flight: "FIN9VM__",
        velocity: [259, 331.65430637692333, 0, "GS"],
        coordinates: [61.24530029296875, 23.863481794084823],
        altitude: 20025,
      },
      {
        id: "AC062A",
        flight: null,
        velocity: 0.0,
        coordinates: [0.0, 0.0],
        altitude: -1,
      },
    ],
    virtual_points: [],
  };
  const [testPlanes, setTestPlanes] = useState(testData.planes);
  const [testPoints, setTestPoints] = useState([
    { name: "first", coordinates: [23.7609, 23.7609] },
  ]);

  const [planes, setPlanes] = useState([]);
  const [virtualPoints, setVirtualPoints] = useState([]);

  const planeLayer = new IconLayer({
    id: "plane-layer",
    data: planes,
    pickable: true,
    //onHover: (info, event) => console.log("Hovered:", info.object),
    //onClick: (info, event) => console.log("Clicked:", info.object.name),
    onClick: (d) => {
      setIsOpen(!isOpen);
      console.log(isOpen);
    },
    iconAtlas: "airplane.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => [d.coordinates[1], d.coordinates[0]],
    getAngle: (d) => d.velocity[2],
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
    getPosition: (d) => [d.coordinates[1], d.coordinates[0]],
    getPixelOffset: textOffset,
    getText: (d) => d.id,
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
    getPosition: (d) => [d.coordinates[1], d.coordinates[0]],
    getSize: (d) => iconSize,
    getColor: (d) => [Math.sqrt(d.exits), 0, 140],
    updateTriggers: {
      getSize: iconSize,
    },
  });

  const testLayer = new IconLayer({
    id: "testlayer",
    data: testPlanes,
    pickable: true,
    //onHover: (info, event) => console.log("Hovered:", info.object),
    //onClick: (info, event) => console.log("Clicked:", info.object.name),
    onClick: (info) => {
      setPlaneInfo(info.object);
    },
    iconAtlas: "airplane.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => [d.coordinates[1], d.coordinates[0]],
    //getAngle: (d) => d.angle,
    getSize: (d) => iconSize,
    getColor: (d) => [Math.sqrt(d.exits), 140, 0],
    updateTriggers: {
      getSize: iconSize,
    },
  });

  // Handles icon, textlayer size on different zoom levels
  const handleIconSize = (zoom) => {
    if (zoom >= 9) {
      setIconSize(48);
      setTextSize(14);
      setTextOffset([0, -28]);
    } else if (zoom >= 8 && zoom < 9) {
      setIconSize(45);
      setTextSize(14);
      setTextOffset([0, -27]);
    } else if (zoom >= 7 && zoom < 8) {
      setIconSize(40);
      setTextSize(12);
      setTextOffset([0, -23]);
    } else if (zoom >= 6 && zoom < 7) {
      setIconSize(30);
      setTextSize(10);
      setTextOffset([0, -16]);
    } else if (zoom >= 5 && zoom < 6) {
      setIconSize(25);
      setTextSize(0);
    } else if (zoom < 5) {
      setIconSize(20);
      setTextSize(0);
    }
  };

  return (
    <>
      <Socket
        setWebSocket={setWebSocket}
        setPlanes={setPlanes}
        planes={planes}
        setVirtualPoints={setVirtualPoints}
        virtualPoints={virtualPoints}
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
        <NavigationControl position="top-right" showCompass={false} />
        <ScaleControl position="bottom-right" />
        <AttributionControl
          customAttribution="© OpenMapTiles © OpenStreetMap contributors"
          position="bottom-left"
        />
        <DeckGLOverlay
          layers={[planeLayer, planeIdLayer, virtualPointLayer, testLayer]}
          //getTooltip={({ object }) => object && `${object.name}` + `${object}`}
        />
      </Map>
      <StatusMemoized webSocket={webSocket} />
      <InfoCardMemoized
        planeInfo={planeInfo}
        setPlaneInfo={setPlaneInfo}
        testData={testData}
      />
    </>
  );
}
/*
      <Status webSocket={webSocket} />
      <InfoCard planeInfo={planeInfo} />
      */

const StatusMemoized = React.memo(Status);
const InfoCardMemoized = React.memo(InfoCard);

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
