//pelin käynnistys, kysymysten haku, niiden näyttäminen käyttäjälle
//ja vastausten lähetys logiikkaan

//importit
import {fetchQuestions} from "./api.js";
import {handleAnswerSubmit} from "./gameLogic.js";

document.addEventListener("DOMContentLoaded", () => {
    startGame(); //käynnistetään peli, kun DOM on ladattu
});

async function startGame() {
    const country = chooseNextCountry(); //valitaan seuraava maa
    const questions = await fetchQuestions(country); //haetaan kysymykset
    renderQuestions(questions); //näytetään kysymykset

    //vastauksen käsittely
    document.getElementById('submit-btn').addEventListener('click', (e) => {
        const answers = getSelectedAnswers(); //haetaan vastaukset UI:sta
        handleAnswerSubmit(country, answers); //lähetetään ja käsitellään logiikassa
    })
}


//ALLA OLEVA ON JOKU CHATIN ESIMERKKI, EN TIIÄ MITE NOIDE KUULUS OLLA
// Esimerkkitoteutus: UI-rakenteesta riippuen nämä funktiot voi toteuttaa erikseen
function chooseNextCountry() {
  // Tässä voisi olla UI-valinta tai satunnaisvalinta
  return "Italia"; // Testausta varten
}

function renderQuestions(questions) {
  // Näytetään kysymykset DOM:iin (ei toteutettu tässä)
}

function getSelectedAnswers() {
  // Haetaan valitut vastaukset DOM-elementeistä
  return ["Rooma", "Oikea", "Väärä"]; // Esimerkki
}