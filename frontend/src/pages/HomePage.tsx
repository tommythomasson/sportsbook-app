import "./css/HomePage.css";

const HomePage = () => {
  const callBackend = async () => {
    const res = await fetch("http://localhost:8000/espn/mlb_player_stats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sports: ["MLB"] }),
    });

    const data = await res.json();
    console.log(data.result);
  };

  return (
    <div className="home container main-content">
      <div className="home-text">
        <h1>Hello</h1>
        <p>This is a betting analysis tool</p>
        <button className="btn">Click to start</button>
        <button className="btn" onClick={callBackend}>
          Grab espn mlb player data
        </button>
      </div>
    </div>
  );
};

export default HomePage;
