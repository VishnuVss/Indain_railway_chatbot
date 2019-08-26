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
    
	# getting the intent name
	intent_name = req["queryResult"]["intent"]["displayName"]
	
	# handling the intents
	if(intent_name == "TrainInfo"):
        return traininfo(req)
    return {}
	if(intent_name == "Location"):
        return location_on_map(req)
    return {}
	if(intent_name == "Station_search"):
        return search(req)
    return {}
	if(intent_name == "Name_to_code"):
        return nametocode(req)
    return {}
	if(intent_name == "Code_to_name"):
        return codetoname(req)
    return {}
	if(intent_name == "Pnr_Number"):
		return pnrnumber(req)
	return {}
	if(intent_name == "Fog_Affected_Train")
		return fogtrain(req)
	return {}

#converting name to code
	def nametocode(data):
    #getting the action from the request json
    action = data["queryResult"]["action"]
	#getting station name
    station_name = data["queryResult"]["parameters"]["name"]
	#base url for name to code
    url="http://indianrailapi.com/api/v2/StationNameToCode/apikey/6df9b792fb69a238e67738655a47cdb9/StationName/" + station_name + "/"
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	# getting the data from the request
	station_code = obj["Station"]["StationCode"]
	
	# generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse4(station_code)
    return {}
	
# this func is for sending station code to dialogflow
def MakeTextResponse4(station_code):
    return {
        "fulfillmentText": "Sation code: " + station_code
    }


#code to name
	def codetoname(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]
	# getting station code
    station_code = data["queryResult"]["parameters"]["code"]
	# base url for code to name
	url="http://indianrailapi.com/api/v2/StationCodeToName/apikey/6df9b792fb69a238e67738655a47cdb9/StationCode/" + station_code + "/"
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	# getting the data from the request
	station_name_en = obj["Station"]["NameEn"]
	station_name_hn = obj["Station"]["NameHn"]
	
	# generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse5(station_name_en, station_name_hn)
    return {}
	
# this func is for sending station code to dialogflow
def MakeTextResponse5(station_name_en, station_name_hn):
    return {
        "fulfillmentText": "Station Name in English: " + station_name_en + " Station name in Hindi" " + station_name_hn
    }

    #location on map
def location_on_map(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]
	# getting station code
    station_code = data["queryResult"]["parameters"]["code"]
	# base url for locatio on map
    url="http://indianrailapi.com/api/v2/StationLocationOnMap/apikey/6df9b792fb69a238e67738655a47cdb9/StationCode/" + station_code + "/"
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	# getting the data from the request
	station_code = obj["StationCode"]
	station_name = obj["StationName"]
	map_url = obj["URL"]
	
	# generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse2(station_code, station_name, map_url)
    return {}

# this func is for sending location to dialogflow
def MakeTextResponse2(station_code, station_name, map_url):
    return {
        "fulfillmentText": "Station Code: " + station_code + " Station Name: " + station_name + " Map URL: " + map_url
    }
	

#viewing location of the train	
def search(data):
    # getting the action from the request json
    action = data["queryResult"]["action"]
	# getting station name
    station_name = data["queryResult"]["parameters"]["name"]
	# base url for station search
    url="http://indianrailapi.com/api/v2/AutoCompleteStation/apikey/6df9b792fb69a238e67738655a47cdb9/StationCodeOrName/" + station_name + "/"
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	# getting the data from the request
	nameen = obj["Station"]["NameEn"]
	namehn = obj["Station"]["NameHn"]
	station_code = obj["Station"]["StationCode"]
	long = obj["Station"]["Longitude"]
	lat = obj["Station"]["Latitude"]
	
	# generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse3(nameen, namehn, station_code, long, lat)
    return {}

	

#train info
def traininfo(data):
    
	# getting the action from the request json
	action = data["queryResult"]["action"]
	
	# getting the train number from the request
    num = int(data["queryResult"]["parameters"]["number"])
	
	# base url for traininfo
    url = "http://indianrailapi.com/api/v2/TrainInformation/apikey/6df9b792fb69a238e67738655a47cdb9/TrainNumber/" + str(num) + "/"
    
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	
	# getting the data from the request
    train_name = obj["TrainName"]
    source_stationcode = obj["Source"]["Code"]
    source_time = obj["Source"]["Arrival"]
    dest_stationcode = obj["Destination"]["Code"]
    dest_time = obj["Destination"]["Arrival"]

    # generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse1(train_name, source_stationcode, source_time, dest_stationcode, dest_time)
    return {}

# this func is for sending train info to dialogflow
def MakeTextResponse1(train_name, source_stationcode, source_time, dest_stationcode, dest_time):
    return {
        "fulfillmentText": "Train Name: " + train_name + " Source Station Code: " + source_stationcode + " Source Time: " + source_time + " Destinaton Station Code: " + dest_stationcode + " Destination Timr: " + dest_time 
    }
	

	
#sending current loc of train to dialogflow
def MakeTextResponse3(nameen, namehn, station_code, long, lat):
    return {
        "fulfillmentText": "NameEn: " + nameen + " NameHn: " + namehn + " Sation code: " + station_code + " Longitude: " + long + " Latitude: " + lat
    }

    # this func is for fog affected train
	def fogtrain(data)
	# getting the action from the request json
    action = data["queryResult"]["action"]
	# base url for code to name
	url="https://indianrailapi.com/api/v2/FogAffectedTrains/apikey/6df9b792fb69a238e67738655a47cdb9/"
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	# getting the data from the request
	train_no = obj["Trains"]["TrainNo"]
	train_name = obj["Trains"]["TrainName"]
	last_station = obj["Trains"]["LastStation"]
	status = obj["Trains"]["Status"]
	expected_arrival = obj["Trains"]["ExpectedArrival"]
	last_update =  obj["LastUpdate"]
	
	# generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse7(train_no, train_name, last_station, status, expected_arrival, last_update)
    return {}
	
# this func is for sending station code to dialogflow
def MakeTextResponse7(train_no, train_name, last_station, status, expected_arrival, last_update):
    return {
        "fulfillmentText": "Train No: " + train_no + " Train Name: " + train_name + " Last Station: " + last_station + " Status: " + status + " Expected Arrival: " + expected_arrival + " Last Update: + last_update 
    }	
	
	

	
#pnr number
	def pnrnumber(data)
	# getting the action from the request json
    action = data["queryResult"]["action"]
	# getting pnr number
    pnr_number = data["queryResult"]["parameters"]["code"]				
	# base url for code to name
	url="http://indianrailapi.com/api/v2/PNRCheck/apikey/6df9b792fb69a238e67738655a47cdb9/PNRNumber/" + pnr_number + "/Route/1/"
	# sending the request to indian railway api and converting the response to json
	obj=requests.get(url).json()
	# getting the data from the request
	pnr_number = obj["PnrNumber"]
	train_no = obj["TrainNumber"]
	train_name = obj["TrainName"]
	journey_class =  obj["JourneyClass"]
	from = obj["From"]
	to = obj["To"]
	joureny_date = obj["JourneyDate"]
	
	# generating the text response
	if(action == "TextResponse"):
        return MakeTextResponse6(pnr_number, train_no, train_name, journey_class, from, to, joureny_date)
    return {}
	
# this func is for sending station code to dialogflow
def MakeTextResponse6(pnr_number, train_no, train_name, journey_class, from, to, joureny_date):
    return {
        "fulfillmentText": "PNR Number: " + pnr_number + " Train No: " + train_no + " Train Name: " + train_name + " Journey Class: " + journey_class + " From: " + from + " To: " + to + " Journey Date: " + joureny_date  
    }


