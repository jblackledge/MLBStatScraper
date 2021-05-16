import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

#urls to parse, use request with "User-Agent" header to prevent MLB from blocking bot
urlOPS = "https://www.mlb.com/stats/national-league"
request = Request(urlOPS, headers={"User-Agent": "XYZ/3.0"})

#download webpage, read contents, and close reader
downloadedOPSPage = urlopen(request)
opsPageHtml = downloadedOPSPage.read()
downloadedOPSPage.close()

#create Beautiful Soup object to parse html page contents
opsSoup = soup(opsPageHtml, "html.parser")

print(opsSoup.h1)
