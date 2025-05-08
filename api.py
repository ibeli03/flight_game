#python puolen API-yhteys
#paljon puutteita ja avonaisia kysymyksiä xdd

#importit
from fastapi import FastAPI, Request
from pydantic import BaseModel #datan tarkastusta ja jäsentämistä automaattisesti
from fastapi.middleware.cors import CORSMiddleware #ratkaisee selaimen suojausrajoituksen CORS (Cross-Origin Resource Sharing)
import sqlite3 #tietokannan käsittelyyn
from fastapi.responses import JSONResponse #virheviestien palauttamiseen
app = FastAPI()

#sallii yhteydet
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#haetaan kysymykset tietokannasta
@app.get("/api/questions")
def get_questions(country: str):
    try:
        conn = sqlite3.connect("questions.db") #yhdistetään tietokantaan
        cursor = conn.cursor()


        #!!!!TÄMÄ KOHTA AINAKIN PITÄÄ MUOKATA PAREMMIN MEIDÄN PELIIN SOPIVAKSI
        #haetaan kysymykset annetulle maalle
        cursor.execute("SELECT kysymys, vaihtoehdot, oikea_vastaus FROM questions WHERE maa = %s" (country)),
        rows = cursor.fetchall()
        conn.close()

        #jos ei löydy kysymyksiä
        if not rows:
            return JSONResponse(status_code=404, content={"Virhe"})

        #muotoillaan frontendille sopivaksi
        questions = []
        for row in rows:
            questions.append({
                "kysymys": row[0],
                "vaihtoehdot": row[1],
                "oikea_vastaus": [row[2], row[3], row[5]]
            })

        return questions

    #jos tulee esim. tietokantavirhe
    except Exception as e:
        return JSONResponse(status_code=500, content={"Virhe"})

class submitRequest(BaseModel):
    country: str #mihin maahan yritetään lentää
    question_id: int #kysymyksen id
    answer: str #pelaajan vastaus

@app.post("/api/submit")
def submit(data: submitRequest):
    try:
        conn = sqlite3.connect("questions.db")
        cursor = conn.cursor()

        #!!!!TÄMÄ KOHTA AINAKIN PITÄÄ MUOKATA PAREMMIN MEIDÄN PELIIN SOPIVAKSI
        cursor.execute("SELECT oikea_vastaus FROM kysymys WHERE maa = %s", (data.country,)),
        correct_row = cursor.fetchone()
        conn.close()

        if not correct_row:
            return JSONResponse(status_code=404, content={"Virhe": "Kysymystä ei löytynyt."})

        correct_answer = int(correct_row[0])

        is_correct = (correct_answer == data.answer)

        return {
            "correct": is_correct,
            "message": "Oikein!" if is_correct else "Väärin meni.",
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"Virhe vastausten tarkistamisessa."})

