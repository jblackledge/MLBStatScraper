# MLBStatScraper
This script scrapes and parses the MLB website to generate a CSV file of the MLB leaders of a chosen league and year. The csv file lists the name name, OPS, batting average, RBI's, and HR's for each player, sorted by the chosen stat type. The generated csv files are perfect for simple machine learning and data science projects.


## Installation
Simply download the code from this repo. This script works on all systems with a python 3 interpreter.

## Usage
### Quick Start
Once downloaded, use the terminal to cd into the folder you downloaded it to. There type "make all" to run the included demo that will create a csv file of all MLB leaders in the current year, sorted by OPS. You can also explicitly choose which league, stat-type and year by typing "python3 MLBStatScraper.py "league-name" "stat-type" "year"", where league-name is one of "national", "american", or "mlb" and stat-type is "ops", "avg", "rbi", or "hr".

### Large Data Sets
One may also decide they need to download many years of csv data all in one go, there are two ways to accomplish this. If you need data from all three leagues in a custom year span, type "python3 MLBStatScraper.py "beginning-year" "ending-year"". Where "beginning-year" and "ending-year" are any year greater than or equal to 1903, less than or equal to the current year, and "ending-year" is greater than "beginning-year". 

If you need data from all three leagues for all possible years, simply type in the console "python3 MLBStatScraper.py all". This will call the the largest test function and provide feedback to the user on the current status. The test functions are designed to start from the first year mlb.com has stat records for and run until the current year to ensure there are no errors that may arise should mlb.com ever decide to change their html layout. The individual tests take approximately twenty minutes to complete per stat-type, and running a test provides visual feedback via console print statements to allow you to see how much data you've gathered so far.
