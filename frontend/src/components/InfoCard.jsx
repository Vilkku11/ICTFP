import { useState, useRef, useEffect } from "react";

import "./InfoCard.css";
const InfoCard = ({ planeInfo, setPlaneInfo }) => {
  const [isOpen, setIsOpen] = useState(false);
  let cardRef = useRef();

  useEffect(() => {
    console.log("adding infocard component");
    const handleClickOutside = (event) => {
      if (cardRef.current && !cardRef.current.contains(event.target)) {
        console.log("CLICKED OUTSIDE");
        setIsOpen(false);
        setPlaneInfo(false);
      }
    };
    if (Object.keys(planeInfo).length !== 0) {
      document.addEventListener("click", handleClickOutside);
      console.log("setIsOpen to true");
      setIsOpen(true);
    }

    return () => {
      console.log("removing infocard component");
      document.removeEventListener("click", handleClickOutside);
    };
  }, [planeInfo]);

  return (
    <div>
      {isOpen && (
        <>
          <div className="content" ref={cardRef}>
            <h1>testtesxt</h1>
            <p>more test text</p>
          </div>
        </>
      )}
    </div>
  );
};

export default InfoCard;
