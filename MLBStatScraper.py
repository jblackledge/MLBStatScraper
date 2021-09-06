import urllib.request
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import datetime
from timeit import default_timer as timer
import sys


def getLeaders(league, statType, year):
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

	#loop through list of player name by 2, and parse the html to retrieve a str object for first and last name
	statIndex = 0; #needed to access stat line
	nameStartingIndex = 28
	nameEndingIndex = -7

	#create an empty csv file to write our stats to
	datestamp = generateDatestamp()
	csvFilenameString = "MLBStatScraper_" + datestamp + '_' + league + '_' + statType + '_' + year + ".csv"
	csvFile = open(csvFilenameString, 'w')

	csvHeader = "player name,ops,avg,rbi,hr" + '\n'
	csvFile.write(csvHeader)

	#loop through the list of players and create a csv line including rank, name, and stats
	for i in range(0, len(playerNames), 2):

		#get first and last name of current player as string
		firstNameLine = str(playerNames[i])
		lastNameLine = str(playerNames[i + 1])

		#parse string, leaving only the name and add to the csv line
		firstName = str(firstNameLine[nameStartingIndex : nameEndingIndex])
		lastName = str(lastNameLine[nameStartingIndex : nameEndingIndex])
		playerName = firstName + ' ' + lastName
		csvLine = playerName + ','

		#add the stats to the csv line for the given stat index
		csvLine = csvLine + getStatsForIndex(statIndex, baseballSoup)

		statIndex += 1
		csvFile.write(csvLine)


def getStatsForIndex(statIndex, baseballSoup):
	statColumnDict = {"ops" : "17", "avg" : "14", "rbi" : "9", "hr" : "8"}
	csvLine = str()

	for statType in statColumnDict:
		#parse the html using the appropriate stat column number from the dictionary
		stats = baseballSoup.select("td[data-col=\"" + statColumnDict[statType] + "\"]")

		#get the desired stat
		statLine = str(stats[statIndex])

		#get the indeces of where the stat starts and begins in the html
		statIndecesTuple = calculateStatIndeces(statLine)
		statEndingIndex = statIndecesTuple[0]
		statStartingIndex = statIndecesTuple[1]

		if statType == "ops" or statType == "avg":
			stat = float(statLine[statStartingIndex : statEndingIndex])
			statString = "{statistic:.3f}"
			csvLine = csvLine + statString.format(statistic = stat)
		else:
			stat = int(statLine[statStartingIndex : statEndingIndex])
			statString = str(stat)
			csvLine = csvLine + statString

		#leave comma off of the last stat
		if statType != "hr":
			csvLine = csvLine + ','
		else:
			csvLine = csvLine + '\n'

	return csvLine


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


def createMVPDict():
	leagueTuple = ("AL", "NL")
	americanMVPDict = dict()
	nationalMVPDict = dict()

	for league in leagueTuple:
		#use request with "User-Agent" header to prevent MLB from blocking bot
		url = "http://m.mlb.com/awards/history-winners/?award_id=" + league + "MVP"
		request = Request(url, headers={"User-Agent": "XYZ/3.0"})

		#download webpage, read contents, and close reader
		downloadedPage = urlopen(request)
		pageHTML = downloadedPage.read()
		downloadedPage.close()

		#create Beautiful Soup object to parse html page contents
		mvpSoup = soup(pageHTML, "html.parser")

		#find place in HTML containing player names
		mvpList = mvpSoup.find_all("td")

		for i in range(0, len(mvpList), 4):
			year = str(mvpList[i])
			year = year[4 : 8]

			playerName = str(mvpList[i + 1])
			playerName = playerName[29 : len(playerName) - 9]

			position = str(mvpList[i + 3])
			position = position[4 : len(position) - 5]

			#filter out pitchers since we only are comparing hitting stats
			if position != "SP":
				if league == "NL":
					nationalMVPDict[year] = playerName
				else:
					americanMVPDict[year] = playerName

	return (americanMVPDict, nationalMVPDict)


