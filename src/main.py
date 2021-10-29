# ----------------------------------------------------------------------------
# Authors: Daniel Panadero i Stefany Chóez
# version ='1.0'
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from bs4 import BeautifulSoup
import requests


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------
def getmostpopularaninme(url: str):
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
    # Extraiem el contigut de la URL de Most Popular Anime
    pageMostPopular = requests.get(root + mostPopularUrl)
    # Organitzem el  contingut de la pàgina web
    soupMostPopular = BeautifulSoup(pageMostPopular.content, 'html.parser')

    # Retornem el contigut amb el qual generarem el dataset
    return soupMostPopular.contents


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    getmostpopularaninme("https://myanimelist.net/")
