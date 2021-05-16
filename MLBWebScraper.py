import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

#urls to parse, use request with "User-Agent" header to prevent MLB from blocking bot
urlOPSNL = "https://www.mlb.com/stats/national-league"
request = Request(urlOPSNL, headers={"User-Agent": "XYZ/3.0"})

#download webpage, read contents, and close reader
downloadedOPSNLPage = urlopen(request)
opsnlPageHtml = downloadedOPSNLPage.read()
downloadedOPSNLPage.close()

#create Beautiful Soup object to parse html page contents
opsnlSoup = soup(opsnlPageHtml, "html.parser")

#find place in HTML containing player names in the table (ordered based on selected attribute)
playerNames = opsnlSoup.find_all("span", {"class": "full-3fV3c9pF"})

#loop through list of player name by 2, and parse the html to retrieve a str object for first and last name
rank = 1;
for i in range(0, len(playerNames), 2):
	#get first and last name of current player as string
	firstNameLine = str(playerNames[i])
	lastNameLine = str(playerNames[i + 1])

	#parse string, leaving only the name
	firstName = str(firstNameLine[28 : -7])
	lastName = str(lastNameLine[28 : -7])
	print("%d,%s %s" % (rank, firstName, lastName))
	print()
	rank += 1

