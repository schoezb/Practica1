# Imports
# ---------------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests


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
