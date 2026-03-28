import './css/HomePage.css'

const HomePage = () => {

  const callBackend = async () => {
    const res = await fetch("http://localhost:8000/draftkings/sport_odds", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sports: ["NHL"] }),
    });

    const data = await res.json();
    console.log(data.result);
  };

  return (
    <div className='home container main-content'>
        <div className='home-text'>
            <h1>Hello World</h1>
            <p>This is a betting analysis tool</p>
            <button className='btn'>Click to start</button>
            <button className='btn' onClick={callBackend}>Grab DraftKings sports data</button>
        </div>
    </div>
  );
}

export default HomePage