import json
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')



def main():
	with open('citylist2') as f:
	    allData = json.load(f)
	db = ""#connect_to_cloudsql()
	try:
		
		for data in allData:
			#print("insert into cities (id, name, country, lon, lat) values (" + str(data['id']) + ", \'" + str(data['name']).encode('utf-8') + "\', \'" + data['country'] + "\', " + str(data['coord']['lon']) + ", " + str(data['coord']['lat']) + ");")
			print("insert ignore into countrycodes (country) values (\'" + data + "\');")
		
	except Exception as e:
		global error_message 
		error_message = sys.exc_info()
		print(error_message)
	return ""
	
if __name__ == "__main__":
    main()

