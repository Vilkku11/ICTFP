import { useState, useRef, useEffect } from "react";

import ObjectHandler from "./ObjectHandler";

import "./InfoCard.css";
const InfoCard = ({ iconInfo, setIconInfo, testPlanes }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [content, setContent] = useState("");
  let cardRef = useRef();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (cardRef.current && !cardRef.current.contains(event.target)) {
        setIsOpen(false);
        setIconInfo(false);
      }
    };
    // Open Card only if data available
    if (Object.keys(iconInfo).length !== 0) {
      document.addEventListener("click", handleClickOutside);
      setIsOpen(true);
    }
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, [iconInfo]);

  useEffect(() => {
    if (isOpen) {
      console.log("isopen and going to objectHandler");
      // .planes ONLY NEEDED FOR TESTDATA
      const obj = testPlanes.find((obj) => obj.id === iconInfo.id);
      // const obj = planes.find((obj) => obj.id === planeInfo.id)

      if (obj) {
        setContent(<ObjectHandler obj={obj} />);
      } else {
        setContent(
          <div>
            <h2>No data</h2>
          </div>
        );
      }
    }
  }, [iconInfo, testPlanes]);
  return (
    <div>
      {isOpen && (
        <>
          <div className="content" ref={cardRef}>
            {content}
          </div>
        </>
      )}
    </div>
  );
};

export default InfoCard;
