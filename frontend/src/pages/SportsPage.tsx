import "./css/SportsPage.css"
import OddsBox from "../components/ContentBox/OddsBox";
import ComputeComponent from "../components/compute";

const SportsPage = () => {
  return (
    <div>
      <h1 className="page-title">Sport</h1> {/* make this a dropdown */}
      <div className="content-grid smaller">
        <OddsBox title="Bryce Harper O/U Hits" value="1+" odds="+100" winnings={2} streak={3}>
          This is where additional betting data will be placed such as
          probability, opponent ranking, over/under-valued
        </OddsBox>
        <ComputeComponent/>
      </div>
    </div>
  );
};
// could do a banner across the top of screen, potentially scrollable with each available sport
// could do the same underneath with available games
export default SportsPage;
