# mtrap
Pipeline for analysis of Gerrit code reviews. Fetches information about changes and visualizes opened and closed changes over time.
The program uses the 'requests' package to retrieve data with HTTP GET requests, and 'matplotlib' is used to plot the data.
When run the program will save the plots and the data in directories 'mtrap_plots/' and 'mtrap_json_logs/' respectively. These directories will be created in the same directory as the program file itself.

## Dependencies
Python packages:  
  -requests  
  -matplotlib  
  -numpy  
These can be installed using the "requirements.txt" file.
```
pip install -r requirements.txt
```

## Usage
Example run, where the program is in 'C:\Users\exmpl\'
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
