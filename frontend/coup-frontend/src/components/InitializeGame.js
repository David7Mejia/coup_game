import React, { useEffect, useState } from "react";
import axios from "axios";

const InitializeGame = ({ setData }) => {
  const [numPlayers, setNumPlayers] = useState(3);

  const startGame = () => {
    axios
      .post("http://localhost:8000/api/set_players/", { num_players: Number(numPlayers), start: true })
      .then(response => {
        setData(response.data);
      })
      .catch(error => console.error("Error:", error));
  };
  return (
    <div className="player-count-container">
      <h1>How many players will join?</h1>
      <h2>(min:3 | max:6)</h2>
      <input className="player-input" type="number" value={numPlayers} onChange={e => setNumPlayers(e.target.value)} />
      <button onClick={startGame}>Start Game</button>
    </div>
  );
};

export default InitializeGame;
