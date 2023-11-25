import { useState, useRef, useEffect } from "react";

import "./InfoCard.css";
const InfoCard = ({ planeInfo, setPlaneInfo, testData }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [content, setContent] = useState("");
  let cardRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (cardRef.current && !cardRef.current.contains(event.target)) {
        setIsOpen(false);
        setPlaneInfo(false);
      }
    };

    // Open Card only if data available
    if (Object.keys(planeInfo).length !== 0) {
      document.addEventListener("click", handleClickOutside);
      setIsOpen(true);
      // .planes ONLY NEEDED FOR TESTDATA
      const obj = testData.planes.find((obj) => obj.id === planeInfo.id);

      if (obj) {
        setContent(
          <div>
            <ul>
              <li>id: {obj.id}</li>
              <li>flight: {obj.flight}</li>
              <li>latitude: {obj.coordinates[0]}</li>
              <li>longitude: {obj.coordinates[1]}</li>
              <li> altitude: {obj.altitude}</li>
            </ul>
          </div>
        );
      } else {
        setContent(
          <div>
            <h2>No data</h2>
          </div>
        );
      }
    }

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [planeInfo]);
  return (
    <div>
      {isOpen && (
        <>
          <div className="content" ref={cardRef}>
            <h1>tesr</h1>
            {content}
          </div>
        </>
      )}
    </div>
  );
};

export default InfoCard;