def generateMVPData(isBinary, isBinaryFL):
	#create an empty csv file to write our stats to
	datestamp = generateDatestamp()

	if isBinary:
		csvFilenameString = "MLBStatScraperMVP_" + datestamp + "_binary" + ".csv"
	elif isBinaryFL:
		csvFilenameString = "MLBStatScraperMVP_" + datestamp + "_binaryFL"  + ".csv"
	else:
		csvFilenameString = "MLBStatScraperMVP_" + datestamp + "_string"  + ".csv"
	csvFile = open(csvFilenameString, 'w')

	csvHeader = "player name,mvp,ops,avg,rbi,hr" + '\n'
	csvFile.write(csvHeader)

	#create the mvp dictionaries to iterate through
	mvpDicts = createMVPDict()
	americanMVPDict = mvpDicts[0]
	nationalMVPDict = mvpDicts[1]
	mvpDict = dict()
	leagueTuple = ("american", "national")

	for league in leagueTuple:
		#set mvpdict to correct league and iterate through the year keys in that dict
		if league == "national":
			mvpDict = nationalMVPDict
		else:
			mvpDict = americanMVPDict

		for year in mvpDict.keys():
			#use request with "User-Agent" header to prevent MLB from blocking bot
			url = getURL(league, "ops", year)
			request = Request(url, headers={"User-Agent": "XYZ/3.0"})

			#download webpage, read contents, and close reader
			downloadedPage = urlopen(request)
			pageHtml = downloadedPage.read()
			downloadedPage.close()

			#create Beautiful Soup object to parse html page contents
			baseballSoup = soup(pageHtml, "html.parser")

			#find place in HTML containing player names, and stats in the table (ordered based on statType)
			playerNames = baseballSoup.find_all("span", {"class": "full-3fV3c9pF"})

			#loop through list of player name by 2, and parse the html to retrieve a str object for first and last name
			statIndex = 0; #needed to access stat line
			nameStartingIndex = 28
			nameEndingIndex = -7

			#loop through the list of players and create a csv line including rank, name, and stats
			for i in range(0, len(playerNames), 2):
				#get first and last name of current player as string
				firstNameLine = str(playerNames[i])
				lastNameLine = str(playerNames[i + 1])

				#parse string, leaving only the name and add to the csv line
				firstName = str(firstNameLine[nameStartingIndex : nameEndingIndex])
				lastName = str(lastNameLine[nameStartingIndex : nameEndingIndex])
				playerName = firstName + ' ' + lastName
				csvLine = playerName + ','

				#check if player is the mvp of that year, in that league, and set mvp status accordingly
				if playerName != mvpDict[year]:
					#determine if the user needs binary values of 1 or 0, if not we use yes/no
					if isBinary:
						csvLine = csvLine + '0' + ','
					elif isBinaryFL:
						csvLine = csvLine + "0.0" + ','
					else:
						csvLine = csvLine + "Not MVP" + ','
				else:
					#determine if the user needs binary values of 1 or 0, if not we use yes/no
					if isBinary:
						csvLine = csvLine + '1' + ','
					elif isBinaryFL:
						csvLine = csvLine + "1.0" + ','
					else:
						csvLine = csvLine + "MVP" + ','

				#add the stats to the csv line for the given stat index
				csvLine = csvLine + getStatsForIndex(statIndex, baseballSoup)

				statIndex += 1
				if playerName == mvpDict[year]:
					print(year + ' ' + league + ' ' + csvLine)
				csvFile.write(csvLine)


def generateDatestamp():
	now = datetime.datetime.now()
	currentYear = now.year
	currentYearString = str(currentYear)

	currentMonth = now.month
	currentMonthString = str(("%02d" % currentMonth))

	currentDate = now.day
	currentDateString = str(("%02d" % currentDate))

	datestampString = currentYearString + currentMonthString + currentDateString
	return datestampString


def isValidLeague(league):
	return (league == "national") or (league == "american") or (league == "mlb")


def isValidStatType(statType):
	return (statType == "ops") or (statType == "avg") or (statType == "rbi") or (statType == "hr")


def isValidYear(year):
	now = datetime.datetime.now()
	currentYear = now.year
	oldestStatYear = 1903

	return (year >= oldestStatYear) and (year <= currentYear)


def isValidYearOrder(beginningYear, endingYear):
	return endingYear >= beginningYear


