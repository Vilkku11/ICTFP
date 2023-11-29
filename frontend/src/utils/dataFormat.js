export const roundToDecimal = (number, decimals) => {
  return Number(number.toFixed(decimals));
};

export const calculateHeading = (velocity) => {
  const headingRad = Math.atan2(velocity[0], velocity[1]);
  let headingDeg = headingRad * (180 / Math.PI);
  if (headingDeg < 0.0) {
    return roundToDecimal((headingDeg += 360.0),1);
  } else {
    return roundToDecimal(headingDeg, 1);
  }
};
