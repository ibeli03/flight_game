//päivittää tilaa, esim sää ja co2-päästöt

//importit
import {gameState} from "./gameState";
import {submitAnswers} from "./api";
import {updateUI, showGameOver, showScoreboard} from "./uiHandlers";

export async function handleAnswerSubmit(country, answers) {
    //lähetetään vastaukset backendiin ja saadaan tulos
    const result = await submitAnswers(country, answers);
    const starsEarned = result.correct;  //tähtiä oikeiden vastausten mukainen määrä
    const landingSuccess = result.landingSuccess   //pääseekö pelaaja maahan
    const weather = result.weather //onko sää hyvä vai huono

    if (landingSuccess) {
        gameState.visitedCountries.push(country);
        gameState.stars += starsEarned;
        gameState.co2 += 300; //onnistunut lento lisää 300kg co2
        gameState.currentCountry = country;
    }   else {
        if (weather === "Hyvä") {
            gameState.co2 += 300;  //hyvä sää eli edelliseen maahan voidaan palata
        }
    }
    //TÄÄLLÄ HÄMMENNYSTÄ ^^^ PITÄÄ KATTOA YHESSÄ MITEN TOI TOIMII

    //tarkistetaan ylittyykö co2-raja
    const limit = gameState.co2Limit + gameState.extendedLimit;
    if (gameState.co2 > limit) {
        showGameOver(); //näytä vaihtoehdot eli lopeta peli tai osta lisää co-rajaa
        return;
    }

    //tarkistetaan onhan kaikissa maissa käyty
    if (gameState.visitedCountries.lenght === 10) {
        showScoreboard();
        return;
    }

    updateUI(); //päivitetään käyttöliittymä
}