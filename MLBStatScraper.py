import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import datetime


def getLeaders(league, statType, year):
	statColumnDict = {"ops" : "17", "avg" : "14", "rbi" : "9", "hr" : "8"}

	#use request with "User-Agent" header to prevent MLB from blocking bot
	url = getURL(league, statType, year)
	request = Request(url, headers={"User-Agent": "XYZ/3.0"})

	#download webpage, read contents, and close reader
	downloadedPage = urlopen(request)
	pageHtml = downloadedPage.read()
	downloadedPage.close()

	#create Beautiful Soup object to parse html page contents
	baseballSoup = soup(pageHtml, "html.parser")

	#find place in HTML containing player names, and stats in the table (ordered based on statType)
	playerNames = baseballSoup.find_all("span", {"class": "full-3fV3c9pF"})
	stats = baseballSoup.select("td[data-col=\"" + statColumnDict[statType] + "\"]")

	#loop through list of player name by 2, and parse the html to retrieve a str object for first and last name
	rank = 1;
	statIndex = 0; #needed to access stat line
	nameStartingIndex = 28
	nameEndingIndex = -7

	for i in range(0, len(playerNames), 2):
		#get first and last name of current player as string
		firstNameLine = str(playerNames[i])
		lastNameLine = str(playerNames[i + 1])

		#parse string, leaving only the name
		firstName = str(firstNameLine[nameStartingIndex : nameEndingIndex])
		lastName = str(lastNameLine[nameStartingIndex : nameEndingIndex])

		#get the desired stat
		statLine = str(stats[statIndex])

		statIndecesTuple = calculateStatIndeces(statLine)
		statEndingIndex = statIndecesTuple[0]
		statStartingIndex = statIndecesTuple[1]

		if statType != "ops" or statType != "avg":
			stat = int(statLine[statStartingIndex : statEndingIndex])
			print("%d,%s %s,%d" % (rank, firstName, lastName, stat))
		else:
			stat = float(statLine[statStartingIndex : statEndingIndex])
			print("%d,%s %s,%.3f" % (rank, firstName, lastName, stat))

		rank += 1
		statIndex += 1


def calculateStatIndeces(statLine):
	#loop through the stat line and decrement the ending index of the stat until we find a number
	statEndingIndex = len(statLine) - 1
	while not statLine[statEndingIndex - 1].isdigit():
		statEndingIndex -= 1

	#increment the statStartingIndex if the character at that pos is not a number or a decimal
	statStartingIndex = statEndingIndex - 1
	while statLine[statStartingIndex - 1] == '.' or statLine[statStartingIndex -1].isdigit():
		statStartingIndex -= 1

	return (statEndingIndex, statStartingIndex)


def getURL(league, statType, year):
	statTypeDict = {"ops" : "", "avg" : "batting-average", "hr" : "home-runs", "rbi" : "rbi"}

	now = datetime.datetime.now()
	currentYear = int(now.year)
	if year == currentYear:
		url = "https://www.mlb.com/stats/" + league + "-league/" + statTypeDict[statType]
	else:
		url = "https://www.mlb.com/stats/" + league + "-league/" + statTypeDict[statType] + "/" + year

	return url


getLeaders("american", "rbi", "2016")
