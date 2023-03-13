# mtrap
Pipeline for analysis of Gerrit code reviews. Fetches information about changes and visualizes opened and closed changes over time.
The program uses the 'requests' package to retrieve data with HTTP GET requests, and 'matplotlib' is used to plot the data.
When run the program will save the plots and the data in directories 'mtrap_plots/' and 'mtrap_json_logs/' respectively. These directories will be created in the same directory as the program file itself. The program will create four different plots, one each for 'Opened', 'Closed', and 'Abandoned' reviews, as well as one total showing all three.

## Requirements
Python 3.9 or newer recommended (probably works with older versions, not tested though)
Python packages:  
  -requests  
  -matplotlib  
  -numpy  
These can be installed using the 'requirements.txt' file.
```
pip install -r requirements.txt
```

## Usage
When installed the program can be run using:
```
python mtrap.py
```
When promted for a source, it is not required to type the whole source name, the first letter is enough.  
After a time frame has been chosen, the program starts crawling data from Gerrit, which will take a while, especially if a longer time frame is entered.  
When the program finishes crawling data it will save results as a JSON file in the directory 'mtrap_json_logs/' and plots in 'mtrap_plots/'. These sub-directories are located in the same directory as the 'mtrap.py' file.  
Example run, where the program is in 'C:\Users\exmpl\':
```
py mtrap.py
Pick one of the following as source for analysis [chromium | openstack | android]: c
   Source: https://chromium-review.googlesource.com/changes/
Choose a number of days in the past to analyze from (1-60): 1
   Number of days: 1
Fetching data...
 Plots saved in: 'C:\Users\exmpl\mtrap_plots'
 Data saved as JSON in: 'C:\Users\exmpl\mtrap_json_logs'
```
