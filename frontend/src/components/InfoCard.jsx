import { useState, useRef, useEffect } from "react";

const InfoCard = ({ isOpen, setIsOpen }) => {
  const drawerRef = useRef(null);

  const handleButtonClick = () => {
    setIsOpen(!isOpen);
  };

  const handleClickOutside = (event) => {
    if (drawerRef.current && !drawerRef.current.contains(event.target)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);
  return (
    <div className={`side-drawer ${isOpen ? "open" : ""}`} ref={drawerRef}>
      {isOpen && (
        <>
          <div className="header">
            <span className="close-button">&times;</span>
          </div>
          <div className="content">
            <h1>testtesxt</h1>
            <p>more test text</p>
          </div>
        </>
      )}
    </div>
  );
};

export default InfoCard;
