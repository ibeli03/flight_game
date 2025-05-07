import mysql.connector
import time
import json
import random
import math


class Pelaaja:
    def __init__(self, nimi, nykyinen_maa="Suomi", tähdet=0, vieraillut_maat=None):
        if vieraillut_maat is None:
            vieraillut_maat = []
        self.nimi = nimi
        self.nykyinen_maa = nykyinen_maa
        self.tähdet = tähdet
        self.vieraillut_maat = vieraillut_maat

    def lisää_tähdet(self, määrä):
        self.tähdet += määrä

    def vähennä_tähdet(self, määrä):
        self.tähdet -= määrä

    def lisää_vieraillut_maa(self, maa):
        if maa not in self.vieraillut_maat:
            self.vieraillut_maat.append(maa)

    def __str__(self):
        return f"Player: {self.nimi}, Tähdet: {self.tähdet}, Nykyinen Maa: {self.nykyinen_maa}"


class Kysmys:
    def __init__(self, kysymys, vaihtoehdot, oikea_vastaus):
        self.kysymys = kysymys
        self.vaihtoehdot = json.loads(vaihtoehdot)  # Assuming it's a JSON string
        self.oikea_vastaus = oikea_vastaus

    def esita_kysymys(self):
        print(f"\n{self.kysymys}")
        for key, value in self.vaihtoehdot.items():
            print(f"{key}. {value}")

    def tarkista_vastaus(self, vastaus):
        return vastaus == self.oikea_vastaus


class CO2Manager:

    EMISSION_FACTOR = 0.115  # grams / km
    CO2_THRESHOLD = 2000  # Päästöraja grammoina

    def __init__(self):
        self.total_emissions = 0

    def calculate_distance(self, country1, country2):
        def calculate_distance(self, country1, country2):
            # Etäisyydet eri maiden välillä (kilometreinä)
            distances = {
                ("Suomi", "Italia"): 2200,
                ("Suomi", "Espanja"): 2500,
                ("Suomi", "Ruotsi"): 500,
                ("Suomi", "Norja"): 600,
                ("Suomi", "Tanska"): 1200,
                ("Suomi", "Ranska"): 2200,
                ("Suomi", "Saksa"): 1600,
                ("Suomi", "Alankomaat"): 1600,
                ("Suomi", "Englanti"): 1700,
                ("Italia", "Espanja"): 1200,
                ("Italia", "Ruotsi"): 1900,
                ("Italia", "Ranska"): 700,
                ("Italia", "Saksa"): 1000,
                ("Italia", "Alankomaat"): 1300,
                ("Italia", "Englanti"): 1400,
                ("Espanja", "Ruotsi"): 2300,
                ("Espanja", "Ranska"): 1200,
                ("Espanja", "Saksa"): 1500,
                ("Espanja", "Alankomaat"): 1600,
                ("Espanja", "Englanti"): 1300,
                ("Ruotsi", "Norja"): 500,
                ("Ruotsi", "Tanska"): 600,
                ("Ruotsi", "Ranska"): 1800,
                ("Ruotsi", "Saksa"): 1200,
                ("Ruotsi", "Alankomaat"): 1300,
                ("Ruotsi", "Englanti"): 1500,
                ("Ranska", "Saksa"): 500,
                ("Ranska", "Alankomaat"): 400,
                ("Ranska", "Englanti"): 300,
                ("Saksa", "Alankomaat"): 200,
                ("Saksa", "Englanti"): 600,
                ("Alankomaat", "Englanti"): 350
            }

        distance = distances.get((country1, country2)) or distances.get((country2, country1))
        return distance

    def update_emissions(self, country1, country2):
        distance = self.calculate_distance(country1, country2)
        emissions = distance * self.EMISSION_FACTOR
        self.total_emissions += emissions
        return emissions

    def get_total_emissions(self):
        return self.total_emissions

    def can_afford_emissions(self, player_stars):
        # Each star represents 100g of CO2 emissions (example ratio)
        return player_stars * 100 >= self.total_emissions

    def calculate_emissions_cost(self, player_stars):

        emissions_covered = player_stars * 100
        emissions_to_pay = self.total_emissions - emissions_covered
        return emissions_to_pay


