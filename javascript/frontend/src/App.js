//src/App.js

//importit
import React, {useState, useEffect} from 'react';
import './App.css';
import {gameState as updatedState} from "../../gameState";

function App() {
  //peliin liittyvät tilat
  const [countries, setCountries] = useState([]);    //lista maista
  const [selectedCountries, setSelectedCountries] = useState("");  //valittu maa
  const [questions, setQuestions] = useState([]);  //kysymykset valitusta maasta
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);  //laskee, monennessako kysymyksessä mennään kolmesta
  const [userAnswer, setUserAnswer] = useState([]);  //pelaajan vastaukset
  const [gameState, setGameState] = useState({
    stars: 0,
    co2: 0,
    visitedCountries: [],
    gameOver: false,
  });

  useEffect(() => {
    //kun komponentti renderöityy ensimmäistä kertaa
    const fetchCountries = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/countries");
        if (!response.ok) throw new Error("Maita ei saatu haettua");
        const data = await response.json();
        setCountries(data);
      }
      catch (error) {
        console.error("Virhe haettaessa: ", error);
      }
    };
    fetchCountries();
  }, []);

  //pelaaja valitsee maan ja kysymykset arvotaan
  const handleCountrySelect = (country) => {
    setSelectedCountries(country);
    setCurrentQuestionIndex(0);
    setUserAnswers([])  ;

    fetch(`http://localhost:8000/api/questions/${country}`)
    .then((res) => res.json())
    .then((data) => setQuestions(data))
    .catch((err) => console.error("Virhe kysymyksien haussa.",err));
  };

  //vastaus backendille ja tarkistus
  const handleUserAnswer = (userAnswer) => {
    const currentQuestion= ((prev) => prev + 1);

    fetch(`http://localhost:8000/api/check_answer`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        question_id: currentQuestion.id,
        userAnswer: userAnswer,
      }),
    })
    .then((res) => res.json())
    .then((data) => {
      setUserAnswers((prev) => [...prev, data.correct]);

      //jos ei olla vielä kolmannessa kysymyksessä, siirrytään seuraavaan
      if (currentQuestionIndex < 2) {
        setCurrentQuestionIndex((prev) => prev + 1);
      } else {
        //kaikkiin kysymyksiin on vastattu
        handleQuestionResults([...userAnswers, data.correct]);
      }
    });
};

//käsitellään tulos
const handleQuestionResults = (answers) => {
  const correctCount = answers.filter(Boolean).lenght;
  const starsEarned = correctCount;
  const passed = correctCount >= 1;

  let newCO2 = gameState.co2 + 300; //aina tulee 300kg päästöjä
  let updatedState = {
    ...gameState,
    co2: newCO2,
  };

  if (passed) {
    updatedState.stars += starsEarned;
    updatedState.visitedCountries.push(selectedCountries);
  }

  //peli päättyy, jos co2 raja ylittyy, eikä voi ostaa lisää
  if (updatedState.co2 > 3600 && updatedState.stars === 0) {
    updatedState.gameOver = true;
  }

  //päivitetään pelitila ja tyhjennetään maa + kysymykset
  setGameState(updatedState);
  selectedCountries("");
  setQuestions([])
  setCurrentQuestionIndex(0);
  setUserAnswer([]);
};

//game over -näkymä
  if (gameState.gameOver) {
    return (
        <div className="App">
          <h1>GAME OVER</h1>
          <p>CO2 päästöraja ylitetty.</p>
          <p>Tähdet: {gameState.stars}</p>
        </div>
    );
  }

  //normaali näkymä
  return (
      <div className="App">
        <h1>Lennä ja tiedä!</h1>
        <p>CO₂: {gameState.co2} / 3600 kg</p>
        <p>Tähdet: {gameState.stars} / 30</p>

        {/*jos ei ole valittua maata, näytetään maat */}
        {selectedCountries === "" ?(
            <div>
              <h2>Valitse maa:</h2>
              <ul>
                {countries
                    .filter((c) => !gameState.visitedCountries.includes(c))
                    .map((country) => (
                        <li key={country}>
                          <button onClick={() =>handleCountrySelect(country)}>
                            {country}
                          </button>
                        </li>
                    ))}
              </ul>
            </div>
        )  :  questions.lenght > 0 ? (
            <div>
              <h2>{selectedCountries}</h2>
              <p>{questions[currentQuestionIndex].text}</p>
              {questions[currentQuestionIndex].options.map((opt, i) =>(
                  <button key={i} onClick={() => handleUserAnswer(opt)}>
                    {opt}
                  </button>
              ))}
            </div>
        )  : (
            <p>Ladataan kysymyksiä...</p>
        )}
    </div>
  );
}

export default App;
