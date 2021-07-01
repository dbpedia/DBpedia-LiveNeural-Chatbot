'''import pandas as pd
df=pd.read_csv('onlySpotlight.csv',encoding= 'unicode_escape',names=['Ques','Bench Ent','Ann Ent','Pr','Rc'])
df1=df.loc[(df['Pr']==0.0) & (df['Rc']==0.0)]
print(df1.head())
df1.to_csv('failedSpotlight.csv',encoding= 'unicode_escape',index=False)'''
import requests
import json
import xmltodict


headers = {
        'Content-Type': 'application/json',
    }
text="wizards"
response = requests.post('https://lookup.dbpedia.org/api/search?MaxHits=2&QueryString='+text,headers=headers)
j=response.content.decode("utf-8")
data_dict = xmltodict.parse(j)
json_data = json.dumps(data_dict,indent=4)
print(json_data)
data = json.loads(json_data)
list_ent=[i["Label"] for i in data["ArrayOfResults"]["Result"] if "Wizards_vs_Aliens" in i["URI"]]
print(list_ent)
