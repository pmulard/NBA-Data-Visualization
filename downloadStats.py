from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os

#---------- PROGRAM OVERVIEW ----------
	#This program runs a beautfulsoup to extract NBA player statistics from nbareference.com. The stats are
	#formatted into a pandas dataframe based on the year and the type of statistic. The five "save" functions
	#use the getStats function to create local CSV files for each type of statistic within the range of years
	#passed as paramaters. These are saved in folders created by the createFolder function within the directory
	#variable below.

	#Years available spans from 1973-present (with the exception of Per 100 Possessions, which starts in 1974).
	#Because the basketball season spans over two calendar years, the year used is the second of the two. i.e. 
	#the 2019-20 season will be 2020 for this program.	

	#The types of stats available are:
		#Totals (totals)
		#Per Game (per_game)
		#Per 36 Minutes (per_minute)
		#Per 100 Possessions (per_poss)
		#Advanced (advanced)

			#String in paranthesis is unique url ID on NBA Reference webpages.

#An example run of this program is: saveTotStats(1982, 1996)

#Directory where you would like the folders with CSV files to be stored
directory = r"C:\Users\PeterMulard\Desktop"
	
#Scrapes statistics from NBA Reference and saves it to a pandas dataframe
def getStats(yearInput, typeInput):

	#Defines the year and type of stat to be used at basketball reference
	year = int(yearInput)
	statsType = str(typeInput)

	#Defines the url used to retrieve the stats with the parameters passed into the getStats function
	url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(year, statsType)
	html = urlopen(url)

	#Creates a soup object from the url
	soup = BeautifulSoup(html, features = "lxml")

	#Finds the right header in the HTML on the web page to get the correct data table
	soup.findAll("tr", limit = 2)

	#Extracts text from headers into a list
	headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]

	#Excludes the first column that has arbitrary values ranking players alphabetically
	headers = headers[1:]

	#Extracts data from the table
	rows = soup.findAll("tr")[1:] #Gets rows while ignoring the first row that contains the header
	playerStats = [[td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))];

	#Create a pandas dataframe
	stats = pd.DataFrame(playerStats, columns = headers)

	#Removes empty columns that appear only in the advanced statistics
	if "advanced" in url:
		col = [18, 23]
		stats.drop(stats.columns[col], axis = 1, inplace = True)

	#Removes duplicate players (NBA Reference has seperate rows for each team an individual played for.
	#They also have a row for the total of all teams, which is what we want. This is always the first
	#entry). Note: Two players who share the same name, age and team (while unlikely), will result in
	#one of them being deleted.
	stats.drop_duplicates(subset = ["Player", "Age"], keep = "first", inplace  = True)

	#Removes blank rows by replacing them with np.nan so they can be removed from the data set
	stats["Player"].replace("", np.nan, inplace = True)
	stats.dropna(subset = ["Player"], inplace = True)

	#Replaces empty string values with zeros
	stats = stats.replace("", 0)

	#Converts numbers currently set as strings to numeric values
	stats = stats.apply(pd.to_numeric, errors = "ignore")

	return stats


#Saves TOTAL statistics CSV files within the range of years passed as arguments
def saveTotStats(lowYear, highYear):
	#Sets range of years
	low = lowYear
	high = highYear
	
	#Creates an array holding dataframes for each year in our range
	totStats = [getStats(x, "totals") for x in range(low, high + 1)]

	#Creates Folder in directory
	createFolder("Totals")

	#Exports CSV file of dataframe
	for i in range(low - low, (high + 1) - low):
		export_csv = totStats[i].to_csv(r"{}\Totals\tot{}.csv".format(directory, i + low), index = None, header=True)


#Saves PER GAME statistics CSV files within the range of years passed as arguments
def saveGameStats(lowYear, highYear):
	#Sets range of years
	low = lowYear
	high = highYear
	
	#Creates an array holding dataframes for each year in our range
	gameStats = [getStats(x, "per_game") for x in range(low, high + 1)]

	#Creates Folder in directory
	createFolder("PerGame")

	#Exports CSV file of dataframe
	for i in range(low - low, (high + 1) - low):
		export_csv = gameStats[i].to_csv(r"{}\PerGame\game{}.csv".format(directory, i + low), index = None, header=True)


#Saves PER 36 MINUTES statistics CSV files within the range of years passed as arguments
def save36minStats(lowYear, highYear):
	#Sets range of years
	low = lowYear
	high = highYear
	
	#Creates an array holding dataframes for each year in our range
	min36Stats = [getStats(x, "per_minute") for x in range(low, high + 1)]

	#Creates Folder in directory
	createFolder("Per36Min")

	#Exports CSV file of dataframe
	for i in range(low - low, (high + 1) - low):
		export_csv = min36Stats[i].to_csv(r"{}\Per36Min\36min{}.csv".format(directory, i + low), index = None, header=True)


#Saves PER 100 POSSESSIONS statistics CSV files within the range of years passed as arguments
def save100possStats(lowYear, highYear):
	#Sets range of years
	low = lowYear
	high = highYear
	
	#Creates an array holding dataframes for each year in our range
	poss100Stats = [getStats(x, "per_poss") for x in range(low, high + 1)]

	#Creates Folder in directory
	createFolder("Per100Poss")

	#Exports CSV file of dataframe
	for i in range(low - low, (high + 1) - low):
		export_csv = poss100Stats[i].to_csv(r"{}\Per100Poss\100poss{}.csv".format(directory, i + low), index = None, header=True)


#Saves ADVANCED statistics CSV files within the range of years passed as arguments
def saveAdvStats(lowYear, highYear):
	#Sets range of years
	low = lowYear
	high = highYear
	
	#Creates an array holding dataframes for each year in our range
	advStats = [getStats(x, "advanced") for x in range(low, high + 1)]

	#Creates Folder in directory
	createFolder("Advanced")

	#Exports CSV file of dataframe
	for i in range(low - low, (high + 1) - low):
		export_csv = advStats[i].to_csv(r"{}\Advanced\adv{}.csv".format(directory, i + low), index = None, header=True)


#Creates a new folder to store the CSV files
def createFolder(statsType):
	newpath = r"{}\{}".format(directory, statsType) 
	if not os.path.exists(newpath):
	    os.makedirs(newpath)