//pelitilan hallinta
import React, { useState } from 'react'

const [gameState, setGameState] = useState({})

export const gameState= {
    currentCountry: null,
    visitedCountries: [],
    stars: 0,
    co2 : 0,
    co2Limit: 3600,
    extendedLimit: 0,  //kuinka paljon päästörajaa on nostettu ostamalla sitä tähdillä
    gameOver: false   //onko peli päättynyt
};

