import React, { useState } from "react";

const Assassinate = ({ gameId, players, currentTurn, setData }) => {
  const [selectedTargetPlayerID, setSelectedTargetPlayerID] = useState(null);
  const [cardToAssassinate, setCardToAssassinate] = useState(null);

  const assassinate = async (targetPlayerID, cardToAssassinate) => {
    const response = await fetch(`http://localhost:8000/api/assassinate/${gameId}/${targetPlayerID}/${cardToAssassinate}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    console.log("response", response);
    // setData(data);
    return data;
  };

  return (
    <div>
      <h3>Select a player to assassinate:</h3>
      {players.map(player => {
        if (`Player ${player.id + 1}` !== currentTurn) {
          return (
            <div key={player.id}>
              <button onClick={() => setSelectedTargetPlayerID(player.id)}>Assassinate {player.name}</button>
            </div>
          );
        }
        return null;
      })}

      {selectedTargetPlayerID != null && (
        <div>
          <h3>Select a card to assassinate:</h3>
          {/* Assuming each player has a cards property which is an array of card names */}
          {players
            .find(player => player.id === selectedTargetPlayerID)
            .cards.map((card, index) => (
              <button key={index} onClick={() => setCardToAssassinate(index)}>
                Assassinate Card: {card}
              </button>
            ))}
        </div>
      )}

      {cardToAssassinate != null && <button onClick={() => assassinate(selectedTargetPlayerID, cardToAssassinate)}>Confirm Assassinate</button>}
    </div>
  );
};

export default Assassinate;
