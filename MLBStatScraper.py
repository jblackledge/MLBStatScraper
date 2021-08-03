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
	rank = 1;
	statIndex = 0; #needed to access stat line
	nameStartingIndex = 28
	nameEndingIndex = -7

	#create an empty csv file to write our stats to
	datestamp = generateDatestamp()
	csvFilenameString = "MLBStatScraper_" + datestamp + '_' + league + '_' + statType + '_' + year + ".csv"
	csvFile = open(csvFilenameString, 'w')

	#loop through the list of players and create a csv line including rank, name, and stats
	for i in range(0, len(playerNames), 2):
		csvLine = str(rank) + ','

		#get first and last name of current player as string
		firstNameLine = str(playerNames[i])
		lastNameLine = str(playerNames[i + 1])

		#parse string, leaving only the name and add to the csv line
		firstName = str(firstNameLine[nameStartingIndex : nameEndingIndex])
		lastName = str(lastNameLine[nameStartingIndex : nameEndingIndex])
		csvLine = csvLine + firstName + ' ' + lastName + ','

		#add the stats to the csv line for the given stat index
		csvLine = csvLine + getStatsForIndex(statIndex, baseballSoup)

		rank += 1
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


#testAll()
#testNationalOPS()
#testNationalAVG()
#testNationalHR()
#testNationalRBI()

#testAmericanOPS()
#testAmericanAVG()
#testAmericanHR()
#testAmericanRBI()

#testMLBOPS()
#testMLBAVG()
#testMLBHR()
#testMLBRBI()

league = str()
statType = str()
year = str()

now = datetime.datetime.now()
currentYearString = str(now.year)

#if there is only one argument, the user is just performing a simple demo of the script
if len(sys.argv) == 1:
	getLeaders("mlb", "ops", currentYearString)
#if there are two arguments, the user is running script for all possible combinations of league, stat type,
#and year, so we must check that they typed "all"
elif len(sys.argv) == 2:
	if sys.argv[1] == "all":
		testAll()
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



#getLeaders("national", "avg", currentYearString)
#getLeaders("national", "avg", currentYearString)
#getLeaders("national", "rbi", currentYearString)
#getLeaders("national", "hr", currentYearString)

#getLeaders("american", "ops", currentYearString)
#getLeaders("american", "avg", currentYearString)
#getLeaders("american", "rbi", currentYearString)
#getLeaders("american", "hr", currentYearString)

#getLeaders("mlb", "ops", currentYearString)
#getLeaders("mlb", "avg", currentYearString)
#getLeaders("mlb", "rbi", currentYearString)
#getLeaders("mlb", "hr", currentYearString)
