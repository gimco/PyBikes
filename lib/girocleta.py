# -*- coding: utf-8 -*-
from station import Station

import re
import urllib,urllib2
from BeautifulSoup import BeautifulSoup

RE_LATLNG='var pParking(.*)'
RE_INFO = 'var html(.*)'
PREFIX = "girocleta"
URL = "http://www.girocleta.cat/Mapadestacions.aspx"


def getInt(data):
	re1='.*?'	# Non-greedy match on filler
	re2='(\\d+)'	# Integer Number 1
	
	rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
	m = rg.search(data)
	if m:
		int1=m.group(1)
		return int1
	return None

def getInfo(data):
	soup = BeautifulSoup(data)
	info = []
	for shit in soup.div.contents:
		info.append(unicode(shit.contents[0].encode('ascii','ignore')))
	id = info[0]
	name = info[1]
	bikes = getInt(info[2])
	free = getInt(info[3])
	return [id,name,bikes,free]


def getLatLng(data):
	re1='.*?'	# Non-greedy match on filler
	re2='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 1
	re3='.*?'	# Non-greedy match on filler
	re4='([+-]?\\d*\\.\\d+)(?![-+0-9\\.])'	# Float 2
	rg = re.compile(re1+re2+re3+re4,re.IGNORECASE|re.DOTALL)
	m = rg.search(data)
	if m:
    		float1=m.group(1)
    		float2=m.group(2)
		return [float1,float2]
    	else:
		return None
	

def get_all():
	usock = urllib2.urlopen(URL)
	data = usock.read()
	usock.close()

	latlngs = re.findall(RE_LATLNG,data)
	infos = re.findall(RE_INFO,data)
	
  	stations = []
  	for index,latlng in enumerate(latlngs):
    		station = GirocletaStation(index)
		info = getInfo(infos[index])
		latlng = getLatLng(latlng)
		station.fromData(info[0],info[1],int(float(latlng[0])*1E6),int(float(latlng[1])*1E6),info[2],info[3])
    		stations.append(station)
  	return stations


class GirocletaStation(Station):
  prefix = PREFIX
  main_url = URL

  def fromData(self, name, description, lat, lng, bikes, free):
	  self.name = name
	  self.description = description
	  self.lat = lat
	  self.lng = lng
	  self.bikes = bikes
	  self.free = free
	  return self
    
  def to_json(self):
    text =  '{"id":"%s", "name":"%s", "lat":"%s", "lng":"%s", "timestamp":"%s", "bikes":%s, "free":%s, "description":"%s"}' % \
    (self.idx, self.name, self.lat, self.lng, self.timestamp, self.bikes, self.free, self.description)
    print text.encode('utf-8'),
    return text.encode('utf-8')