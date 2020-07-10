import json

import httplib2
from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__, template_folder='template')

api_key = ''

@app.route('/success/<name>+<count>+<date>')
def success(name, count, date, lat, lon):
    mydict = {'name': name, 'count': count, 'date': date, 'lng': lon, 'lat': lat}
    return render_template('Home.html', success= mydict, api_key=api_key)

@app.route('/app',methods = ['POST', 'GET'])
def form_data():
   if request.method == 'POST':
      user = request.form['nm']
      count = request.form['nm2']
      date = request.form['nm3']
      lat, lon = getGeocodeLocation(user)
      mydict = {'name': user, 'count': count, 'date': date, 'lng': lon, 'lat': lat}
      return render_template('Home.html', success= mydict, api_key=api_key)
   else:
      user = request.args.get('nm')
      count = request.form['nm2']
      date = request.form['nm3']
      lat, lon = getGeocodeLocation(user)
      mydict = {'name': user, 'count': count, 'date': date, 'lng': lon, 'lat': lat}
      return render_template('Home.html', success= mydict, api_key=api_key)


def getGeocodeLocation(inputString):
   # Use Here Maps to convert a location into Latitute/Longitute coordinates
   # FORMAT: https://geocode.search.hereapi.com/v1/geocode?q=5+Rue+Daunou%2C+75000+Paris%2C+France

   locationString = inputString.replace(" ", "+")
   relevance = 1
   url = ('https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey=%s&searchtext=%s&relevance=%s' % (
   api_key, locationString, relevance))

   h = httplib2.Http()
   result = json.loads(h.request(url, 'GET')[1])
   latitude = result.get('Response').get('View')[0].get('Result')[0].get('Location').get('DisplayPosition').get(
      'Latitude')
   longtitude = result.get('Response').get('View')[0].get('Result')[0].get('Location').get('DisplayPosition').get(
      'Longitude')
   return (latitude, longtitude)


if __name__ == '__main__':
   app.run(debug=True)
