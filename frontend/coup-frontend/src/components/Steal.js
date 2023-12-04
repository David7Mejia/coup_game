import React, { useState } from "react";

const Steal = ({ gameId, players, currentTurn, setData, nextTurn }) => {
  const [selectedTargetPlayerID, setSelectedTargetPlayerID] = useState(null);

  const steal = async targetPlayerID => {
    const response = await fetch(`http://localhost:8000/api/steal/${gameId}/${targetPlayerID}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
    nextTurn(`Player 1 Stole 2 coins from Player ${players[targetPlayerID].name}`);

    return data;
  };

  return (
    <div>
      <h3>Select a player to steal from:</h3>
      {players.map(player => {
        if (`Player ${player.id + 1}` !== currentTurn) {
          // Exclude the current player
          return (
            <div key={player.id}>
              <button onClick={() => setSelectedTargetPlayerID(player.id)}>Steal from {player.name}</button>
            </div>
          );
        }
        return null;
      })}

      {selectedTargetPlayerID != null && <button onClick={() => steal(selectedTargetPlayerID)}>Confirm Steal</button>}
    </div>
  );
};

export default Steal;
