import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen


urlOPS = "https://www.mlb.com/stats/national-league"
request = Request(urlOPS, headers={"User-Agent": "XYZ/3.0"})
downloadedOPSPage = urlopen(request)

opsPageHtml = downloadedOPSPage.read()
downloadedOPSPage.close()
opsSoup = soup(opsPageHtml, "html.parser")

print(opsSoup.h1)
