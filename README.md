# NYC Bike Sharing System Analysis
# Dashboard Preview
Popularity Analysis

![](img/pop1.PNG?raw=true)
![](img/pop2.PNG?raw=true)

Shortage and Overload Analysis
![](img/short.PNG?raw=true)
# Download nearby_stations.csv
Since the file is over 100MB, please download here:
https://drive.google.com/open?id=1d6y7ripwLc235UxezdMtvKHv010DISrk
and save it to ui/data/q2_data

# Reproducing Layer Structure

For detail instructions, Please refer to [Running.txt](Running.txt)<br/>
For fetched data download, Please go to https://drive.google.com/open?id=1YmHJwR3xzXCQQiQEnZV2IKUQux_M6MXg 

# Running front-end UI

```
cd ui
```

Question 1: NYC Bike Station Popularity  
step 1: 
```
python q1.py
```
step 2: copy the URL into browser  
step 3: select year | month | time frame combinations in the left box  
step 4: Click one of the  bars in the chart to see the corresponding station in the map  

Question 2: NYC Bike Shortage and Overload  
step 1:   
```
python q2.py
```
step 2: copy the URL into browser  
step 3: select a date from datepicker  
step 4: select a shortage station in dropdown  
step 5: click a shortage hour in histogram, the supply station will be listed under the ‘supply station list’ on the left green box.  
(note: if there is no supply station, nothing will be shown in the ‘supply station list’ section.)  

Question 3: Recommend New Stations  
step 1: 
```
python q3.py
```
step 2: copy the URL into browser   
step 3: select the number of clusters  

