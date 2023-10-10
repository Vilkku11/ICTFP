import { useState } from "react";
import DeckGL from "@deck.gl/react";
import { MVTLayer } from "@deck.gl/geo-layers";

function App() {
  const layer = new MVTLayer({
    data: `http://0.0.0.0:3000/finland/{z}/{x}/{y}`,
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
    <DeckGL
      viewState={viewState}
      onViewStateChange={(e) => setViewState(e.viewState)}
      controller={true}
      layers={[layer]}
    ></DeckGL>
  );
}

export default App;
// http://0.0.0.0:3000/finland/{z}/{x}/{y}
