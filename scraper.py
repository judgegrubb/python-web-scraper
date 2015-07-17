from lxml import html
from pymongo import MongoClient
import requests
import datetime

# simply change the dept variable in the link below to scrape different deptartments at the U
page = requests.get('http://www.acs.utah.edu/uofu/stu/scheduling?term=1158&dept=CS&classtype=g')
tree = html.fromstring(page.text)

classes = tree.xpath('//tr[@valign="top"]')

classNumbers = []
catalogNumbers = []
sections = []
components = []
units = []
titles = []
daysTaught = []
times = []
locations = []
instructors = []


for c in classes:
	cdata = c.xpath('td')
	if len(cdata) == 16:
		classNumbers.append(cdata[1].xpath('font/text()')[0])
		catalogNumbers.append(cdata[3].xpath('font/a/text()')[0])
		sections.append(cdata[4].xpath('font/text()')[0])
		components.append(cdata[5].xpath('font/text()')[0])
		units.append(cdata[6].xpath('font/text()')[0])

		if len(cdata[7].xpath('font/a/text()')) > 0:
			titles.append(cdata[7].xpath('font/a/text()')[0])
		else:
			titles.append(cdata[7].xpath('font/text()')[0][18:][:-9])

		daysTaught.append(cdata[8].xpath('font/text()')[0])
		times.append(cdata[9].xpath('font/text()')[0])

		locationtext = cdata[10].xpath('font/text()')
		if locationtext == [u'\xa0']:
			locations.append(cdata[10].xpath('font/a/text()')[0])
		else:
			locations.append(locationtext[0])

		instructortext = cdata[12].xpath('font/text()')
		if instructortext == [u'\xa0']:
			instructors.append(cdata[12].xpath('font/a/text()')[0])
		else:
			instructors.append(instructortext[0])

# This is for my personal project which runs on meteor and mangodb
client = MongoClient('mongodb://127.0.0.1:3001/')
db = client['meteor']
tasks = db['classes']

# This database schema is likely to change due to repeats and different section numbers
# But as a proof of concept this is wonderful right now
for i in range(0, len(titles)):     
	tasks.insert({         
		"catalogNumber": catalogNumbers[i],         
		"section": sections[i],         
		"unit": units[i],
		"title": titles[i],         
		"daysTaught": daysTaught[i],         
		"time": times[i],         
		"location": locations[i],         
		"instructor": instructors[i],         
		"createdAt": datetime.datetime.utcnow()     
	})

