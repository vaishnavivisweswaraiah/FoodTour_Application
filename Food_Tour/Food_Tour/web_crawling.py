import requests
import pandas as pd
import json , csv
import datetime,time


def filter_dataframe(dataframe,rating,distance,name):

    rating_value=eval(rating.split("and")[0])
    distance_value=float(distance)
    restaurant_name=name.title()
    return dataframe[(dataframe['rating'] >= rating_value) & (dataframe['distance'] <= distance_value) & \
                      (dataframe['name'].str.contains(restaurant_name)) ]


#function to add sorting and filters to dataframe
def sort_dataframe(dataframe,sort_feature='rating',sort_by_asc=False):
    if sort_by_asc=='Ascending':
        sort_by_asc=True
    elif sort_by_asc=='Descending':
        sort_by_asc=False
    return dataframe.sort_values(by=sort_feature, kind='mergesort',ascending=sort_by_asc,ignore_index=True)\
                            if not dataframe.empty else dataframe

#function convert dataframe to html renderable json format
def convert_dataframe_json(dataframe):
    json_records=dataframe.to_json(orient ='records')
    return json.loads(json_records )

#function to convert list to dataframe
def convert_list_DataFrame(list):
    return pd.DataFrame(list)

#process the json api response into html form
def process_JSON(JSON_response,filter_columns):
    #print("**",JSON_response)
    #normalize json and convert it into dataframe
    df=pd.json_normalize(JSON_response,record_path=["businesses"])
    #filter required columns from dataframe
    df_response=df.filter(regex='|'.join(filter_columns))
    #convert meteres to miles
    return df_response.apply(lambda x: round(x/1609.34,2) if x.name == 'distance' else x)


#fetch data throuh API and process the result
def process_request(search_params,filter_columns):
    url="https://api.yelp.com/v3/businesses/search"
    api_key='B6thriYagtEILIQsSm_Rsm0OIBGjs0j_WUpgCsAwXY_CGmJ6rQccHA2z3rxLdVrJdQ4ay1wNlll557IVdBHyA3JwYBgV3fqJsvtjXGXiioeYHa-NEeGvjHNgj6A9YHYx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    JSON_response = requests.get(url,headers=headers,params=search_params).json()
    #handling exception for null response from API
    result=process_JSON(JSON_response,filter_columns)
    result=sort_dataframe(result)
    result=convert_dataframe_json(result)
    return result

#function to process table content retrived from html and processed using js and sent to download file python function
def process_text(message):
    data=[]
    message=message.rstrip().lstrip()
    for row in message.split("\n"):
        data.append(row.split("\t"))
    data=pd.DataFrame(data ,columns=['name','rating','distance_in_miles'])
    return data
