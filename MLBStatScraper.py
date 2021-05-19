import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import datetime
from timeit import default_timer as timer


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

		if statType == "ops" or statType == "avg":
			stat = float(statLine[statStartingIndex : statEndingIndex])
			#print("%d,%s %s,%d" % (rank, firstName, lastName, stat))
		else:
			stat = int(statLine[statStartingIndex : statEndingIndex])
			#print("%d,%s %s,%.3f" % (rank, firstName, lastName, stat))

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


def testAll():
	leagues = ["national", "american"]
	statTypes = ["ops", "avg", "hr", "rbi"]
	now = datetime.datetime.now()
	currentYear = int(now.year)

	for league in leagues:
		for statType in statTypes:
			for year in range(1903, currentYear):
				try:
					getLeaders(league, statType, str(year))
					print("Success: %s, %s, %s" % (league, statType, str(year)))
				except Exception as e:
					print(str(e) + ": " + league + ", " + statType + ", " + str(year))


def testNationalOPS():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("national", "ops", str(year))
			print("Success: national, ops, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": national, ops, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testNationalAVG():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("national", "avg", str(year))
			print("Success: national, avg, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": national, avg, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testNationalHR():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("national", "hr", str(year))
			print("Success: national, hr, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": national, hr, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testNationalRBI():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("national", "rbi", str(year))
			print("Success: national, rbi, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": national, rbi, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testAmericanOPS():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("american", "ops", str(year))
			print("Success: american, ops, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": american, ops, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testAmericanAVG():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("american", "avg", str(year))
			print("Success: american, avg, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": american, avg, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testAmericanHR():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("american", "hr", str(year))
			print("Success: american, hr, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": american, hr, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testAmericanRBI():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear):
		try:
			getLeaders("american", "rbi", str(year))
			print("Success: american, rbi, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": american, rbi, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


#testNationalOPS()
#testNationalAVG()
#testNationalHR()
#testNationalRBI()

#testAmericanOPS()
#testAmericanAVG()
#testAmericanHR()
#testAmericanRBI()
