import './NavBar.css';
import logo from '../../assets/images.png';
import { Link } from 'react-router-dom';

const NavBar = () => {

  return (
      <nav className='container'>
        <img src={logo} alt="" className="logo"/>
          <Link to='/'>Home</Link>
          <Link to='/favorites'>Favorites</Link>
          <Link to='/sports'>Sports</Link>
          <li>About</li>
          <li><button className="btn">Contact Us</button></li>
      </nav>
  )
}

export default NavBar;
