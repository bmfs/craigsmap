import feedparser
import re
import simplejson
import web

import urllib2
urllib2.install_opener(urllib2.build_opener())
        
urls = (
	'/get/', 'Elements',
    '/', 'Index',

)
app = web.application(urls, globals())
render = web.template.render('templates/')

addressStart = r'!-- CLTAG GeographicArea='
addressEnd = r'-->'
locationReg = re.compile(addressStart + r'(.*?)' + addressEnd)
		
roadexp = r'\((.*?Road.*?)\)'
roadReg = re.compile(roadexp)
		
nearatExp = r'(near|at|@) (.*?)(MRT|for|For)'
nearatReg = re.compile(nearatExp)

mrtExp = r'\((.*?)(MRT|mrt)'
mrtReg = re.compile(mrtExp)

parentesisExp = r'\((.*?)\)'
parentesisReg = re.compile(parentesisExp)

def getLocation(entry):
	locationRes = re.search(locationReg,entry['description'])
	if (locationRes != None):
		return locationRes.group(1).replace('Link', 'Road').replace('MRT','')
		
	locationRes = re.search(roadReg,entry['title'])
	if (locationRes != None):
		return locationRes.group(1)
	
	locationRes = re.search(nearatReg, entry['title'])
	if (locationRes != None):
		return locationRes.group(2)

	locationRes = re.search(mrtReg, entry['title'])
	if (locationRes != None):
		return "%s Mrt" % locationRes.group(1)
	
	parentesisReg

	locationRes = re.search(parentesisReg, entry['title'])
	if (locationRes != None):
		return locationRes.group(1)

	return None
	
def getElements(query="condo", start=0, minAsk=600, maxAsk = 1300):

		price = r'SGD([0-9]*)'
		priceprog = re.compile(price)
		url = 'http://singapore.craigslist.org/search/roo?query=%s&minAsk=%s&maxAsk=%s&srchType=A&format=rss&s=%s' % (urllib2.quote(query),minAsk, maxAsk,start)
		#url = 'http://singapore.craigslist.com.sg/roo/index.rss'
		
		
		print url
		d = feedparser.parse(url)
	
		results = []
		print len(d['entries'])
		for entry in d['entries']:
			
			priceres = re.search(priceprog, entry['title'])
			tmp = {}
			tmp['url'] = entry['link']
			tmp['title'] = entry['title']
			
			location = getLocation(entry);
			if (location != None):
				tmp['location'] = "%s, Singapore" % (location)
				
				
			if (priceres != None):
				tmp['price'] = priceres.group(1)
			results.append(tmp)
	
		return simplejson.dumps(results)

class Elements:

	def GET(self):
		input_data = web.input(query="condo", start=0, minAsk=600, maxAsk=1300)
		return getElements(input_data.query, input_data.start, input_data.minAsk, input_data.maxAsk);

class Index:        
	def GET(self):
		input_data = web.input(query="condo", start="0", minAsk=600, maxAsk=1300)
		start = input_data.start
		query = input_data.query
		minAsk = input_data.minAsk
		maxAsk = input_data.maxAsk
		next = int(('0'+start))+10
		return render.index(query, start, next, minAsk, maxAsk)

if __name__ == "__main__":
    app.run()