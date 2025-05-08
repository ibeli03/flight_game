//vastaa pelin tilan näkymisestä käyttöliittymässä

//importit
import {gameState} from ".gameState.js";

export function updateUI() {  //päivitetään tähdet ja päästöt näkyviin
    document.getElementById("stars").textContent = `${gameState.stars}`;
    document.getElementById("co2").textContent = `${gameState.co2} / ${gameState.co2Limit}`;
}

export function showGameOver() {
    //näytetään game over -ikkuna ja valinta siitä, haluaako ostaa tähdillä lisää co2-päästörajaa
    alert("GAME OVER - ylitit päästörajasi\nKäytä tähtiä tai lopeta peli");
}

export function showScoreboard() {
    //loppunäkymä eli lopulliset tähdet ja päästöt
    alert(`Onnittelut! Kävit kaikissa maissa ja suoritit pelin loppuun!\n
    Tähdet: ${gameState.stars} / 30\nPäästöt: ${gameState.co2} / 3600kg
    (korotettu: ${gameState.co2Limit + gameState.extendedLimit} kg)`);
}