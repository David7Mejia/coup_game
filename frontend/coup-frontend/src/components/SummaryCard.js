import React from "react";

const SummaryCard = () => {
  return (
    <div className="summary-container">
      <table className="summary-table">
        <thead>
          <tr>
            <th>Character</th>
            <th>Action</th>
            <th>Effect</th>
            <th>Counteraction</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="column-box">--------</td>
            <td className="column-box">Income</td>
            <td className="column-box">Take 1 coin from treasury</td>
            <td className="column-box">--------</td>
          </tr>

          <tr>
            <td className="column-box">--------</td>
            <td className="column-box">Foreign Aid</td>
            <td className="column-box">Take 2 coins from treasury</td>
            <td className="column-box">--------</td>
          </tr>
          <tr>
            <td className="column-box">--------</td>
            <td className="column-box">Coup</td>
            <td className="column-box">Pay 7 coins to treasury</td>
            <td className="column-box">--------</td>
          </tr>
          <tr>
            <td className="column-box">DUKE</td>
            <td className="column-box">Tax</td>
            <td className="column-box">Take 3 coins from treasury</td>
            <td className="column-box">Block Foreign Aid</td>
          </tr>
          <tr>
            <td className="column-box">ASSASSIN</td>
            <td className="column-box">Assassinate</td>
            <td className="column-box">Pay 3 coins (Choose Player's Influence')</td>
            <td className="column-box">--------</td>
          </tr>
          <tr>
            <td className="column-box">AMBASSADOR</td>
            <td className="column-box">Exchange</td>
            <td className="column-box">Exchange cards with court deck</td>
            <td className="column-box">Block Stealing</td>
          </tr>
          <tr>
            <td className="column-box">CAPTAIN</td>
            <td className="column-box">Steal</td>
            <td className="column-box">Take 2 coins from another player</td>
            <td className="column-box">Block Stealing</td>
          </tr>
          <tr>
            <td className="column-box">CONTESSA</td>
            <td className="column-box">--------</td>
            <td className="column-box">--------</td>
            <td className="column-box">Block Assassination</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SummaryCard;
