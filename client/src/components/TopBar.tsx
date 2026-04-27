//components/TopBar.tsx

export default function TopBar({ onStart, onStep, onReset }: any) {
  return (
    <div className="topbar">
      <div className="title">SENTINEL FORGE</div>

      <div className="controls">
        <button onClick={onStart}>START</button>
        <button onClick={onStep}>STEP</button>
        <button onClick={onReset}>RESET</button>
      </div>

      <div className="status">LIVE</div>
    </div>
  );
}