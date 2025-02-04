import React from 'react';
import Navbar from './pages/navbar';
import PDFViewer from './pages/PDFViewer';
import Catalog from './pages/catalog';
//import Home from './pages/Home';
// import TextPrompt from './pages/textPrompt';
import './App.css'; 
import TextSender from './pages/textSender';

function App() {
  return (
    <div className="App">
      {/* <Navbar /> */}
      {/* <PDFViewer /> */}
      {/* <Catalog /> */}
      {/* <TextPrompt /> */}
      <TextSender />
    </div>
  );
}

export default App;