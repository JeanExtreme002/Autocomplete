import * as React from 'react';

import SearchBox from './SearchBox';
import SearchButton from './SearchButton';

import logo from '../resources/logo.png';
import './App.css';

function App() {
    return (
        <div className='App'>
            <header className='App-header'>
                <div className='container'>
                    <img src={logo} alt='logo' />
                    <div className='content'>
                        <h2>Busca com Autocompletar</h2>
                        <small>Digite no campo abaixo para exibir as sugestões.</small>
                        <div id='search-box'>
                            <SearchBox />
                        </div>
                        <SearchButton />
                    </div>
                </div>
            </header>
        </div>
    );
}

export default App;
