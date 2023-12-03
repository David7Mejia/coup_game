import React from "react";

const Tax = ({ gameId, setData }) => {
  const handleTax = async () => {
    const response = await fetch(`http://localhost:8000/api/tax/${gameId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
  };

  return <button onClick={handleTax}>Tax</button>;
};

export default Tax;
