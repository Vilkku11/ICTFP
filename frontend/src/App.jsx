import React, { useState, useEffect } from "react";
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

import { calculateHeading } from "./utils/dataFormat";

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

  // Websocket and receiver status
  const [webSocket, setWebSocket] = useState(false);
  const [receiver, setReceiver] = useState(false);

  // Plane and virtualpoint data arrays
  const [planes, setPlanes] = useState([]);
  const [virtualPoints, setVirtualPoints] = useState([]);
  const [receiverPoint, setReceiverPoint] = useState([]);

  // Infocard
  const [iconInfo, setIconInfo] = useState({});

  const planeLayer = new IconLayer({
    id: "plane-layer",
    data: planes,
    pickable: true,
    onClick: (info) => {
      setIconInfo(info.object);
    },
    iconAtlas: "airplane.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => [d.coordinates[1], d.coordinates[0]],
    getAngle: (d) => d.heading,
    getSize: (d) => iconSize,
    getColor: (d) => [255, 255, 0],
    updateTriggers: {
      getSize: iconSize,
    },
  });

  const planeIdLayer = new TextLayer({
    id: "plane-id-layer",
    data: planes,
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

  const receiverLayer = new IconLayer({
    id: "receiver-point",
    data: receiverPoint,
    pickable: true,
    onClick: (info) => {
      setIconInfo(info.object);
    },
    iconAtlas: "receiver.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => [d.coordinates[1], d.coordinates[0]],
    getSize: (d) => iconSize,
    getColor: (d) => [0, 0, 0],
    updateTriggers: {
      getSize: iconSize,
    },
  });

  const virtualPointLayer = new IconLayer({
    id: "virtual-point-layer",
    data: virtualPoints,
    pickable: true,
    onClick: (info) => {
      setIconInfo(info.object);
    },
    iconAtlas: "virtualPoint.svg",
    iconMapping: {
      marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
    },
    getIcon: (d) => "marker",
    getPosition: (d) => [d.position[1], d.position[0]],
    getSize: (d) => iconSize,
    getColor: (d) => [0, 0, 0],
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
        setReceiver={setReceiver}
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
          layers={[
            planeLayer,
            planeIdLayer,
            virtualPointLayer,
            //testLayer,
            receiverLayer,
          ]}
        />
      </Map>
      <StatusMemoized webSocket={webSocket} receiver={receiver} />
      <InfoCardMemoized
        iconInfo={iconInfo}
        setIconInfo={setIconInfo}
        //testPlanes={testPlanes}
        planes={planes}
        virtualPoints={virtualPoints}
        //testPoints={testPoints}
      />
    </>
  );
}

const StatusMemoized = React.memo(Status);
const InfoCardMemoized = React.memo(InfoCard);

export default App;
