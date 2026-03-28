import "./ContentBox.css";
import { useState } from "react";

interface Props {
  title: string;
  value: string;
  odds: string;
  winnings: number;
  streak: number;
  children: string;
}

const OddsBox = ({ title, value, odds, winnings, streak, children }: Props) => {
  const [expanded, setExpanded] = useState(false);
  const [starred, setStarred] = useState(false);

  return (
    <div className="content-box main-content">
      <p className="content-title">
        {title}: {value}
      </p>
      <div className="content-separation">
        <p className="content-odds-streaks">Odds: {odds}</p>
        <p className="content-odds-streaks">{winnings}x winnings</p>
      </div>
      <div className="content-separation">
        <p className="content-odds-streaks">{streak} Game Streak</p>
        <div>
          <p className="content-odds-streaks">_/3 Last 3</p>
          <p className="content-odds-streaks">_/7 Last 7</p>
          <p className="content-odds-streaks">_/X Season</p>
        </div>
      </div>
      <div className="content-separation">
        <span
          className={`star-icon ${starred ? "starred" : ""}`}
          onClick={() => setStarred(!starred)}
        >
          {starred ? "★" : "☆"}
        </span>
        <button className="toggle-btn" onClick={() => setExpanded(!expanded)}>
          {expanded ? "less" : "more"}
        </button>
      </div>
      {expanded && <div className="content-details">{children}</div>}
    </div>
  );
};

export default OddsBox;
