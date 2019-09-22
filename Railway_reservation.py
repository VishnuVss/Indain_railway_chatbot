# importing Packages
from flask import Flask
from flask import request
from flask import make_response
import json
import requests

# flask set up
app = Flask(__name__)

# handling the webhook request
@app.route('/webhook', methods=["GET","POST"])

def webhook():

    # getting the request from dialogflow
    req = request.get_json(silent=True, force=True)

    # getting the intent name from the dialog flow
    intent_name = req["queryResult"]["intent"]["displayName"]

    # handling the intents from the dialog flow
    if(intent_name == 'Train_information'):
        return traininfo(req)
    if(intent_name == 'Station_Location'):
        return location_on_map(req)
    if(intent_name == 'Code_to_name'):
        return codetoname(req)
    if(intent_name == 'Name_to_code'):
        return nametocode(req)
    return {}


#This function is for train information
def traininfo(data):

    #getting the action from the request json
    action = data["queryResult"]["action"]

    #getting train number
    number = int(data["queryResult"]["parameters"]["number"])

    #base url of train information api
    req_url="http://indianrailapi.com/api/v2/TrainInformation/apikey/6df9b792fb69a238e67738655a47cdb9/TrainNumber/" + str(number) + "/"
    
    
	# sending the request to indian railway api and converting the response to json
    obj = requests.get(req_url).json()

    # getting the data from the request
    train_name = obj["TrainName"]
    source_stationcode = obj["Source"]["Code"]
    source_time = obj["Source"]["Arrival"]
    dest_stationcode = obj["Destination"]["Code"]
    dest_time = obj["Destination"]["Arrival"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse(train_name, source_stationcode, source_time, dest_stationcode, dest_time)
    return {}
 
#This function is for sending train information to dialogflow
def MakeTextResponse(train_name, source_stationcode, source_time, dest_stationcode, dest_time):
    return {
        "fulfillmentText": "Train Name: " + train_name + " Source Station Code: " + source_stationcode + " Source Time: " + source_time + " Destinaton Station Code: " + dest_stationcode + " Destination Time: " + dest_time 
    }




#This function is for station location on map
def location_on_map(data):

    #getting the action from the request json
    action = data["queryResult"]["action"]

    #getting station code
    station_code = data["queryResult"]["parameters"]["station_code"]

    #base url of location on map api
    req_url="http://indianrailapi.com/api/v2/StationLocationOnMap/apikey/6df9b792fb69a238e67738655a47cdb9/StationCode/" + station_code + "/"

    # sending the request to indian railway api and converting the response to json
    obj=requests.get(req_url).json()

    # getting the data from the request
    station_code = obj["StationCode"]
    station_name = obj["StationName"]
    map_url = obj["URL"]

    # generating the text response
    if(action == "TextResponse"):
        return MakeTextResponse2(station_code, station_name, map_url)
    return {}   

#This function is for sending location on map to dialogflow
def MakeTextResponse2(station_code, station_name, map_url):
    return {
        "fulfillmentText": "Station Code: " + station_code + " Station Name: " + station_name + " Map URL: " + map_url
    }


#This function is code to name
def codetoname(data):

    #getting the action from the request json
    action = data["queryResult"]["action"]

    #getting station code
    station_code = data["queryResult"]["parameters"]["code"]

    #base url of code to name
    req_url="http://indianrailapi.com/api/v2/StationCodeToName/apikey/6df9b792fb69a238e67738655a47cdb9/StationCode/" + station_code + "/"
    
    #Sending the request to indian railway api and converting the response to json
    obj=requests.get(req_url).json()

    #generating the text response
    station_name_en = obj["Station"]["NameEn"]
    station_name_hn = obj["Station"]["NameHn"]

    #this function is for sending code to name 
    if(action == "TextResponse"):
        return MakeTextResponse5(station_name_en, station_name_hn)
    return {}

#This function is for sending code to name to dialogflow
def MakeTextResponse5(station_name_en, station_name_hn):
    return {
       "fulfillmentText": "Station Name in English: " + station_name_en + " Station name in Hindi"  + station_name_hn 
    }




#This function is name to code
def nametocode(data):

    #getting the action from the request json
    action = data["queryResult"]["action"]

    #getting station code
    station_name = data["queryResult"]["parameters"]["name"]

    #base url of code to name
    req_url="http://indianrailapi.com/api/v2/StationNameToCode/apikey/6df9b792fb69a238e67738655a47cdb9/StationName/" + station_name + "/"
    
    #Sending the request to indian railway api and converting the response to json
    obj=requests.get(req_url).json()
    
    #generating the text response
    station_code = obj["Station"]["StationCode"]

    #this function is for sending name to code
    if(action == "TextResponse"):
        return MakeTextResponse4(station_code)
    return {}

#This function is for sending name to code to dialogflow
def MakeTextResponse4(station_code):
    return {
        "fulfillmentText": "Sation code: " + station_code
    }


if __name__ == '__main__':
    app.run(port=3000, debug=True)