import React from 'react';
import './Navbar.css'; // Make sure to create a corresponding CSS file for styling
import logo from '../assets/doodlegyanlogo.png'; // Make sure to import the logo image

function Navbar() {
  return (
    <div className = "parent">
    <nav className="navbar">
      <div className="navbar-left">
        <img src={logo} alt="Logo" className="navbar-icon" />
      </div>
      <div className="navbar-center">
        <a href="#home" className="navbar-link">Home</a>
        <a href="#about" className="navbar-link">About</a>
        <a href="#services" className="navbar-link">Services</a>
        <a href="#contact" className="navbar-link">Contact</a>
      </div>
      <div className="navbar-right">
        <button className="navbar-button">Login</button>
        <button className="navbar-button">Sign Up</button>
      </div>
    </nav>
    </div>
  );
}

export default Navbar;