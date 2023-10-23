import { useState } from "react";
import DeckGL from "@deck.gl/react";
//import {StaticMap} from "react-map-gl";
import { MVTLayer } from "@deck.gl/geo-layers";
import { BASEMAP } from "@deck.gl/carto";

import {
  Map,
  ScaleControl,
  FullscreenControl,
  NavigationControl,
} from "react-map-gl/maplibre";

import "maplibre-gl/dist/maplibre-gl.css";

function App() {
  const layer = new MVTLayer({
    data: `http://0.0.0.0:5000/finland/{z}/{x}/{y}`,
    minZoom: 0,
    maxZoom: 14,
    getLineColor: [192, 192, 192],
    getFillColor: [140, 170, 180],
    pickable: true,

    getLineWidth: (f) => {
      switch (f.properties.class) {
        case "street":
          return 6;
        case "motorway":
          return 10;
        default:
          return 1;
      }
    },
    lineWidthMinPixels: 1,
  });

  const [viewState, setViewState] = useState({
    longitude: 23.45,
    latitude: 61.4981,
    zoom: 11,
  });

  return (
    <>
      <Map
        initialViewState={viewState}
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: 0,
          width: "100%",
        }}
        //mapStyle={BASEMAP.POSITRON} working as a replacement
        mapStyle="style.json"
      >
        <NavigationControl position="top-right" />
        <FullscreenControl position="top-right" />
        <ScaleControl position="bottom-right" />
      </Map>
    </>
  );
}

export default App;
// http://0.0.0.0:3000/finland/{z}/{x}/{y}