def getURL(league, statType, year):
	statTypeDict = {"ops" : "", "avg" : "batting-average", "hr" : "home-runs", "rbi" : "rbi"}
	now = datetime.datetime.now()
	currentYear = int(now.year)

	if year == currentYear:
		url = "https://www.mlb.com/stats/" + league + "-league/" + statTypeDict[statType]
	else:
		url = "https://www.mlb.com/stats/" + league + "-league/" + statTypeDict[statType] + "/" + year

	return url


def runAllCustomYearSpan(beginningYear, endingYear):
	leagues = ["national", "american", "mlb"]
	statTypes = ["ops", "avg", "hr", "rbi"]

	for league in leagues:
		for statType in statTypes:
			for year in range(beginningYear, endingYear + 1):
				try:
					getLeaders(league, statType, str(year))
					print("Success: %s, %s, %s" % (league, statType, str(year)))
				except Exception as e:
					print(str(e) + ": " + league + ", " + statType + ", " + str(year))


def testAll():
	leagues = ["national", "american", "mlb"]
	statTypes = ["ops", "avg", "hr", "rbi"]
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for league in leagues:
		for statType in statTypes:
			for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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

	for year in range(oldestStatYear, currentYear + 1):
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




def testMLBOPS():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear + 1):
		try:
			getLeaders("mlb", "ops", str(year))
			print("Success: mlb, ops, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": mlb, ops, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testMLBAVG():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear + 1):
		try:
			getLeaders("mlb", "avg", str(year))
			print("Success: mlb, avg, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": mlb, avg, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testMLBHR():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear + 1):
		try:
			getLeaders("mlb", "hr", str(year))
			print("Success: mlb, hr, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": mlb, hr, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


def testMLBRBI():
	start = timer()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	oldestStatYear = 1903

	for year in range(oldestStatYear, currentYear + 1):
		try:
			getLeaders("mlb", "rbi", str(year))
			print("Success: mlb, rbi, %s" % (str(year)))
		except Exception as e:
			print(str(e) + ": mlb, rbi, %s" % (str(year)))

	end = timer()
	if end - start >= 60:
		minutes = (end - start) / 60
		print("Elapsed time: %s" % str(minutes))
	else:
		print(end - start)


#main
league = str()
statType = str()
year = str()

now = datetime.datetime.now()
currentYearString = str(now.year)

#if there is only one argument, the user is just performing a simple demo of the script
if len(sys.argv) == 1:
	getLeaders("mlb", "ops", currentYearString)
#if there are two arguments, the user is either running script for all possible combinations of league, 
#stat-type, and year, OR they are generating an mvp csv file, so we must check which one they typed
elif len(sys.argv) == 2:
	if sys.argv[1] == "all":
		testAll()
	elif sys.argv[1] == "mvp":
		generateMVPData(False)
	else:
		print("Error: invalid input")
#if there are three arguments, the user is inputting a custom year span to run all leagues and stat types OR
#is gnerating mvp data in with a binary(1/0) or binary float(1.0/0.0) mvp columnt
elif len(sys.argv) == 3:
	if sys.argv[1] == "mvp" and sys.argv[2] == "binary":
		generateMVPData(True, False)
	elif sys.argv[1] == "mvp" and sys.argv[2] == "binaryfl":
		generateMVPData(False, True)
	elif isValidYear(int(sys.argv[1])) and isValidYear(int(sys.argv[2])) and isValidYearOrder(int(sys.argv[1]), int(sys.argv[2])):
		runAllCustomYearSpan(int(sys.argv[1]), int(sys.argv[2]))
	else:
		print("Error: invalid input")
#if there are four arguments, the user has input a league, stat type and year, so we must check that they
#are valid before running the script
elif len(sys.argv) == 4:
	if isValidLeague(sys.argv[1]) and isValidStatType(sys.argv[2]) and isValidYear(int(sys.argv[3])):
		league = sys.argv[1]
		statType = sys.argv[2]
		year = sys.argv[3]
		getLeaders(league, statType, year)
	else:
		print("Error: invalid input")
else:
	print("Error: invalid number of arguments")
