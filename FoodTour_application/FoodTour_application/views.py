from django.shortcuts import render

from . web_crawling import *

Table_header = ['Restaurant_Name','Rating','Distance','Add to Tour']
sort_list = ['name','rating','distance']
sort_by = ['Ascending','Descending']

rating_values = ['4.5 and up','4.0 and up','3.0 and up','2.0 and up']
distance_values = []

global output
global radius



def home(re):
    return render(re,'index.html')


def result(re):
        global output
        global radius
        food_input=re.POST["Food_Category"]
        address1 = re.POST["address1"]
        address2 = re.POST["address2"]
        city = re.POST["city"]
        state = re.POST["state"]
        country = re.POST.get("country",'NONE')
        zipcode = re.POST["zipcode"]
        radius = int(re.POST["radius"]) # converting miles to meteres
        distance_values=list((range(1,radius+1)))
        location = ",".join([address1,address2,city,state,country,zipcode])
        print(location)
        print(type(radius))
        output = process_request(search_params= \
              {'term':food_input,'location':location,'radius':int(radius * 1609.34) },filter_columns=sort_list)
        response_dic = {
            'table' :output ,
             'Table_header':Table_header,
             'sort_list':sort_list,
             'sort_by':sort_by,
             'rating_values':rating_values,
             'distance_values':distance_values
        }
        return render(re,'result.html',response_dic)

def filter_sort(re):
    global output
    global radius
    sort_feature=re.GET.get('sort-select',sort_list[1])
    sort_type=re.GET.get('sort-type',sort_by[1])
    rating_value = re.GET.get('rating_values','0.0 and up')
    distance_value= re.GET.get('distance_values',radius)
    restaurant_name=re.GET.get('restaurant_name',r'^[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*$')

    output=convert_list_DataFrame(list=output)
    output=sort_dataframe(dataframe=output,sort_feature=sort_feature,sort_by_asc=sort_type)
    temporal_output=filter_dataframe(dataframe=output,rating=rating_value,distance=distance_value,name=restaurant_name)

    distance_values=list((range(1,radius+1)))
    response_dic = {
        'table' : convert_dataframe_json(dataframe=temporal_output) ,
         'Table_header':Table_header,
         'sort_list':sort_list,
         'sort_by':sort_by,
         'rating_values':rating_values,
         'distance_values':distance_values
    }
    return render(re,'result.html',response_dic)
