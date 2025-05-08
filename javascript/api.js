// JSON-pohjaiset API-kutsut tämän ja selaimen välillä

export async function fetchQuestions(country){ //haetaan maan kysymykset palvelimelta GET-pyynnöllä
    const response = await fetch(`/api/questions?country=${country}`)
    return response.json(); //vastaus JSON-muodossa
}

export async function submitAnswers(country, answers){ //lähetetään pelaajan vastaukset POST-pyynnöllä
    const response = fetch(`/api/submit`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'}, //ilmoitetaan JSON-muoto
        body: JSON.stringify({country, answers}) //muutetaan JSON-muotoon
    });
    return response.json();
}

