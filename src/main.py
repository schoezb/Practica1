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
def accessTopMostPopularAninme(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    menuAnime = soup.find_all(text="Top Anime", href=True)
    topAnimeUrl = menuAnime[0]['href']
    print(topAnimeUrl)
    pageTopAnime = requests.get(topAnimeUrl)
    soupTopAnime = BeautifulSoup(pageTopAnime.content, 'html.parser')
    print(soupTopAnime.contents)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    accessTopMostPopularAninme("https://myanimelist.net/")
