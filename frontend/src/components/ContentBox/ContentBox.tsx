import "./ContentBox.css";
import { useState } from "react";

interface Props {
  image: string;
  title: string;
  children: string;
  // content: string[];
}

const ContentBox = ({ image, title, children }: Props) => {
  const [expanded, setExpanded] = useState(false);
  const [starred, setStarred] = useState(false);

  return (
    <div className="content-box main-content">
      <img className="content-img" src={image} alt="" />
      <p className="content-title">{title}</p>
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

export default ContentBox;
