import { useState } from 'react'
import Navbar from './Navbar.jsx'
import Home from './Home.jsx'
import './App.css'



function App() {
  //const [count, setCount] = useState(0)

  return (
    <>
      <div className='app-parent'>
        <Navbar />
        <Home />
      </div>
    </>
  );
}

export default App;
