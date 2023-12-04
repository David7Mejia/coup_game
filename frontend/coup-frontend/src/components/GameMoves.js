const GameMoves = ({ data }) => {
  return (
    <div className="move-box">
      {data?.game_data?.actions && data?.game_data?.actions.length > 0 ? (
        data?.game_data?.actions
          .slice()
          .reverse()
          .map((action, index) => <div key={index}>{action.action}</div>)
      ) : (
        <div>No actions yet</div>
      )}
    </div>
  );
};

export default GameMoves;