class Peli:
    def __init__(self, pelaaja, yhteys):
        self.pelaaja = pelaaja
        self.yhteys = yhteys
        self.cursor = self.yhteys.cursor()
        self.co2_manager = CO2Manager()  # Instantiate CO2Manager

    def intro(self, text):
        for i in text:
            print(i, end="")
            time.sleep(0.030)
        print()
        time.sleep(len(text) / 1000)

    def aloita(self):
        self.intro("Tervetuloa Lennä ja tiedä! -peliin, jossa opit lisää eri Euroopan maista!")
        self.intro("Tässä pelissä saat tähtiä oikein vastatuista kysymyksistä eri maista, joihin olet lentämässä.")
        self.intro(
            "Pelin lopussa sinulle kerrotaan montako tähteä, eli pistettä, olet kerännyt. Maksimi pistemäärä on 30.")
        self.intro("Oletko ymmärtänyt ohjeet? Paina enter aloittaaksesi!")
        input("")
        self.intro(
            "Olet Helsinki-Vantaan lentokentällä. Olet saanut tarpeeksesi Suomen kylmyydestä ja haluat vaihtaa maisemaa.")
        self.alusta_peli()

    def alusta_peli(self):
        # Poistetaan vanhat pelit ennen uuden aloittamista
        self.cursor.execute("Delete FROM player_state")
        sql = "INSERT INTO player_state (nykyinen_maa, tähdet, vieraillut_maat) VALUES (%s, %s, %s)"
        arvot = ("Suomi", 0, "[]")
        self.cursor.execute(sql, arvot)
        self.yhteys.commit()

        while True:
            self.play_round()

    def play_round(self):
        # Haetaan vieraillut maat tietokannasta
        self.cursor.execute("SELECT vieraillut_maat FROM player_state")
        result = self.cursor.fetchone()

        if result:
            self.pelaaja.vieraillut_maat = json.loads(result[0])

        # Haetaan kaikki maat
        self.cursor.execute("SELECT id, maa FROM airports")
        tulos = self.cursor.fetchall()

        saatavilla_olevat_maat = sorted([x for x in tulos if x[1] not in self.pelaaja.vieraillut_maat],
                                        key=lambda x: x[0])

        if not saatavilla_olevat_maat:
            self.pelaaja_loppu()

        print('\nValitse seuraava kohdemaa.')
        for x in saatavilla_olevat_maat:
            print(x)

        maa_id = int(input('\nAnna kohdemaata vastaava numero: '))
        kohdemaa_query = "SELECT maa, nimi FROM airports WHERE id = %s"
        self.cursor.execute(kohdemaa_query, (maa_id,))
        rivit = self.cursor.fetchall()

        if rivit:
            kohdemaa, nimi = rivit[0]
            print(f'Olet matkalla maahan {kohdemaa}, kentälle {nimi}.')
            self.pelaaja.nykyinen_maa = kohdemaa

            oikeat_vastaukset = 0
            kysymykset_query = "SELECT kysymys, vaihtoehdot, oikea_vastaus FROM questions WHERE maa = %s"
            self.cursor.execute(kysymykset_query, (kohdemaa,))
            questions = self.cursor.fetchall()

            random.shuffle(questions)
            questions = questions[:3]

            for kysymys, vaihtoehdot, oikea_vastaus in questions:
                kysymys_obj = Kysmys(kysymys, vaihtoehdot, oikea_vastaus)
                kysymys_obj.esitä_kysymys()

                while True:
                    vastaus = input("Valitse oikea vaihtoehto (A/B/C): ").strip().upper()
                    if vastaus in kysymys_obj.vaihtoehdot:
                        break
                    else:
                        print("Virheellinen syöte, yritä uudelleen.")

                if kysymys_obj.tarkista_vastaus(vastaus):
                    print("Vastaus oikein!")
                    oikeat_vastaukset += 1
                else:
                    print("Vastaus väärin.")

            if oikeat_vastaukset > 0:
                self.pelaaja.lisää_tähdet(oikeat_vastaukset)
                self.pelaaja.lisää_vieraillut_maa(kohdemaa)
                self.tallenna_tilanne(oikeat_vastaukset, kohdemaa)

                # Laskee CO2 päästöt
                emissions = self.co2_manager.update_emissions(self.pelaaja.nykyinen_maa, kohdemaa)
                print(f"CO2 päästöt matkasta: {emissions:.2f}g")

                # Meneekö yli?
                if self.co2_manager.get_total_emissions() > self.co2_manager.CO2_THRESHOLD:
                    print("CO2 päästöt ylittävät sallitun rajan!")
                    print(f"Yhteensä CO2 päästöjä: {self.co2_manager.get_total_emissions():.2f}g")

                    # Haluaako käyttää tähtiä
                    if self.co2_manager.can_afford_emissions(self.pelaaja.tähdet):
                        print("Sinulla on tarpeeksi tähtiä matkustuksen maksamiseen.")
                        vastaus = input(
                            f"Haluatko käyttää tähtiäsi päästöjen maksamiseen? Sinulla on {self.pelaaja.tähdet} tähteä. (Kyllä/Ei): ").strip().lower()

                        if vastaus == 'kyllä':
                            stars_used = int(input(
                                f"Kuinka monta tähteä käytät maksamiseen (sinulla on {self.pelaaja.tähdet} tähteä)? "))

                            emissions_to_pay = self.co2_manager.calculate_emissions_cost(stars_used)
                            if emissions_to_pay <= 0:
                                print("Tähtiä käytetty onnistuneesti! Voit jatkaa peliä.")
                                self.pelaaja.vähennä_tähdet(stars_used)
                            else:
                                print("Sinulla ei ole tarpeeksi tähtiä, et voi jatkaa peliä. Peli alkaa alusta.")
                                self.alusta_peli()
                        else:
                            print("Et halunnut käyttää tähtiä päästöjen maksamiseen. Peli päättyy!")
                            self.alusta_peli()
                    else:
                        print("Et voi maksaa päästöjäsi tähtiäsi käyttäen. Peli päättyy!")
                        self.alusta_peli()

            else:
                print("\nEt vastannut yhteenkään kysymykseen oikein. Kone palaa lähtömaahan.")

    def tallenna_tilanne(self, oikeat_vastaukset, kohdemaa):
        update_query = "UPDATE player_state SET tähdet = tähdet + %s"
        self.cursor.execute(update_query, (oikeat_vastaukset,))
        self.yhteys.commit()

        update_query = "UPDATE player_state SET nykyinen_maa = %s"
        self.cursor.execute(update_query, (kohdemaa,))
        self.yhteys.commit()

        self.cursor.execute("SELECT vieraillut_maat FROM player_state")
        result = self.cursor.fetchone()

        if result:
            vieraillut_maat = json.loads(result[0])
        else:
            vieraillut_maat = []

        if kohdemaa not in vieraillut_maat:
            vieraillut_maat.append(kohdemaa)
            update_query = "UPDATE player_state SET vieraillut_maat = %s"
            self.cursor.execute(update_query, (json.dumps(vieraillut_maat),))
            self.yhteys.commit()

    def pelaaja_loppu(self):
        print("\nOnneksi olkoon! Olet vieraillut kaikissa maissa ja suorittanut pelin loppuun!")
        self.cursor.execute("SELECT tähdet FROM player_state")
        tulos = self.cursor.fetchone()
        kokonaistähdet = tulos[0] if tulos else 0
        print(f'Kokonaispistemääräsi: {kokonaistähdet} tähteä!')
        print(f"Yhteensä CO2 päästöjä: {self.co2_manager.get_total_emissions():.2f}g")
        self.cursor.close()
        self.yhteys.close()
        exit()


try:
        yhteys = mysql.connector.connect(
            host='localhost',
            database='lentopeli',
            user='user',
            password='password',
            autocommit=True,
            collation='utf8mb4_unicode_ci'
        )

        pelaaja = Pelaaja("Player1")
        peli = Peli(pelaaja, yhteys)
        peli.aloita()

    except mysql.connector.Error as err:
        print(f"Virhe tietokantaoperaatiossa: {err}")
    except Exception as e:
        print(f'Virhe pelin aikana: {e}')

