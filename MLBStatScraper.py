import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import datetime


def getLeadersDecimal(league, year):
	statDictionary = {"ops" : "17", "avg" : "14", "hr" : "8", "rbi" : "9"}
	#urls to parse, use request with "User-Agent" header to prevent MLB from blocking bot
	url = "https://www.mlb.com/stats/" + league + "-league/" + year
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
	stats = opsSoup.select("td[data-col=\"17\"]")


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

		statStartingIndex = 205
		#increment the statStartingIndex if the character at that pos is not a number or a decimal
		while (desiredStatLine[statStartingIndex] != '.') and (not desiredStatLine[statStartingIndex].isdigit()):
			statStartingIndex += 1

		stat = float(desiredStatLine[statStartingIndex : statEndingIndex])
		print("%d,%s %s,%.3f" % (rank, firstName, lastName, stat))

		rank += 1
		statIndex += 1


def getLeadersInteger(league, statType, year):
	statTypeDict = {"hr" : "home-runs", "rbi" : "rbi"}
	statColumnDict = {"hr" : "8", "rbi" : "9"}

	#urls to parse, use request with "User-Agent" header to prevent MLB from blocking bot
	now = datetime.datetime.now()
	currentYear = int(now.year)
	if year == currentYear:
		url = "https://www.mlb.com/stats/" + league + "-league/" + statTypeDict[statType]
		#url = "https://www.mlb.com/stats/" + league + "-league/rbi"
	else:
		url = "https://www.mlb.com/stats/" + league + "-league/" + statTypeDict[statType] + "/" + year
		#url = "https://www.mlb.com/stats/" + league + "-league/rbi/" + year
	request = Request(url, headers={"User-Agent": "XYZ/3.0"})

	#download webpage, read contents, and close reader
	downloadedOPSPage = urlopen(request)
	opsPageHtml = downloadedOPSPage.read()
	downloadedOPSPage.close()

	#create Beautiful Soup object to parse html page contents
	rbiSoup = soup(opsPageHtml, "html.parser")

	#find place in HTML containing player names in the table (ordered based on selected attribute)
	playerNames = rbiSoup.find_all("span", {"class": "full-3fV3c9pF"})

	#find column specific stat
	stats = rbiSoup.select("td[data-col=\"" + statColumnDict[statType] + "\"]")
	#stats = rbiSoup.select("td[data-col=\"9\"]")


	#loop through list of player name by 2, and parse the html to retrieve a str object for first and last name
	rank = 1;
	statIndex = 0; #needed to access stat line
	nameStartingIndex = 28
	nameEndingIndex = -7
	#statEndingIndex = -5

	for i in range(0, len(playerNames), 2):
		#get first and last name of current player as string
		firstNameLine = str(playerNames[i])
		lastNameLine = str(playerNames[i + 1])

		#parse string, leaving only the name
		firstName = str(firstNameLine[nameStartingIndex : nameEndingIndex])
		lastName = str(lastNameLine[nameStartingIndex : nameEndingIndex])

		#get the desired stat line
		desiredStatLine = str(stats[statIndex])
		statEndingIndex = len(desiredStatLine) - 1

		#loop through the stat line and decrement the ending index of the stat until we find a number
		while not desiredStatLine[statEndingIndex - 1].isdigit():
			statEndingIndex -= 1


		desiredStatLine = desiredStatLine[0 : statEndingIndex]
		statStartingIndex = len(desiredStatLine) - 1

		while desiredStatLine[statStartingIndex].isdigit() and desiredStatLine[statStartingIndex - 1].isdigit():
			statStartingIndex -= 1

		stat = int(desiredStatLine[statStartingIndex : ])
		#print(desiredStatLine[statStartingIndex : ])
		print("%d,%s %s,%d" % (rank, firstName, lastName, stat))

		rank += 1
		statIndex += 1


getLeadersInteger("american", "hr" ,"2016")
