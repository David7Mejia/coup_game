// src/App.js
import React, { useEffect, useState } from "react";
import "./App.css";
import InitializeGame from "./components/InitializeGame";
import SummaryCard from "./components/SummaryCard";
//challenge
import Assassinate from "./components/Assassinate";
//exchange
import Steal from "./components/Steal";
import Tax from "./components/Tax";
import Exchange from "./components/Exchange";
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
  const [temporaryCards, setTemporaryCards] = useState([]);
  const [selectedCards, setSelectedCards] = useState([]);
  const [exchangeCompleted, setExchangeCompleted] = useState(false);
  const [selectedTemporaryCards, setSelectedTemporaryCards] = useState([]);
  const [selectedCardForExchange, setSelectedCardForExchange] = useState(null);

  //STEAL
  const [showSteal, setShowSteal] = useState(false);
  //ASSASSINATE
  const [showAssassinate, setShowAssassinate] = useState(false);
  //EXCHANGE
  const [showExchange, setShowExchange] = useState(false);
  // Handler to toggle the visibility of the Steal component
  const toggleSteal = () => {
    setShowSteal(!showSteal);
  };
  const toggleAssassinate = () => {
    setShowAssassinate(!showAssassinate);
  };
  const toggleExchange = () => {
    setShowExchange(!showExchange);
  };

  const handleGameInitialized = gameData => {
    if (gameData) {
      console.log("DAAAATAAAA: ", gameData);

      setGameId(gameData.game_data.game_id);
      setTreasury(gameData.game_data.treasury);
      setTurn(gameData.game_data.players[gameData.game_data.current_turn].name);
      setDeck(Object.values(gameData.game_data.deck_card_counts).reduce((a, b) => a + b));
      setPlayers(gameData.game_data.players);
      setGameInitialized(true);
    } else {
      // Handle any initialization errors
      // e.g., display an error message to the user
    }
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
    return data;
  };

  // const exchange = async () => {
  //   try {
  //     const response = await fetch(`http://localhost:8000/api/exchange/${gameId}/`, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //     });
  //     const data = await response.json();
  //     setTemporaryCards(data.temporary_cards);
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  // const handleCardSelection = card => {
  //   // If the card is already selected, deselect it
  //   if (selectedTemporaryCards.includes(card)) {
  //     setSelectedTemporaryCards(prevSelected => prevSelected.filter(selectedCard => selectedCard !== card));
  //   } else {
  //     // If the card is not selected, select it
  //     setSelectedTemporaryCards(prevSelected => [...prevSelected, card]);
  //   }
  // };

  // const handleExchangeConfirmation = async () => {
  //   try {
  //     const response = await fetch(`http://localhost:8000/api/exchange/confirm/${gameId}/`, {
  //       method: "PUT",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         selected_temporary_cards: selectedTemporaryCards,
  //         selected_card_for_exchange: selectedCardForExchange,
  //       }),
  //     });
  //     const data = await response.json();
  //     setData(data);
  //     setExchangeCompleted(true);
  //     // Optionally handle the updated game state from the response
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

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
            <div>
              <p>Game ID: {gameId}</p>
              <p>Current Player: {turn} </p>
              <p>Treasury: {treasury}</p>
              <p>Deck: {deck}</p>
            </div>
            <div>
              <h2>Actions</h2>
              <div>
                <p onClick={() => challenge()}>Challenge</p>
                <button onClick={toggleAssassinate}>Assassin: Assassinate</button>
                {/* <Exchange gameId={gameId} setData={setData} players={players} /> */}
                <button onClick={toggleExchange}>Ambassador: Exchange</button>
                <button onClick={toggleSteal}>Captain: Steal</button>
                <button onClick={() => tax()}>Duke: Tax</button>
              </div>
            </div>
          </div>
          {showAssassinate && <Assassinate gameId={gameId} players={players} currentTurn={turn} setData={setData} />}
          {showSteal && <Steal gameId={gameId} players={players} currentTurn={turn} setData={setData} />}
          {/* {showExchange && <h1>HELLO</h1>} */}
          {showExchange && <Exchange gameId={gameId} players={players} currentTurn={turn} setData={setData} selectedCardForExchange={selectedCardForExchange} />}
          <div className="player-container">
            {data &&
              data.game_data.players.map((player, i) => (
                <div key={player.id} className={`player ${i === 0 ? "player-bottom" : "player-top"}`}>
                  <div className="player-name">{i === 0 ? player.name : `Bot ${player.id + 1}`}</div>
                  <div className="player-info">
                    <div className="card-container">
                      Cards:
                      <div className="card-cols">
                        {player.cards.map((card, i) => (
                          <label key={i}>
                            <input type="radio" name="selectedCard" value={card} onChange={() => setSelectedCardForExchange(card)} checked={selectedCardForExchange === card} />
                            <div
                              className={cn("human-cards", {
                                "card-1": card === "Duke",
                                "card-2": card === "Assassin",
                                "card-3": card === "Ambassador",
                                "card-4": card === "Captain",
                                "card-5": card === "Contessa",
                              })}
                            >
                              {card}
                            </div>
                          </label>
                        ))}
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
