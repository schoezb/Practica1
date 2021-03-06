# Imports
# ---------------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
import time


class Web_Scrapping:

    def __init__(self, numero):
        self.root = "https://myanimelist.net/"
        self.numero = numero
        self.topurl = ""
        self.animelinks = []
        self.anime = []

    # ---------------------------------------------------------------------------
    # Functions
    # ---------------------------------------------------------------------------
    def getmostpopularanime(self):
        # Retorna el contingut de la pàgina web
        page = requests.get(self.root)
        # Organitzem el  contingut de la pàgina web
        soup = BeautifulSoup(page.content, 'html.parser')
        # Busquem la secció de Top Anime
        menuAnime = soup.find_all(text="Top Anime", href=True)
        # Extraiem la URL
        topAnimeUrl = menuAnime[0]['href']
        # Extraiem el contigut de la nova URL
        pageTopAnime = requests.get(topAnimeUrl)
        # Organitzem el  contingut de Top Anime
        soupTopAnime = BeautifulSoup(pageTopAnime.content, 'html.parser')
        # Busquem la secció de Most Popular
        mostPopular = soupTopAnime.find_all(text="Most Popular", href=True)
        # Extraiem la URL
        mostPopularUrl = mostPopular[0]['href']
        # Extraiem la URL de la pàgina Top Anime
        roottop = topAnimeUrl.split("?")[0]
        # Generem la url dels animes més populars
        self.topurl = roottop + mostPopularUrl

    def getanimeslinks(self):
        # Utlitzem un for per agafar la informació de 2000 animes
        for i in range(0, self.numero, 50):
            # Creem la url utilitzant la variable link i el contador "i"
            url = self.topurl + "&limit=" + str(i)
            # Utilitzem request i beatifulsoup per aconseguir la informació
            request = requests.get(url)
            soup = BeautifulSoup(request.content, 'html.parser')
            animes = soup.findAll('a', {"class": "hoverinfo_trigger fl-l ml12 mr8"})
            # Recorrem tots els animes de la pagina actual i guardem el enllaç a la llista
            for anime in animes:
                href = anime['href']
                self.animelinks.append(href)

    def getdata(self, url: str):
        # Retorna el contingut de la pàgina web
        page = requests.get(url)
        # Organitzem el  contingut de la pàgina web
        soup = BeautifulSoup(page.content, 'html.parser')

        # Variable que retornarem amb les dades obtingudes
        result = []

        # Busquem el nom del anime
        divname = soup.find_all("h1", {"class": "title-name h1_bold_none"})
        name = divname[0].next_element.next_element

        # Busquem el Score
        divscore = soup.find_all("div", {"class": "fl-l score"})
        score = divscore[0].next_element.next_element

        # Busquem el nombre de popularitat
        spanpopularity = soup.find_all("span", {"class": "numbers popularity"})
        popularity = (spanpopularity[0].next_element.next_element.next_element).split("#")[1]

        # Busquem el nombre de membres
        spanmembers = soup.find_all("span", {"class": "numbers members"})
        members = spanmembers[0].next_element.next_element.next_element

        # Variables globals
        type = ""
        episodes = ""
        licensors = ""
        studios = ""
        demographic = ""
        rating = ""
        genres = ""
        divaux = soup.find_all("div", {"class": "spaceit_pad"})
        for i in range(0, len(divaux)):

            if "Type" in (divaux[i].next_element.next_element).text:
                # Busquem el tipus d'anime
                type = (divaux[i].text).split("Type:")[1].strip()
            elif "Episodes" in (divaux[i].next_element.next_element).text:
                # Busquem el nombre de episodis
                episodes = (divaux[i].text).split("Episodes:")[1].strip()
            elif "Licensors" in (divaux[i].next_element.next_element).text:
                # Busquem la llicencia
                licensorsaux = ((divaux[i].text).split("Licensors:")[1]).split(",")
                if licensorsaux[0].strip() != "None found":
                    licensorslist = [x.strip() for x in licensorsaux]
                    for j in licensorslist:
                        if j != licensorslist[len(licensorslist) - 1]:
                            licensors += j + ","
                        else:
                            licensors += j
                else:
                    licensors = "None found"

            elif "Studios" in divaux[i].next_element.next_element.text:
                # Busquem el nombre del estudio
                studiosaux = (divaux[i].text).split("Studios:")[1].strip()
                studios = (divaux[i].text).split("Studios:")[1].strip()
                if studios == "None found, add some":
                    studiosaux = (divaux[i].text).split("Studios:")[1].strip()
                    studios = (studiosaux.split(",")[0]).strip()

            elif "Genres" in divaux[i].next_element.next_element.text:
                # Busquem el genere
                spangenres = (divaux[i].text).split("Genres:\n")[1:]
                genreslist = spangenres[0].split(",")
                genres = ""
                # Funció per obtenir els generes de l'anime
                for j in genreslist:
                    aux = j.strip()
                    firstletter = aux[0][0]
                    genresaux = aux.split(firstletter)
                    text = firstletter + genresaux[1]
                    if j != genreslist[len(genreslist) - 1]:
                        genres += text + ","
                    else:
                        genres += text
            elif "Demographic" in (divaux[i].next_element.next_element).text:
                # Busquem el tipus demografic i rating, comprovem que la demografica existeix
                if "Demographics:" in (divaux[i].next_element.next_element).text:
                    spandemographic = (divaux[i].text).split("Demographics:\n")[1:]
                    demographiclist = spandemographic[0].split(",")
                    # Funció per obtenir les demografies de l'anime
                    for j in demographiclist:
                        aux = j.strip()
                        firstletter = aux[0][0]
                        demographicaux = aux.split(firstletter)
                        text = firstletter + demographicaux[1]
                        if j != demographiclist[len(demographiclist) - 1]:
                            demographic += text + ","
                        else:
                            demographic += text
                else:
                    spandemographic = (divaux[i].text).split("Demographic:\n")[1:]
                    demographiclist = spandemographic[0].split(",")
                    # Funció per obtenir les demografies de l'anime
                    for j in demographiclist:
                        aux = j.strip()
                        firstletter = aux[0][0]
                        demographicaux = aux.split(firstletter)
                        text = firstletter + demographicaux[1]
                        if j != demographiclist[len(demographiclist) - 1]:
                            demographic += text + ","
                        else:
                            demographic += text

            elif "Rating" in (divaux[i].next_element.next_element).text:
                # Busquem la clasificació
                spanrating = (divaux[i].text).split("Rating:\n")[1:]
                ratinglist = spanrating[0].strip()
                rating = ''.join([str(elem) for elem in ratinglist])

        # Guardem tota la informació a una llista
        result = [name, score, popularity, members, type, episodes, licensors, studios, genres,
                  demographic, rating]

        return result

    def scrapper(self):
        # Recorrem la llista de links amb un for
        for i in self.animelinks:
            # Utilitzem la llibreria time per aplicar un delay, per evitar que la pagina ems bloquegi l'acces
            t0 = time.time()
            # Afegim la informació del anime a la variable "anime"
            self.anime.append(self.getdata(i))
            response_delay = time.time() - t0
            time.sleep(2 * response_delay)

    def csv(self, filename):
        # Creem el csv amb el nom que li hem passat
        # Si ja existeix, es sobrescriu
        csv = open("../csv/" + filename, "w+", encoding="utf-8")

        # Copiem la informacio dels animes al csv
        for i in range(len(self.anime)):
            for j in range(len(self.anime[i])):
                csv.write(self.anime[i][j] + ";")
            csv.write("\n")
