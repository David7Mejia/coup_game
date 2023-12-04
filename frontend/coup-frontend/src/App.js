// src/App.js
import React, { useEffect, useState } from "react";
import "./App.css";
import InitializeGame from "./components/InitializeGame";
import SummaryCard from "./components/SummaryCard";
//challenge
import Assassinate from "./components/Assassinate";
import Exchange from "./components/Exchange";
import Steal from "./components/Steal";
import Tax from "./components/Tax";
import Coup from "./components/Coup";
import cn from "classnames";

function App() {
  const [gameId, setGameId] = useState(null);
  const [gameInitialized, setGameInitialized] = useState(false);
  const [data, setData] = useState(null);
  const [treasury, setTreasury] = useState(null);
  const [deck, setDeck] = useState(null);
  const [turn, setTurn] = useState(null);
  const [players, setPlayers] = useState(/* your players state here */);

  //EXCHANGE
  const [selectedCardForExchange, setSelectedCardForExchange] = useState([]);
  //STEAL
  const [showSteal, setShowSteal] = useState(false);
  //ASSASSINATE
  const [showAssassinate, setShowAssassinate] = useState(false);
  //EXCHANGE
  const [showExchange, setShowExchange] = useState(false);
  //COUP
  const [showCoup, setShowCoup] = useState(false);

  // Handler to toggle the visibility of API components
  const toggleSteal = () => {
    setShowSteal(!showSteal);
  };

  const toggleAssassinate = () => {
    setShowAssassinate(!showAssassinate);
  };
  const toggleCoup = () => {
    setShowCoup(!showCoup);
  };

  const toggleExchange = () => {
    setShowExchange(!showExchange);
  };

  const handleGameInitialized = gameData => {
    if (gameData) {
      console.log("DAAAATAAAA: ", gameData);

      setGameId(gameData.game_data.game_id);
      setTreasury(gameData.game_data.treasury);
      setTurn(gameData?.game_data?.players[gameData.game_data.current_turn].name);
      setDeck(Object.values(gameData.game_data.deck_card_counts).reduce((a, b) => a + b));
      setPlayers(gameData.game_data.players);
      setGameInitialized(true);
    } else {
      // e.g., display an error message to the user
    }
  };

  const nextTurn = async () => {
    const response = await fetch(`http://localhost:8000/api/next_turn/${gameId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
    return data;
  };

  const challenge = async () => {
    const response = await fetch(`http://localhost:8000/api/challenge/${gameId}/`);
    const data = await response.json();
    console.log(data);
    return data;
  };

  const tax = async () => {
    const response = await fetch(`http://localhost:8000/api/tax/${gameId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
    nextTurn();

    return data;
  };

  const income = async () => {
    const response = await fetch(`http://localhost:8000/api/income/${gameId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
    nextTurn();
    return data;
  };

  const handleCardSelection = card => {
    const cardId = card.id; // Assuming each card has a unique 'id' attribute
    console.log("Selected Card ID:", cardId);

    setSelectedCardForExchange(prevSelected => {
      if (prevSelected.includes(cardId)) {
        return prevSelected.filter(id => id !== cardId); // Remove the card ID
      } else {
        return [...prevSelected, cardId]; // Add the card ID
      }
    });
  };

  const foreignAid = async () => {
    const response = await fetch(`http://localhost:8000/api/foreign_aid/${gameId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    setData(data);
    nextTurn();
    return data;
  };

  useEffect(() => {
    if (data) {
      handleGameInitialized(data);
    }
  }, [data]);

  return (
    <div className="App">
      {!gameInitialized ? (
        <InitializeGame setData={setData} />
      ) : (
        // Display the main game view or additional components here
        <div className="game-container">
          <h2>Let the Game Begin!</h2>
          <div className="top-container">
            <SummaryCard />
            <div className="game-info-holder">
              <p>Game ID: {gameId}</p>
              <p>Current Player: {turn} </p>
              <p>Treasury: {treasury}</p>
              <p>Deck: {deck}</p>
            </div>
            <div className="actions-holder">
              <h2>General Actions</h2>
              <div>
                <button onClick={() => income()}>Income</button>
                <button onClick={toggleCoup}>Coup</button>
                <button onClick={() => foreignAid()}>Foreign Aid</button>
                {/* <button onClick={() => challenge()}>Challenge</button> */}
              </div>
              <h2>Influence Actions</h2>
              <div>
                <button onClick={toggleAssassinate}>Assassin: Assassinate</button>
                <button onClick={toggleExchange}>Ambassador: Exchange</button>
                <button onClick={toggleSteal}>Captain: Steal</button>
                <button onClick={() => tax()}>Duke: Tax</button>
              </div>
            </div>
          </div>
          {showAssassinate && <Assassinate gameId={gameId} players={players} currentTurn={turn} setData={setData} nextTurn={nextTurn} />}
          {showCoup && <Coup gameId={gameId} players={players} currentTurn={turn} setData={setData} nextTurn={nextTurn} />}
          {showSteal && <Steal gameId={gameId} players={players} currentTurn={turn} setData={setData} nextTurn={nextTurn} />}
          {showExchange && (
            <Exchange
              gameId={gameId}
              players={players}
              currentTurn={turn}
              setData={setData}
              selectedCardForExchange={selectedCardForExchange}
              handleCardSelection={handleCardSelection}
              nextTurn={nextTurn}
            />
          )}
          <div className="player-container">
            {data &&
              data?.game_data?.players.map((player, i) => (
                <div key={player.id} className={`player ${i === 0 ? "player-bottom" : "player-top"}`}>
                  <div className="player-name">{i === 0 ? player.name : `Bot ${player.id + 1}`}</div>
                  <div className="player-info">
                    <div className="card-container">
                      Cards:
                      <div className="card-cols">
                        {player.cards.map((card, index) => {
                          if (player.id === 0) {
                            // Render with checkbox for the first player
                            return (
                              <label key={index}>
                                <input
                                  type="checkbox"
                                  name="selectedCard"
                                  value={index} // Using index as the value
                                  onChange={() => handleCardSelection(card)}
                                  checked={selectedCardForExchange.includes(card.id)}
                                />
                                <div
                                  className={cn("human-cards", {
                                    "card-1": card.type === "Duke",
                                    "card-2": card.type === "Assassin",
                                    "card-3": card.type === "Ambassador",
                                    "card-4": card.type === "Captain",
                                    "card-5": card.type === "Contessa",
                                  })}
                                >
                                  {card.type}
                                </div>
                              </label>
                            );
                          } else {
                            // Just display the card for other players
                            return (
                              <div
                                key={index}
                                className={cn("human-cards", {
                                  "card-1": card.type === "Duke",
                                  "card-2": card.type === "Assassin",
                                  "card-3": card.type === "Ambassador",
                                  "card-4": card.type === "Captain",
                                  "card-5": card.type === "Contessa",
                                })}
                              >
                                {`Card ${index + 1}`}
                              </div>
                            );
                          }
                        })}
                      </div>
                    </div>

                    <div>Coins: {player.coins}</div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
