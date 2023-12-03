import React, { useEffect, useState } from "react";

const Exchange = ({ gameId, setData, players, selectedCardForExchange }) => {
  const [temporaryCards, setTemporaryCards] = useState([]);
  const [selectedTemporaryCards, setSelectedTemporaryCards] = useState([]);
  const [exchangeCompleted, setExchangeCompleted] = useState(false);
  //   const [selectedCardForExchange, setSelectedCardForExchange] = useState(null);

  const exchange = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/exchange/${gameId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      setTemporaryCards(data.temporary_cards);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    exchange();
  }, []);

  const handleCardSelection = card => {
    // If the card is already selected, deselect it
    if (selectedTemporaryCards.includes(card)) {
      setSelectedTemporaryCards(prevSelected => prevSelected.filter(selectedCard => selectedCard !== card));
    } else {
      // If the card is not selected, select it
      setSelectedTemporaryCards(prevSelected => [...prevSelected, card]);
    }
  };

  const handleExchangeConfirmation = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/exchange/confirm/${gameId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          selected_temporary_cards: selectedTemporaryCards,
          selected_card_for_exchange: selectedCardForExchange,
        }),
      });
      const data = await response.json();
      setData(data);
      setExchangeCompleted(true);
      // Optionally handle the updated game state from the response
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      {temporaryCards.length > 0 && !exchangeCompleted && (
        <div>
          <h3>Temporary Cards</h3>
          {temporaryCards.map((card, index) => (
            <div key={index} onClick={() => handleCardSelection(card)} className={selectedTemporaryCards.includes(card) ? "selected-card" : ""}>
              {card}
            </div>
          ))}
          <button onClick={() => handleExchangeConfirmation()}>Confirm Exchange</button>
        </div>
      )}
      {exchangeCompleted && (
        <div>
          <p>Exchange completed!</p>
          {/* Additional UI or actions after the exchange */}
        </div>
      )}
    </div>
  );
};

export default Exchange;