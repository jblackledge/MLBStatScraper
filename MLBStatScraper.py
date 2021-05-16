import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen


def getOPSLeaders(league, statType, year):
	statDictionary = {"ops" : "17", "avg" : "14", "hr" : "8", "rbi" : "9"}
	#urls to parse, use request with "User-Agent" header to prevent MLB from blocking bot
	if statType == "ops":
		url = "https://www.mlb.com/stats/" + league + "-league/" + year
	elif statType == "rbi":
		url = "https://www.mlb.com/stats/" + league + "-league"
	request = Request(url, headers={"User-Agent": "XYZ/3.0"})

	#download webpage, read contents, and close reader
	downloadedOPSPage = urlopen(request)
	opsPageHtml = downloadedOPSPage.read()
	downloadedOPSPage.close()

	#create Beautiful Soup object to parse html page contents
	opsSoup = soup(opsPageHtml, "html.parser")

	#find place in HTML containing player names in the table (ordered based on selected attribute)
	playerNames = opsSoup.find_all("span", {"class": "full-3fV3c9pF"})

	#find column specific stat
	stats = opsSoup.select("td[data-col=\"" + statDictionary[statType]  + "\"]")


	#loop through list of player name by 2, and parse the html to retrieve a str object for first and last name
	rank = 1;
	statIndex = 0; #needed to access stat line
	nameStartingIndex = 28
	nameEndingIndex = -7
	statEndingIndex = -5

	for i in range(0, len(playerNames), 2):
		#get first and last name of current player as string
		firstNameLine = str(playerNames[i])
		lastNameLine = str(playerNames[i + 1])

		#parse string, leaving only the name
		firstName = str(firstNameLine[nameStartingIndex : nameEndingIndex])
		lastName = str(lastNameLine[nameStartingIndex : nameEndingIndex])


		#get the desired stat
		desiredStatLine = str(stats[statIndex])
		if statType == "ops":
			statStartingIndex = 205
			#increment the statStartingIndex if the character at that pos is not a number or a decimal
			while (desiredStatLine[statStartingIndex] != '.') and (not desiredStatLine[statStartingIndex].isdigit()):
				statStartingIndex += 1
		elif statType == "rbi":
			statStartingIndex = 185
			while not desiredStatLine[statStartingIndex].isdigit():
				statStartingIndex += 1
		elif statType == "hr":
			statStartingIndex = 180
		elif statType == "avg":
			statStartingIndex = 180
		else:
			print("Stat not supported")
			break


		if statType == "ops":
			stat = float(desiredStatLine[statStartingIndex : statEndingIndex])
			print("%d,%s %s,%.3f" % (rank, firstName, lastName, stat))
		elif statType == "rbi":
			stat = int(desiredStatLine[statStartingIndex : -5])
			print("%d,%s %s,%d" % (rank, firstName, lastName, stat))

		rank += 1
		statIndex += 1



def getRBILeaders(league, statType):
	statDictionary = {"ops" : "17", "avg" : "14", "hr" : "8", "rbi" : "9"}
	#urls to parse, use request with "User-Agent" header to prevent MLB from blocking bot
	urlOPS = "https://www.mlb.com/stats/" + league + "-league"
	request = Request(urlOPS, headers={"User-Agent": "XYZ/3.0"})

	#download webpage, read contents, and close reader
	downloadedOPSPage = urlopen(request)
	opsPageHtml = downloadedOPSPage.read()
	downloadedOPSPage.close()

	#create Beautiful Soup object to parse html page contents
	opsSoup = soup(opsPageHtml, "html.parser")

	#find place in HTML containing player names in the table (ordered based on selected attribute)
	playerNames = opsSoup.find_all("span", {"class": "full-3fV3c9pF"})

	statIndex = 0
	#find column specific stat
	stats = opsSoup.select("td[data-col=\"" + statDictionary[statType]  + "\"]")
	for i in range(0, len(playerNames), 2):
		statLine = str(stats[statIndex])
		startingStatIndex = 185
		while not statLine[startingStatIndex].isdigit():
			startingStatIndex += 1
		rbis = int(statLine[startingStatIndex : -5])
		print(rbis)
		statIndex += 1


#getRBILeaders("national", "rbi")
getOPSLeaders("national", "ops", "1922")

