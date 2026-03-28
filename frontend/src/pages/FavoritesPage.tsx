import "./css/FavoritesPage.css";
import ContentBox from "../components/ContentBox/ContentBox";
import testPlot from "../assets/test_plot.png";

// needs a list of content boxes to display
// trigger creation of new content box after clicking button

const FavortiesPage = () => {
  return (
    <div>
      <h1 className="page-title">Favorites</h1>
      <div className="content-grid">
        <ContentBox image={testPlot} title="Test Plot">
          This is where additional betting data will be placed such as
          probability, opponent ranking, over/under-valued
        </ContentBox>
        <ContentBox image={testPlot} title="Test Plot">
          This is where additional betting data will be placed such as
          probability, opponent ranking, over/under-valued
        </ContentBox>
        <ContentBox image={testPlot} title="Test Plot">
          This is where additional betting data will be placed such as
          probability, opponent ranking, over/under-valued
        </ContentBox>
        <ContentBox image={testPlot} title="Test Plot">
          This is where additional betting data will be placed such as
          probability, opponent ranking, over/under-valued
        </ContentBox>
        <div className='centered-button-wrapper'>
          <button className='new-box-btn'>+ Create New Analysis</button>
        </div>
        {/* <CreateContentBox /> */}
        {/* if unstarred then pop from the list of favorites */}
      </div>
    </div>
  );
};

export default FavortiesPage;
