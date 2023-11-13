import { useState } from "react";
//import DeckGL from "@deck.gl/react";
//import {StaticMap} from "react-map-gl";
//import { useControl } from "react-map-gl";
import { IconLayer } from "@deck.gl/layers";
import { MapboxOverlay } from "@deck.gl/mapbox/typed";
//import { BASEMAP } from "@deck.gl/carto";
//import * as Module from "./mapbox-gl-rtl-text.js";

import Socket from "./Socket";

import {
  Map,
  ScaleControl,
  FullscreenControl,
  NavigationControl,
  useControl,
  AttributionControl,
} from "react-map-gl/maplibre";

import "maplibre-gl/dist/maplibre-gl.css";

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

  const [test, setTest] = useState([
    { name: "test", coordinates: [23.7609, 61.48], angle: 100 },
    { name: "receiver", coordinates: [23.76, 61.46], angle: 10 },
  ]);

  const handleIconSize = (zoom) => {
    const baseSize = 50;
    const saturationZoom = 9;

    const zoomMultiplier = 0.09;
    const sizeMultiplier = zoom <= saturationZoom ? zoom * zoomMultiplier : 1;
    const iconSize = baseSize * sizeMultiplier;
    setIconSize(iconSize);
  };

  const ICON_MAPPING = {
    marker: { x: 0, y: 0, width: 800, height: 800, mask: true },
  };
  const [iconSize, setIconSize] = useState(50);

  const iconLayer = new IconLayer({
    id: "icon-layer",
    data: test,
    pickable: true,
    onHover: (info, event) => console.log("Hovered:", info.object),
    onClick: (info, event) => console.log("Clicked:", event),
    // iconAtlas and iconMapping are required
    // getIcon: return a string
    iconAtlas: "airplane.svg",
    iconMapping: ICON_MAPPING,
    getIcon: (d) => "marker",
    getPosition: (d) => d.coordinates,
    getAngle: (d) => d.angle,
    getSize: (d) => iconSize,
    getColor: (d) => [Math.sqrt(d.exits), 140, 0],
    updateTriggers: {
      getSize: iconSize,
    },
  });
  const testButton = () => {
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
    setTest(...[data]);
    key = data.length;
    console.log(test);
  };

  return (
    <>
      <Socket onReceiveMessage={"test"} />
      <button onClick={testButton}>test</button>
      <Map
        initialViewState={viewState}
        onMove={(evt) => setViewState(evt.viewState)}
        onZoom={() => handleIconSize(viewState.zoom)}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: "50%",
          width: "50%",
        }}
        //mapStyle={BASEMAP.POSITRON} working as a replacement
        mapStyle="style.json"
        setRTLTextPlugin={"s"}
      >
        <NavigationControl position="top-right" />
        <FullscreenControl position="top-right" />
        <ScaleControl position="bottom-right" />
        <AttributionControl
          customAttribution="© OpenMapTiles © OpenStreetMap contributors"
          position="bottom-left"
        />
        <DeckGLOverlay
          layers={[iconLayer]}
          getTooltip={({ object }) => object && `${object.name}` + `${object}`}
        />
      </Map>
    </>
  );
}

export default App;
// http://0.0.0.0:3000/finland/{z}/{x}/{y}
