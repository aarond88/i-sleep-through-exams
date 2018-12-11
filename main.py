## Quick GAE scaffolding to launch the front-end.

import webapp2 as webapp
import jinja2
import wsgiref.handlers
import os
import json
import sys
import MySQLdb
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf8')

#from flask import Flask
#import psycopg2.pool

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE_NAME = os.environ.get('CLOUDSQL_DATABASE_NAME')


def connect_to_cloudsql():
    if True:
		try:
			cloudsql_unix_socket = os.path.join('/cloudsql', CLOUDSQL_CONNECTION_NAME)
			db = MySQLdb.connect(
	            unix_socket=cloudsql_unix_socket,
	            user=CLOUDSQL_USER,
	            passwd=CLOUDSQL_PASSWORD,
	            db=CLOUDSQL_DATABASE_NAME)
	            
		except Exception as e:
			global error_message 
			error_message = sys.exc_info()
    else:
        db = MySQLdb.connect(host='127.0.0.1', user='', passwd='', db='msqldb')
    return db

def executeQuery(query):
	db = connect_to_cloudsql()
	try:
		cursor = db.cursor()
		cursor.execute(query)
		db.commit()
		global response 
		response = cursor.fetchall()
		return response 
	except Exception as e:
		global error_message 
		error_message = sys.exc_info()
	return error_message

def format_to_json(data_stream):
  # NB. Dates don't do well in Python JSON.
  return json.dumps(data_stream, default=str)

def get_data(parameter):
	## Return a constant for the moment.
	return format_to_json(getEventDetails())

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class AboutPageHandler(webapp.RequestHandler):
  def get(self, *args):

    template_values = {'title': 'Strong Feather Team'}
    template = JINJA_ENVIRONMENT.get_template('about.html')
   
    self.response.write(template.render(template_values))

class MainPageHandler(webapp.RequestHandler):
  def get(self, *args):

    print self.request

    countrydata = getCountryData()
    
    template_values = {'title': 'Weather Status', 'errormessage': '', 'countrydata': countrydata}
    template = JINJA_ENVIRONMENT.get_template('index.html')

    self.response.write(template.render(template_values))


class CreatePageHandler(webapp.RequestHandler):
  def get(self):

    template_values = {'title': 'Strong Feather Events'}
    template = JINJA_ENVIRONMENT.get_template('create.html')

    self.response.write(template.render(template_values))

class EventAPIHandler(webapp.RequestHandler):
  def get(self):
    #events = get_data('events')
    self.response.write([])
  def post(self):
    payload = self.request
    data = payload.body

class DonationAPIHandler(webapp.RequestHandler):
  def get(self):
    donations = [1, 2, 3]
    self.response.write(donations)

  def post(self):
    payload = self.request
    data = payload.body
    print data


routes = [
  webapp.Route(r'/', handler=MainPageHandler, name="home"),
]

app = webapp.WSGIApplication(
  routes,
  debug=os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')
)


# Get all event details
def getCountryData():
	allCountries = executeQuery("SELECT country, countryname FROM countrycodes ORDER BY countryname ASC;") 
	return allCountries
