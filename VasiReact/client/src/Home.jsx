import { useState } from 'react'
import './Home.css'


function Home() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='home-parent'>
        <div className='header-text'>Education.<br></br>Panelized into<br></br>Comics.</div>
      </div>
    </>
  );
}

export default Home;
