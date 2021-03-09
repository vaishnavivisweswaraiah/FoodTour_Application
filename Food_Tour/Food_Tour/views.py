from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from xhtml2pdf import pisa
from . web_crawling import *

Table_header = ['Image','Restaurant_Name','Rating','Distance','Add to Tour']
filter_list = ['name','rating','distance','id','image_url'] #To fetch required data
sort_list = ['name','rating','distance'] #sort by given fields
sort_by = ['Ascending','Descending'] #sort by given category
rating_values = ['4.5 and up','4.0 and up','3.0 and up','2.0 and up'] #filter by ratings with rating_values
global output , radius, distance_values,filetype,data #global variables to store locally search results for further processings


def home(re):
    return render(re,'index.html')

#Fetch submit request and do query serach through yelp api and render the result on the html
def result(re):
        global output,radius,distance_values
        food_input="food "+re.POST["Food_Category"]
        location = re.POST["location"]
        country = re.POST.get("country",'US')
        radius = int(re.POST["radius"]) # converting miles to meteres
        distance_values=list((range(1,radius+1))) # to display list of distances within user search limit for applying filters_by radius
        location = ",".join([location,country])
        #Query search based on user request
        output = process_request(search_params= \
              {'term':food_input,'location':location,'radius':int(radius * 1609.34) },filter_columns=filter_list)
        #response dictionary
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
    global output,radius,distance_values
    sort_feature=re.POST.get('sort-select',sort_list[1])
    sort_type=re.POST.get('sort-type',sort_by[1])
    rating_value = re.POST.get('rating_values','0.0 and up')
    distance_value= re.POST.get('distance_values',radius)
    restaurant_name=re.POST.get('restaurant_name',r'^[A-Za-z]+((\s)?((\'|\-|\.)?([A-Za-z])+))*$')
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


def convert_text_dataframe(re):
    response_js = None
    try:
        global data, filetype
        data = re.GET.get('table_content'," ")
        filetype = re.GET.get("convert_to" ," ")
        print(type(data))
        print(data)
        if len(data) > 1 :
            data = process_text(data)
            response_js=json.dumps(convert_dataframe_json(data),indent=4)

    except Exception as e:
        print("error occured at convert_text_dataframe",e)

    return HttpResponse(response_js)

def export_to(re):
    try:
        if filetype == "Download as CSV":
            response=HttpResponse(data.to_csv(index=False),content_type='text/csv')
            response['content-Disposition']='attachment;filename=Finalized_Tour'+str(datetime.datetime.now())+'.csv'

        if filetype == "Download as JSON":
            response=HttpResponse(json.dumps(convert_dataframe_json(data),indent =4),content_type='application/json')
            response['content-Disposition']='attachment;filename=Finalized_Tour'+str(datetime.datetime.now())+'.json'

        if filetype == "Download as PDF":
            content={ 'data' : convert_dataframe_json(data)}
            #creating django response object
            response = HttpResponse(content_type='application/pdf')
            response['content-Disposition']='attachment;filename=Finalized_Tour'+str(datetime.datetime.now())+'.pdf'
            #find tempalate and render it
            template = loader.get_template('pdf-template.html')
            html=template.render(content) # rendering content to html file
            #creating the pdf
            pisa_status=pisa.CreatePDF(html ,dest=response)


    except Exception as e:
            print("Exception occured at export_to",e) 
                'table' :output ,
                 'Table_header':Table_header,
                 'sort_list':sort_list,
                 'sort_by':sort_by,
                 'rating_values':rating_values,
                 'distance_values':distance_values
            }
            return render(re,'result.html',response_dic)
    return response