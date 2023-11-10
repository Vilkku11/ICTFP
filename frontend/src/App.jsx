import { useState } from "react";
//import DeckGL from "@deck.gl/react";
//import {StaticMap} from "react-map-gl";
//import { useControl } from "react-map-gl";
import { IconLayer } from "@deck.gl/layers";
import { MapboxOverlay } from "@deck.gl/mapbox/typed";
//import { BASEMAP } from "@deck.gl/carto";
//import * as Module from "./mapbox-gl-rtl-text.js";

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


let testData = [
  { name: "test", coordinates: [23.7609, 61.48], angle: 100 },
  { name: "receiver", coordinates: [23.76, 61.46], angle: 10 },
];

function App() {
  const [viewState, setViewState] = useState({
    longitude: 23.7601,
    latitude: 61.498,
    zoom: 11,
    dragRotate: false,
    touchRotate: false,
    keyboard: false,
  });

  const [test, setTest] = useState( [
  { name: "test", coordinates: [23.7609, 61.48], angle: 100 },
  { name: "receiver", coordinates: [23.76, 61.46], angle: 10 },
]);

  const ICON_MAPPING = {
    marker: { x: 0, y: 0, width: 32, height: 32, mask: true },
  };

  const iconLayer = new IconLayer({
    id: "icon-layer",
    data: test,
    pickable: true,
    // iconAtlas and iconMapping are required
    // getIcon: return a string
    iconAtlas: "plane.svg",
    iconMapping: ICON_MAPPING,
    getIcon: (d) => "marker",

    sizeScale: 15,
    getPosition: (d) => d.coordinates,
    getSize: (d) => 5,
    getColor: (d) => [Math.sqrt(d.exits), 140, 0],
  });
  const testButton = () => {
    testData.push({name: "receiverlol", coordinates: [23.76, 62.46], angle: 20})
   let data = test;
   data.push({name: "receiverlol", coordinates: [23.76, 61.50], angle: 20})
   setTest(data);
   console.log(test);
  }
  
  return (
    <>
    <button onClick={testButton}>test</button>
      <Map
        initialViewState={viewState}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: "50%",
          width: "50%",
        }}
        //mapStyle={BASEMAP.POSITRON} working as a replacement
        mapStyle="style.json"
      >
        <NavigationControl position="top-right" />
        <FullscreenControl position="top-right" />
        <ScaleControl position="bottom-right" />
        <AttributionControl customAttribution="© OpenMapTiles © OpenStreetMap contributors"
         position="bottom-left" />
        <DeckGLOverlay
          layers={[iconLayer]}
          getTooltip={({ object }) => object && `${object.name}`}
       />
      </Map>
    </>
  );
}

export default App;
// http://0.0.0.0:3000/finland/{z}/{x}/{y}
