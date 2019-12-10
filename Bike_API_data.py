
# coding: utf-8

# In[ ]:


#!/usr/bin/python


# In[ ]:


import requests
import csv
import json
import pandas as pd
import datetime


# In[ ]:


#Creating an empty dataframe for responses 
df_final_datewise=pd.DataFrame()
#endtime set for 40 days from script run
endTime = datetime.datetime.now() + datetime.timedelta(days=40)
#Initialization of previous date as script run date
date_prev=datetime.datetime.now().date().strftime("%m %d %Y")

while datetime.datetime.now().date().strftime("%m %d %Y") <= endTime.date().strftime("%m %d %Y"):
    
    #Running the script hour-wise , everday
    if(':00:00' in datetime.datetime.now().time().strftime("%H:%M:%S.%f")):
        date_next=datetime.datetime.now().date().strftime("%m %d %Y")
        #api key generated from https://developer.jcdecaux.com/#/opendata/vls?page=getstarted
        api_key = "4834959d5e8197387aa4f3e1511982ae412c83c6"
        #api call
        resp = requests.get("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey="+api_key)
        #loading responses to json
        responses = json.loads(resp.text)
        for response in responses:
            time=response['last_update']
            #Converting timestamp to standard date time format
            response['last_update']= datetime.datetime.fromtimestamp(time / 1e3)
            #Storing the responses in data frame
            df=pd.DataFrame(responses)
        #Checking for date condition for storing data into csv files
        if date_prev== date_next:
            df_final_datewise=df_final_datewise.append(df)
            #df_final_datewise.to_csv(date_prev+'.csv')
        else:
            #Creating different csv files for each date
            df_final_datewise.to_csv(date_prev+'.csv')
            df_final_datewise=pd.DataFrame(df)
    else:
        continue
    date_prev= date_next
    

