# ----------------------------------------------------------------------------
# Authors: Daniel Panadero i Stefany Chóez
# version ='1.0'
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
from Web_Scrapping import Web_Scrapping

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    Scrappy = Web_Scrapping(2000)
    Scrappy.getmostpopularaninme()
    Scrappy.getanimeslinks()
    Scrappy.scrapper()
    Scrappy.csv("dataset.csv")
    print(Scrappy.anime)
