# MLBStatScraper
This script scrapes and parses the MLB website to generate a csv file of the MLB leaders of a chosen league
and year. The csv file lists the rank, name, OPS, batting average, RBI's, 
and HR's for each player, sorted by the chosen stat type. The generated csv files are perfect for simple machine learning and data science 
projects.


## Installation
Simply download the code from this repo. This script works on all systems with a python 3 interpreter.

## Usage
Once downloaded, use the terminal to cd into the folder you downloaded it to. There type "make all" to run the
included demo that will create a csv file of all MLB leaders in the current year, sorted by OPS. You can also
explicitly choose which league, stat-type and year by typing "python3 MLBStatScraper.py "league-name"
"stat-type" "year"", where league-name is national, american, or mlb and stat-type is ops, avg, rbi, or hr.
Alternatively, you can choose to uncomment the examples in main and edit those.

One may also decide they need to download many years of csv data all in one go, to accomplish that, simply
uncomment the calls to the test functions and use those. The test functions are designed to start from the
first year mlb.com has stat records for and run the script to ensure there are no errors that may arise should
mlb.com ever decide to change their html layout.
