import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup


def scrapeGameStats(team, date):
	url = createURLString(team, date)
	pageHTML = downloadWebpage(url)

	baseballSoup = soup(pageHTML, "html.parser")
	print(baseballSoup.h1)


def downloadWebpage(url):
	request = Request(url)
	downloadedPage = urlopen(request)
	pageHTML = downloadedPage.read()
	downloadedPage.close()

	return pageHTML


def createURLString(team, date):
	url = "https://www.baseball-reference.com/boxes/" + team + "/" + team + date + "0.shtml"
	return url


scrapeGameStats("BOS", "20210419")
