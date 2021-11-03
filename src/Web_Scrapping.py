# Imports
# ---------------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests
from time import strptime


class Web_Scrapping:
    # ---------------------------------------------------------------------------
    # Functions
    # ---------------------------------------------------------------------------
    def getmostpopularaninme(self, url: str):
        # Retorna el contingut de la pàgina web
        page = requests.get(url)
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
        root = topAnimeUrl.split("?")[0]
        # Generem la url dels animes més populars
        link = root + mostPopularUrl
        return link

    def getanimeslinks(self, link):
        # Utlitzem un for per agafar la informació de 2000 animes
        for i in range(0, 2000, 50):
            # Creem la url utilitzant la variable link i el contador "i"
            url = link + "&limit=" + str(i)
            #Utilitzem request i beatifulsoup per acaonseguir la informació
            request = requests.get(url)
            soup = BeautifulSoup(request.content, 'html.parser')
            animes = soup.findAll('a', {"class": "hoverinfo_trigger fl-l ml12 mr8"})
            #Creem una llista per guardar els enllaços
            animelinks = []
            #Recorrem tots els animes de la pagina actual i guardem el enllaç a la llista
            for anime in animes:
                href = anime['href']
                animelinks.append(href)
        return animelinks



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

        # Busquem el numbre de pupolaritat
        spanpopularity = soup.find_all("span", {"class": "numbers popularity"})
        popularity = (spanpopularity[0].next_element.next_element.next_element).split("#")[1]

        # Busquem el nombre de membres
        spanmembers = soup.find_all("span", {"class": "numbers members"})
        members = spanmembers[0].next_element.next_element.next_element

        # Busquem el tipus d'anime
        div = soup.find_all("div", {"class": "spaceit_pad"})
        divaux = div[3:]
        type = (divaux[0].text).split("Type:")[1].strip()

        # Busquem el nombre de episodis
        episodes = (divaux[1].text).split("Episodes:")[1].strip()

        # Busquem la llicencia
        licensorsaux = ((divaux[7].text).split("Licensors:")[1]).split(",")
        licensorslist = [x.strip() for x in licensorsaux]
        licensors = ""
        for i in licensorslist:
            if i != licensorslist[len(licensorslist) - 1]:
                licensors += i + ","
            else:
                licensors += i

        # Busquem les fechas de inici i final d'emissió
        years = (divaux[3].text).split("Aired:")[1]
        yearslist = years.split("to")
        yearsliststrip = [x.strip() for x in yearslist]
        day1 = ""
        if yearsliststrip[0][5] == ",":
            day1 = yearsliststrip[0][4]
        else:
            day1 = yearsliststrip[0][4] + yearsliststrip[0][5]
        month1 = strptime(yearsliststrip[0][0:3], '%b').tm_mon
        year1 = (yearsliststrip[0].split(",")[1]).strip()
        firstyear = year1 + "-" + str(month1) + "-" + day1

        lastyear = ""
        if yearsliststrip[1] != "?":
            day2 = ""
            if yearsliststrip[1][5] == ",":
                day2 = yearsliststrip[1][4]
            else:
                day2 = yearsliststrip[1][4] + yearsliststrip[1][5]

            month2 = strptime(yearsliststrip[1][0:3], '%b').tm_mon
            year2 = (yearsliststrip[1].split(",")[1]).strip()
            lastyear = year2 + "-" + str(month2) + "-" + day2
        else:
            lastyear = "currently aired"

        # Busquem el nombre del estudio
        studios = (divaux[8].text).split("Studios:")[1].strip()

        # Busquem el genere
        spangenres = (divaux[10].text).split("Genres:\n")[1:]
        genreslist = spangenres[0].split(",")
        genres = ""
        # Funció per obtenir els generes de l'anime
        for i in genreslist:
            aux = i.strip()
            firstletter = aux[0][0]
            genresaux = aux.split(firstletter)
            text = firstletter + genresaux[1]
            if i != genreslist[len(genreslist) - 1]:
                genres += text + ","
            else:
                genres += text

        # Busquem el tipus demografic
        spandemographic = (divaux[12].text).split("Demographic:\n")[1:]
        demographiclist = spandemographic[0].strip()
        firstletter = demographiclist[0][0]
        demographicaux = demographiclist.split(firstletter)
        demographic = firstletter + demographicaux[1]

        # Busquem la clasificació
        spanrating = (divaux[14].text).split("Rating:\n")[1:]
        ratinglist = spanrating[0].strip()
        rating = ((ratinglist.split("-")[1]).split("+")[0]).strip()

        # Guardem tota la informació a una llista
        result = [name, score, popularity, members, type, episodes, licensors, firstyear, lastyear, studios, genres,
                  demographic, rating]

        return result