import React, { useState } from "react";

const Assassinate = ({ gameId, players, currentTurn, setData, nextTurn }) => {
  const [selectedTargetPlayerID, setSelectedTargetPlayerID] = useState(null);
  const [cardToAssassinate, setCardToAssassinate] = useState(null);
  const currentPlayer = players.find(player => player.id === currentTurn - 1); // Assuming currentTurn starts from 1

  const assassinate = async (targetPlayerID, cardToAssassinate) => {
    const response = await fetch(`http://localhost:8000/api/assassinate/${gameId}/${targetPlayerID}/${cardToAssassinate}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
    nextTurn(`Player 1 Assassinated Card from Player ${players[targetPlayerID].name}`);

    return data;
  };

  return (
    <div>
      <h3>Select a player to assassinate:</h3>
      {players.map(player => {
        if (`Player ${player.id + 1}` !== currentTurn) {
          return (
            <div key={player.id}>
              <button
                onClick={() => setSelectedTargetPlayerID(player.id)}
                disabled={currentPlayer && currentPlayer.coins < 3} // Disable button if current player has less than 3 coins
              >
                Assassinate {player.name}
              </button>
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
                Assassinate Card: {card.type} {/* Display the card type or any relevant property */}
              </button>
            ))}
        </div>
      )}

      {cardToAssassinate != null && <button onClick={() => assassinate(selectedTargetPlayerID, cardToAssassinate)}>Confirm Assassinate</button>}
    </div>
  );
};

export default Assassinate;
