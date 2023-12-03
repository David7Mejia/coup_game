import React, { useState } from "react";

const Coup = ({ gameId, players, currentTurn, setData }) => {
  const [selectedTargetPlayerID, setSelectedTargetPlayerID] = useState(null);
  const [cardToCoup, setCardToCoup] = useState(null);

  const coup = async (targetPlayerID, cardToCoup) => {
    const response = await fetch(`http://localhost:8000/api/coup/${gameId}/${targetPlayerID}/${cardToCoup}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log("response", response);
    setData(data);
    return data;
  };

  return (
    <div>
      <h3>Select a player to perform Coup!:</h3>
      {players.map(player => {
        if (`Player ${player.id + 1}` !== currentTurn) {
          return (
            <div key={player.id}>
              <button onClick={() => setSelectedTargetPlayerID(player.id)}>Coup against {player.name}</button>
            </div>
          );
        }
        return null;
      })}

      {selectedTargetPlayerID != null && (
        <div>
          <h3>Select an Influence card to Coup:</h3>
          {/* Assuming each player has a cards property which is an array of card names */}
          {players
            .find(player => player.id === selectedTargetPlayerID)
            .cards.map((card, index) => (
              <button key={index} onClick={() => setCardToCoup(index)}>
                Coup Card: {card}
              </button>
            ))}
        </div>
      )}

      {cardToCoup != null && <button onClick={() => coup(selectedTargetPlayerID, cardToCoup)}>Confirm Coup</button>}
    </div>
  );
};

export default Coup;
