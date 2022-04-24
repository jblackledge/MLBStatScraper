# MLBStatScraper
This script scrapes and parses the MLB website to generate a CSV file of the MLB leaders of a chosen league and year. The csv file lists the name name, OPS, batting average, RBI's, and HR's for each player, sorted by the chosen stat type. The generated csv files are perfect for simple machine learning and data science projects.


## Installation
Simply download the code from this repo. This script works on all systems with a python 3 interpreter.

## Usage
### Quick Start
Once downloaded, use the terminal to cd into the folder you downloaded it to. There type "make all" to run the included demo that will create a csv file of all MLB leaders in the current year, sorted by OPS. You can also explicitly choose which league, stat-type and year by typing "python3 MLBStatScraper.py "league-name" "stat-type" "year"", where league-name is one of "national", "american", or "mlb" and stat-type is "ops", "avg", "rbi", or "hr". Specifying a stat type sorts the data based on the leader of the specified stat category.

### Large Data Sets
One may also decide they need to download many years of csv data all in one go, there are two ways to accomplish this. If you need data from all three leagues in a custom year span, type "python3 MLBStatScraper.py "beginning-year" "ending-year"". Where "beginning-year" and "ending-year" are any year greater than or equal to 1903, less than or equal to the current year, and "ending-year" is greater than "beginning-year". 

If you need data from all three leagues for all possible years, simply type in the console "python3 MLBStatScraper.py all". This will call the the largest test function and provide feedback to the user on the current status. The test functions are designed to start from the first year mlb.com has stat records for and run until the current year to ensure there are no errors that may arise should mlb.com ever decide to change their html layout. The individual tests take approximately twenty minutes to complete per stat-type, and running a test provides visual feedback via console print statements to allow you to see how much data you've gathered so far.

### MVP Large Data Set
In [my own machine learning project](https://github.com/jblackledge/MLB-MVP-Predictor), I am using a custom dataset that scrapes the stats of the league leaders from every year that a hitter won the MVP, and includes an extra column denoting whether that player won the mvp or not in that year. The csv file includes ~4,000 lines of data and is perfect for both classification and regression models. To generate this MVP dataset, simply type "python3 MLBStatScraper.py mvp" to generate the csv with a string mvp column ("mvp"/"not mvp"), or type "python3 MLBStatScraper.py mvp binary" to generate the csv with a binary mvp column (1/0).

I have purposely chosen to leave out years in which a pitcher has won the MVP because the dataset focuses only on hitting data, and I want to avoid "confusing" my model. Pitchers rarely win the MVP award, but when they do, it's because they had a phenomenal year pitching, and not because hitters had a bad year hitting. Meaning that if the pitcher only had an average year (not MVP caliber), then a hitter would have likely won. This means that hitting data in those years doesn't tell us anything about the type of hitting stats required to win the MVP, and would only cause problems with our model. 
